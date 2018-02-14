#! /usr/local/bin/python

import os
import json
import re
import time
import flask
import sqlite3
import datetime
import dateutil.parser


# SETUP

app = flask.Flask(__name__)

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'barc.db'),
    UPLOAD_FOLDER=os.path.join(app.root_path, 'images'),
))


# TEMPLATING

def format_datetime(value):
    return dateutil.parser.parse(value).strftime('%b %d, %Y %-I:%M %p')

def format_percent(value):
    if value == '': return 0
    return str(int(float(value) * 100)) + '%'

def format_result(value):
    if not value: return ''
    if value == '': return ''
    result = json.loads(value)
    lines = [ ]
    for r in result:
        lines.append('%s (%.0f%%)' % (r[1], r[0] * 100, ))
    return ', '.join(lines)

app.jinja_env.filters['datetime'] = format_datetime
app.jinja_env.filters['percent'] = format_percent
app.jinja_env.filters['result'] = format_result



# DATABASE

def connect_db():
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def get_db():
    if not hasattr(flask.g, 'sqlite_db'): flask.g.sqlite_db = connect_db()
    return flask.g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    if hasattr(flask.g, 'sqlite_db'): flask.g.sqlite_db.close()




# INIT COMMANDS

# creates a fresh database, downloads inception, and loads the caption codes
@app.cli.command('init_db')
def init_db_command():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    print('Initialized new database.')

# loads images to database or if they exist, reclassifies them
@app.cli.command('init_images')
def init_images_command():
    load_nn()
    db = get_db()
    cursor = db.cursor()
    for img in os.listdir(app.config['UPLOAD_FOLDER']):
        if (img[-3:].lower() == 'jpg'):
            print 'Adding image %s' % img[:-4]
            image_id = img[:-4]
            r = cursor.execute(
                'SELECT id FROM images WHERE id = ?',
                (image_id, )
            )
            if not r.fetchone():
                add_image(image_id=image_id)
            classify_image(image_id)



# IMAGE FUNCTIONS

# adds image to the database
def add_image(image_id = None, device_id = None, ip_address = None):
    db = get_db()
    cursor = db.cursor()
    created_at = datetime.datetime.now().isoformat()

    if image_id:
        cursor.execute(
           'INSERT INTO images (id, created_at, device_id, ip_address) VALUES (?, ?, ?, ?)',
           (image_id, created_at, device_id, ip_address)
        )
    else:
        cursor.execute(
           'INSERT INTO images (created_at, device_id, ip_address) VALUES (?, ?, ?)',
           (created_at, device_id, ip_address)
        )

    db.commit()
    return cursor.lastrowid

# runs the AI and adds the result to the database
def classify_image(image_id):
    db = get_db()
    cursor = db.cursor()
    filename = os.path.join(
        app.config['UPLOAD_FOLDER'],
        str(image_id) + '.jpg'
    )

    start = time.time()
    result = ai(filename)
    latency = int((time.time()- start) * 1000.0)

    print 'AI found: %s with %.0f%% accuracy in %0.0f ms' % (result[0][1], result[0][0] * 100, latency)

    cursor.execute(
       "UPDATE images SET result = ?, latency = ? WHERE id = ?",
       (json.dumps(result), latency, image_id)
    )

    db.commit()

    return result



# ROUTES

def check_auth(username, password):
    return (
        username == os.environ['BARC_USERNAME'] and
        password == os.environ['BARC_PASSWORD']
    )

@app.route('/')
def ui():
    auth = flask.request.authorization
    if not auth or not check_auth(auth.username, auth.password):
        return flask.Response(
            'You have to login with proper credentials',
            401,
            { 'WWW-Authenticate': 'Basic realm="Login Required"' }
        )
    db = get_db()
    cursor = db.cursor()
    images = cursor.execute(
        'SELECT * FROM images ORDER BY id DESC LIMIT 1000'
    )
    return flask.render_template('images.html', images=images)


@app.route('/api/images', methods=['GET', 'POST'])
def upload_file():

    # Poor man's token authentication
    auth_header = flask.request.headers.get('Authorization')
    if auth_header != 'Token token=' + os.environ['BARC_PASSWORD']:
        return '', 401

    # POST new image
    if flask.request.method == 'POST':

        if 'file' not in flask.request.files:
            flask.abort(422)

        if 'device_id' not in flask.request.form:
            flask.abort(422)

        file = flask.request.files['file']

        if not file or not file.filename.lower().endswith('.jpg'):
            flask.abort(422)

        device_id = flask.request.form['device_id']

        image_id = add_image(
            device_id=device_id, 
            ip_address=flask.request.remote_addr
        )

        filename = os.path.join(
            app.config['UPLOAD_FOLDER'],
            str(image_id) + '.jpg'
        )

        file.save(filename)

        try:
            result = classify_image(image_id)
        except Exception as detail:
            print "AI error:", detail
            return flask.jsonify(result=None)

        first_result = re.sub(
            r'(bedroom|dining_room|foyer|hallway|living_room|pumpkin)_',
            '',
            result[0][1]
        )
        first_result = first_result.replace('_',' ')

        if result[0][0] >= .8:
            return flask.jsonify(result=first_result)
        else:
            return flask.jsonify(result=None)

    # GET will be API JSON response
    else:
        flask.abort(404)


@app.route('/images/<path:path>')
def send_js(path):
    return flask.send_from_directory('images', path)



# AI

model = None
labels = None

def load_nn():
    global model, labels
    from keras.models import load_model

    model = load_model('model/nn.h5')
    # https://github.com/fchollet/keras/issues/6462
    model._make_predict_function()

    with open('model/labels.json', 'r') as fp:
        labels = json.load(fp)

def ai(image):
    global model, labels
    if not model: load_nn()
    from keras.preprocessing.image import load_img, img_to_array
    from keras.applications.inception_v3 import preprocess_input

    img = load_img(image, target_size=(299, 299))
    data = img_to_array(img)
    data = data.reshape((1,) + data.shape)
    data = preprocess_input(data)

    prediction = model.predict(data)

    top_5 = [ ]
    for i in prediction.argsort(axis=-1)[0][::-1][0:5]:
        top_5.append((float(prediction[0][i]), labels[i], ))

    return top_5


# SETUP

if __name__ == '__main__':
    load_nn()
    app.run(port=5000, host='0.0.0.0')


import os
import json
import flask
import sqlite3
import datetime
import dateutil.parser
from keras.models import load_model
from keras.preprocessing.image import load_img, img_to_array
from keras.applications.inception_v3 import preprocess_input
from six.moves import urllib

# SETUP

application = flask.Flask(__name__)

application.config.update(dict(
    DATABASE=os.path.join(application.root_path, 'barc.db'),
    UPLOAD_FOLDER=os.path.join(application.root_path, 'images'),
))

def format_datetime(value):
    return dateutil.parser.parse(value).strftime('%b %d, %Y %-I:%M %p')

def format_percent(value):
    if value == '': return 0
    return str(int(float(value) * 100)) + '%'

application.jinja_env.filters['datetime'] = format_datetime
application.jinja_env.filters['percent'] = format_percent

model_dir = os.path.join(application.root_path, 'inception')

def connect_db():
    rv = sqlite3.connect(application.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def get_db():
    if not hasattr(flask.g, 'sqlite_db'): flask.g.sqlite_db = connect_db()
    return flask.g.sqlite_db

@application.teardown_appcontext
def close_db(error):
    if hasattr(flask.g, 'sqlite_db'): flask.g.sqlite_db.close()

# creates a fresh database, downloads inception, and loads the caption codes
@application.cli.command('init')
def init_command():
    db = get_db()
    with application.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    print('Initialized new database.')



# ROUTES

def check_auth(username, password):
    return (
        username == os.environ['BARC_USERNAME'] and
        password == os.environ['BARC_PASSWORD']
    )


def authenticate():
    return flask.Response(
        'Could not verify your access level for that URL.\n'
        'You have to login with proper credentials', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'}
    )


@application.route('/')
def ui():
    auth = flask.request.authorization
    if not auth or not check_auth(auth.username, auth.password):
        return authenticate()
    db = get_db()
    cursor = db.cursor()
    images = cursor.execute('''
        SELECT * FROM images
        ORDER BY created_at DESC LIMIT 100
    ''')
    return flask.render_template('images.html', images=images)


@application.route('/api/images', methods=['GET', 'POST'])
def upload_file():

    # Poor man's token authentication
    auth_header = flask.request.headers.get('Authorization')
    if auth_header != 'Token token=' + os.environ['BARC_PASSWORD']:
        return '', 401

    # POST new image
    if flask.request.method == 'POST':
        if 'file' not in flask.request.files:
            flask.abort(422)
        file = flask.request.files['file']
        if not file or not file.filename.lower().endswith('.jpg'):
            flask.abort(422)
        image_id = 0
        db = get_db()
        cursor = db.cursor()
        created_at = datetime.datetime.now().isoformat()
        cursor.execute(
           '''INSERT INTO images (created_at) VALUES (?)''',
           (created_at,)
        )
        image_id = cursor.lastrowid
        filename = os.path.join(
            application.config['UPLOAD_FOLDER'],
            str(image_id) + '.jpg'
        )
        file.save(filename)

        try:
            result, score = ai(filename)
        except Exception as detail:
            print "AI error:", detail
            db.commit()
            return flask.jsonify(result=None)

        print 'AI found: ', result, score

        cursor.execute(
           "UPDATE images SET result = ?, score = ? WHERE id = ?",
           (result, str(score), image_id)
        )

        db.commit()

        first_result = result.replace('_',' ')

        return flask.jsonify(result=(first_result if score >= .3 else None))

    # GET will be API JSON response
    else:
        flask.abort(404)


@application.route('/images/<path:path>')
def send_js(path):
    return flask.send_from_directory('images', path)



# AI

model = load_model('model/nn.h5')

# https://github.com/fchollet/keras/issues/6462
model._make_predict_function()

with open('model/labels.json', 'r') as fp:
    labels = json.load(fp)

def ai(image):
    img = load_img(image, target_size=(299, 299))
    data = img_to_array(img)
    data = data.reshape((1,) + data.shape)
    data = preprocess_input(data)

    prediction = model.predict(data)

    label = labels[prediction.argmax(axis=-1)[0]]
    value = prediction[0][prediction.argmax(axis=-1)[0]]

    return label, value


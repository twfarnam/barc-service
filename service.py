import os
import flask
import sqlite3
import datetime
import dateutil.parser # pip install python-dateutil
import sys
import re
import tarfile
import tensorflow as tf
import numpy as np
from six.moves import urllib


# SETUP

# removes TensorFlow verbose messages
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'

app = flask.Flask(__name__)

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'barc.db'),
    UPLOAD_FOLDER=os.path.join(app.root_path, 'images'),
))

def format_datetime(value):
    return dateutil.parser.parse(value).strftime('%b %d, %Y %-I:%M %p')

app.jinja_env.filters['datetime'] = format_datetime

model_dir = os.path.join(app.root_path, 'inception')

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

# creates a fresh database, downloads inception, and loads the caption codes
@app.cli.command('init')
def init_command():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    print('Initialized new database.')

    DATA_URL = 'http://download.tensorflow.org/models/image/imagenet/inception-2015-12-05.tgz'

    model_dir = os.path.join(app.root_path, 'inception')

    if not os.path.exists(model_dir):
      os.makedirs(model_dir)

    filename = DATA_URL.split('/')[-1]
    filepath = os.path.join(model_dir, filename)
    if not os.path.exists(filepath):
      def _progress(count, block_size, total_size):
        sys.stdout.write('\r>> Downloading %s %.1f%%' % (
            filename, float(count * block_size) / float(total_size) * 100.0))
        sys.stdout.flush()
      filepath, _ = urllib.request.urlretrieve(DATA_URL, filepath, _progress)
      print()
      statinfo = os.stat(filepath)
      print('Successfully downloaded', filename, statinfo.st_size, 'bytes.')
    tarfile.open(filepath, 'r:gz').extractall(model_dir)

    # Load mapping from string UID to human-readable string. File like:
    #      n00004475	organism, being
    uid_to_human = {}
    uid_lookup_path = os.path.join(
        model_dir,
        'imagenet_synset_to_human_label_map.txt'
    )
    p = re.compile(r'[n\d]*[ \S,]*')
    for line in tf.gfile.GFile(uid_lookup_path).readlines():
      parsed_items = p.findall(line)
      uid = parsed_items[0]
      human_string = parsed_items[2]
      uid_to_human[uid] = human_string

    # Load mapping from string UID to integer node ID. File looks like:
    #     entry {
    #       target_class: 449
    #       target_class_string: "n01440764"
    #     }
    node_id_to_uid = {}
    label_lookup_path = os.path.join(
        model_dir,
        'imagenet_2012_challenge_label_map_proto.pbtxt'
    )
    for line in tf.gfile.GFile(label_lookup_path).readlines():
      if line.startswith('  target_class:'):
        target_class = int(line.split(': ')[1])
      if line.startswith('  target_class_string:'):
        target_class_string = line.split(': ')[1]
        node_id_to_uid[target_class] = target_class_string[1:-2]

    cursor = db.cursor()

    # Final mapping of integer node ID to human-readable string
    for key, val in node_id_to_uid.items():
      if val not in uid_to_human:
        tf.logging.fatal('Failed to locate: %s', val)
      cursor.execute(
        "INSERT INTO captions ('id', 'caption') VALUES (?, ?)",
        (key, uid_to_human[val])
      )

    db.commit()





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


@app.route('/')
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
            app.config['UPLOAD_FOLDER'],
            str(image_id) + '.jpg'
        )
        file.save(filename)

        caption_id, score = run_inference_on_image(filename)

        if score > .5:
            cursor.execute(
                "SELECT id, caption FROM captions WHERE id == ?",
                (caption_id,)
            )

            result = cursor.fetchone()[1]

            cursor.execute(
               "UPDATE images SET result = ? WHERE id = ?",
               (result, image_id)
            )

            db.commit()
            return flask.jsonify(id=image_id, result=result)

        else:
            return flask.jsonify(id=image_id, result=None, score=score)

    # GET will be API JSON response
    else:
        flask.abort(404)


@app.route('/images/<path:path>')
def send_js(path):
    return flask.send_from_directory('images', path)




# AI

def create_graph():
  filename = os.path.join(model_dir, 'classify_image_graph_def.pb')
  with tf.gfile.FastGFile(filename, 'rb') as f:
    graph_def = tf.GraphDef()
    graph_def.ParseFromString(f.read())
    tf.import_graph_def(graph_def, name='')

filename = os.path.join(model_dir, 'classify_image_graph_def.pb')
graph_def = tf.GraphDef()
with tf.gfile.FastGFile(filename, 'rb') as f:
    graph_def.ParseFromString(f.read())



def run_inference_on_image(image):

  if not tf.gfile.Exists(image):
    tf.logging.fatal('File does not exist %s', image)

  image_data = tf.gfile.FastGFile(image, 'rb').read()

  # XXX 
  # want to run this only once instead of on every request but somehow the
  # default graph is getting reset before we can use it
  tf.import_graph_def(graph_def, name='')

  with tf.Session() as sess:
    # Some useful tensors:
    # 'softmax:0': A tensor containing the normalized prediction across
    #   1000 labels.
    # 'pool_3:0': A tensor containing the next-to-last layer containing 2048
    #   float description of the image.
    # 'DecodeJpeg/contents:0': A tensor containing a string providing JPEG
    #   encoding of the image.
    # Runs the softmax tensor by feeding the image_data as input to the graph.
    softmax_tensor = sess.graph.get_tensor_by_name('softmax:0')

    predictions = sess.run(
        softmax_tensor,
        {'DecodeJpeg/contents:0': image_data}
    )

    predictions = np.squeeze(predictions)

    n = predictions.argsort()[-1]
    return n, predictions[n]


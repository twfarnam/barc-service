#! /usr/bin/env python

import os
import json
import re
import flask
import datetime

from db import get_db
from helpers import token_auth, simple_auth, authorize
from image import ImageView



# SETUP

app = flask.Flask(__name__, template_folder='.', static_folder='../../static')





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
@app.cli.command('import_images')
def import_images_command():
    # load_nn()
    db = get_db()
    cursor = db.cursor()
    for img in os.listdir(os.path.join(app.root_path, '../../images')):
        if (img[-3:].lower() == 'jpg'):
            print 'Adding image %s' % img[:-4]
            image_id = img[:-4]
            r = cursor.execute(
                'SELECT id FROM images WHERE id = ?',
                (image_id, )
            )
            if not r.fetchone():
                add_image(image_id=image_id)
            # classify_image(image_id)



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







# ROUTES

@app.route('/')
@app.route('/<path:path>')
def frontend(path=''):
    if not simple_auth(): 
        return authorize()
    return flask.render_template('index.html')

@app.route('/images/<path:path>')
def send_images(path):
    return flask.send_from_directory('../../images', path)

image_view = ImageView.as_view('image_view')
app.add_url_rule('/api/images', view_func=image_view, methods=[ 'GET' ])
app.add_url_rule('/api/images', view_func=image_view, methods=[ 'POST' ])
app.add_url_rule(
    '/api/images/<int:image_id>',
    view_func=image_view,
    methods=[ 'PATCH' ]
)


# SETUP

if __name__ == '__main__':
    app.run(port=5000, host='0.0.0.0')


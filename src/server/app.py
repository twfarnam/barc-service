#! /usr/bin/env python

import os
import json
import re
import flask
import datetime

from db import get_db
from helpers import token_auth, simple_auth, authorize
from image import ImageView


app = flask.Flask(__name__, template_folder='.', static_folder='../../static')

@app.route('/')
@app.route('/<path:path>')
def frontend(path=''):
    if not simple_auth(): 
        return authorize()
    return flask.render_template('index.html')

@app.route('/images/<path:path>')
def send_images(path):
    return flask.send_from_directory('../../images', path)

view = ImageView.as_view('image_view')
app.add_url_rule('/api/images', view_func=view, methods=[ 'GET' ])
app.add_url_rule('/api/images', view_func=view, methods=[ 'POST' ])
app.add_url_rule('/api/images/<image_id>', view_func=view, methods=[ 'PATCH' ])

if __name__ == '__main__':
    app.run(port=5000, host='0.0.0.0')


import flask
import os
from flask.views import MethodView

from db import get_db
from helpers import token_auth, simple_auth, authorize


class ImageView(MethodView):


    # index of images, uses ?from=
    def get(self):
        if not simple_auth(): 
            return authorize()

        db = get_db()
        cursor = db.cursor()

        count = cursor.execute(
            'SELECT count(*) as total FROM images'
        ).fetchone()['total']

        offset = flask.request.args.get('from', 0)
        images = cursor.execute(
            'SELECT * FROM images ORDER BY id DESC LIMIT 10 OFFSET ?', 
            (offset, )
        ).fetchall()

        return flask.jsonify(count=count, images=images)


    # update a single user
    def patch(self, image_id):
        pass


    # create a new image
    def post(self):

        if not token_auth(flask.request.headers.get('Authorization')):
            return '', 401

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

        return '', 200




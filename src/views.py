import flask
import json
from flask.views import MethodView
from sqlalchemy import desc
from sqlalchemy.orm import joinedload
from models import Image, Category, Session, newID


class CategoryView(MethodView):

    def get(self):
        session = Session()
        categories = (
            session.query(Category)
            .order_by(Category.room, Category.object)
        )
        return flask.jsonify(data=[ r.dict() for r in categories ])


class ImageView(MethodView):

    # index of images
    def get(self):
        session = Session()

        # XXX must do some kind of checking of those parameters
        meta = {
            'count': session.query(Image).count(),
            'order': flask.request.args.get('order', 'created_at desc'),
            'offset': int(flask.request.args.get('offset', 0)),
            'limit': int(flask.request.args.get('limit', 10)),
        }

        if meta['order'] == 'created_at asc':
            order = Image.created_at
        else:
            order = desc(Image.created_at)

        images = (
            session.query(Image)
            .order_by(order)
            .limit(meta['limit'])
            .offset(meta['offset'])
            .options(joinedload('categories'))
        )

        return flask.jsonify(meta=meta, data=[ r.dict() for r in images ])


    # update an image's categories
    def patch(self, image_id):
        session = Session()
        image = session.query(Image).get(image_id)
        ids = flask.request.json['categories']
        if len(ids) > 0:
            categories = session.query(Category).filter(Category.id.in_(ids))
        else:
            categories = [ ]
        image.categories[:] = categories
        session.commit()
        return '', 200


    # create an image
    def post(self):

        if 'file' not in flask.request.files:
            flask.abort(422)

        session = Session()

        image_id = newID()

        image = Image(
            id=image_id,
            device_id=flask.request.form['device_id'],
            result=flask.request.form['result'],
            motion=flask.request.form['motion'],
            ip_address=flask.request.remote_addr,
        )

        flask.request.files['file'].save(image.filename())

        result = json.loads(flask.request.form['result'])
        labels = [ ]
        for r in result:
            if r['confidence'] > .3: labels.append(r['label'])

        if len(labels) > 0:
            image.categories = (
                session.query(Category)
                .filter(Category.label.in_(labels))
                .all()
            )

        session.add(image)
        session.commit()

        return '', 200




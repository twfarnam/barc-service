import flask
from .views import ImageView, CategoryView
from .models import Image
from .auth import AuthMiddleware


app = flask.Flask(
    __name__,
    template_folder='.',
    static_folder='../static'
)
app.wsgi_app = AuthMiddleware(app.wsgi_app)


@app.route('/')
@app.route('/images')
@app.route('/objects')
def frontend():
    return flask.render_template('index.html')

# this and static_folder served directly by nginx in production (n.b. without
# authentication but UUID image names should prevent scraping)
@app.route('/static/images/<path:path>')
def send_images(path):
    return flask.send_from_directory('../images', path)

app.add_url_rule(
    '/api/categories',
    view_func=CategoryView.as_view('category_view')
)

image_view = ImageView.as_view('image_view')
app.add_url_rule(
    '/api/images',
    view_func=image_view,
    methods=['GET', 'POST']
)
app.add_url_rule(
    '/api/images/<image_id>',
    view_func=image_view,
    methods=[ 'PATCH', 'DELETE' ]
)


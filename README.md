
To create a fresh databse:

    FLASK_APP=service.py flask init

To run in development mode:

    FLASK_APP=service.py FLASK_DEBUG=1 BARC_USERNAME=admin BARC_PASSWORD=secret flask run --host=0.0.0.0

To do a test upload with CURL:

    curl -F "file=@sloth.jpg" -H "Authorization: Token token=secret" localhost:5000/api/images

To run in production:

    pip install -r requirements.txt
    BARC_USERNAME=admin BARC_PASSWORD=secret uwsgi --ini service.ini --plugin python



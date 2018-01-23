
To create a fresh databse:

    FLASK_APP=service.py flask init_db

To upload images:

    FLASK_APP=service.py flask init_images

To run in development mode:

    FLASK_DEBUG=1 BARC_USERNAME=admin BARC_PASSWORD=secret ./service.py

To do a test upload with CURL:

    curl -F "file=@sloth.jpg" -F "device_id=test" -H "Authorization: Token token=secret" localhost:5000/api/images

To run in production:

    pip install -r requirements.txt
    BARC_USERNAME=admin BARC_PASSWORD=secret python service.py

To test production service with a training file:

    curl -F "file=@../training/data/validation/pumpkin_armoire/90.jpg" -F "device_id=test" -H "Authorization: Token token=secret" https://barc.squids.online/api/images




To create a fresh databse:

    FLASK_APP=src/server/app.py flask init_db

To upload images:

    FLASK_APP=src/server/app.py flask init_images

To run in development mode:

    npm start
    FLASK_DEBUG=1 BARC_USERNAME=admin BARC_PASSWORD=secret ./src/server/app.py

Then open http://localhost:5001.

To compile production JavaScript:
    npm run build

Test an upload with CURL:

    curl -F "file=@sloth.jpg" -F "device_id=test" -H "Authorization: Token token=secret" localhost:5000/api/images

Run in production:

    pip install -r requirements.txt
    BARC_USERNAME=admin BARC_PASSWORD=secret ./src/server/app.py

To test production service with a training file:

    curl -F "file=@../training/data/validation/pumpkin_armoire/90.jpg" -F "device_id=test" -H "Authorization: Token token=secret" https://barc.squids.online/api/images



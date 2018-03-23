To import images that you just made:

    python -m src.import.import_video_images

To run in development mode:

    npm start

And in a new shell:

    export FLASK_DEBUG=1 BARC_USERNAME=admin BARC_PASSWORD=secret
    ./src/server/app.py

Then open http://localhost:5001

To compile production JavaScript:

    npm run build

Run it in production (with the correct password, of course):

    pip install -r requirements.txt
    BARC_USERNAME=admin BARC_PASSWORD=secret ./src/server/app.py


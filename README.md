To import videos from import/videos/<CATEGORY>/video.mp4:

    python -m src.import.import_videos

To run in development mode:

    npm start

And in a new shell:

    export FLASK_DEBUG=1 BARC_USERNAME=admin BARC_PASSWORD=secret
    ./src/app.py

Then open http://localhost:5001

To compile production JavaScript:

    npm run build

Run it in production (with the correct username and password, of course):

    pip install -r requirements.txt
    export BARC_USERNAME=admin BARC_PASSWORD=secret
    ./src/app.py


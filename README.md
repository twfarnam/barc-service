To import videos from import/videos/<CATEGORY>/video.mp4:

    python -m src.import.import_videos

To run in development mode:

    export FLASK_DEBUG=1 BARC_USERNAME=admin BARC_PASSWORD=secret
    ./src/app.py

Then open http://localhost:5000 in a browser. If you also need JavaScript
changes via webpack, open a new shell and run:

    npm start

Then open http://localhost:5001 in the browser. To compile production
JavaScript:

    npm run build

Run it in production (with the correct username and password, of course):

    pip install -r requirements.txt
    export BARC_USERNAME=admin BARC_PASSWORD=secret
    ./barc.py serve


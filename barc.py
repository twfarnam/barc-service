#! /usr/bin/env python3

import argparse

parser = argparse.ArgumentParser(
    description='Run the Barc web service and related tasks'
)

parser.add_argument(
    'command',
    action='store',
    default=[ 'serve' ],
    choices=[
        'serve',
        'categorize',
        'recategorize',
        'import-uncategorized',
        'import-videos'
    ],
    help='one of: serve, categorize, recategorize, import-videos, import-uncategorized',
)

parser.add_argument(
    '--arch',
    action='store',
    dest='architecture',
    nargs=1,
    type=str,
    default=[ 'inception' ],
    choices=[ 'mobilenets', 'inception' ],
    help='which architecture to use, default is inception',
)

parser.add_argument(
    '--image',
    action='store',
    dest='image',
    nargs='+',
    type=str,
    help='image files to run through neural network',
)

args = parser.parse_args()

if args.command == 'serve':
    from src.service import app 
    app.run(port=5000, host='0.0.0.0')
elif args.command == 'recategorize':
    from src.recategorize import run
    run(args.architecture[0])
elif args.command == 'categorize':
    from src.neural_net import load_model, load_image, labels
    model = load_model(args.architecture[0])
    for path in args.image:
        prediction = model.predict(load_image(path, args.architecture[0]))[0]
        result = [ ]
        for i, confidence in enumerate(prediction):
            if float(confidence) > .05:
                result.append(( labels[i], float(confidence), ))
        sorted_result = sorted(result, key=lambda r: -r[1])
        for (label, confidence) in sorted_result:
            print("{:<35}{:.0%}".format(label, confidence))
elif args.command == 'import-uncategorized':
    from src.import_uncategorized import run
    run(args.architecture[0])
elif args.command == 'import-videos':
    from src.import_videos import run
    run()


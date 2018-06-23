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
    from src.categorize import run
    run(args.architecture[0], args.image)
elif args.command == 'import-uncategorized':
    from src.import_uncategorized import run
    run(args.architecture[0])
elif args.command == 'import-videos':
    from src.import_videos import run
    run()


#! /usr/bin/env python

import os
import re
import tempfile
from shutil import copyfile, rmtree
from models import Session, Category, Image, newID
from subprocess import call

root = os.path.normpath(os.path.join(os.path.dirname(__file__), '..'))
video_dir = os.path.join(root, 'import', 'videos')
session = Session()

for room in os.listdir(video_dir):
    if room.startswith('.'): continue

    for obj in os.listdir(os.path.join(video_dir, room)):
        if obj.startswith('.'): continue

        category = session.query(Category).filter(Category.object == obj).first()
        print(category)

        if category == None:
            category = Category(room=room, object=obj)
            session.add(category)
        print(category)
        session.commit()


        for video in os.listdir(os.path.join(video_dir, room, obj)):
            if video.startswith('.'): continue

            temp_dir = tempfile.mkdtemp()

            call([
                "ffmpeg",
                "-i", os.path.join(video_dir, room, obj, video),
                "-vf", "scale=299:532",
                "-r", "5/1",
                os.path.join(temp_dir, "%03d.jpg"),
            ])

            for image_file in os.listdir(temp_dir):

                id = newID()
                image = Image(id=id)
                image.categories.append(category)
                session.add(image)

                src_path = os.path.join(temp_dir, image_file)
                print(src_path)
                copyfile(src_path, image.filename())

            rmtree(temp_dir)

session.commit()


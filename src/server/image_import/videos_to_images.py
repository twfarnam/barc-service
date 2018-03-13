#! /usr/bin/env python

import os
from shutil import rmtree
from subprocess import call

this_dir = os.path.dirname(__file__)
video_dir = os.path.normpath(this_dir + '/../../../import/videos')
image_dir = os.path.normpath(this_dir + '/../../../import/images')

if os.path.exists(image_dir):
    rmtree(image_dir)
os.makedirs(image_dir)

for slug in os.listdir(video_dir):
    if slug.startswith('.'): continue
    input_slug_dir = os.path.join(video_dir, slug)
    output_slug_dir = os.path.join(image_dir, slug)
    if not os.path.exists(output_slug_dir): os.makedirs(output_slug_dir)
    for video in os.listdir(input_slug_dir):
        if video.startswith('.'): continue
        out_dir = os.path.join(output_slug_dir, video)
        os.makedirs(out_dir)
        call([
            "ffmpeg",
            "-i", os.path.join(input_slug_dir, video),
            "-vf", "scale=299:532",
            "-r", "5/1",
            os.path.join(out_dir, "%03d.jpg"),
        ])




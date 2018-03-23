import os
import re
from shutil import copyfile
from ..models import Session, Category, Image, newID

root = os.path.normpath(os.path.dirname(__file__) + '/../..')
image_dir = os.path.join(root, 'import/images')

session = Session()

for slug in os.listdir(image_dir):
    if slug.startswith('.'): continue
    slug_dir = os.path.join(image_dir, slug)

    room, object = re.match(
        r'(bedroom|dining room|foyer|hallway|living room|pumpkin) (.*)',
        slug.replace('_',' ')
    ).group(1, 2)
    category = Category(room=room, object=object)
    session.add(category)

    for video in os.listdir(slug_dir):
        if video.startswith('.'): continue
        video_dir = os.path.join(slug_dir, video)
        for image_file in os.listdir(video_dir):
            if image_file.startswith('.'): continue

            id = newID()
            image = Image(id=id)
            image.categories.append(category)
            session.add(image)

            src_path = os.path.join(video_dir, image_file)
            print src_path
            copyfile(src_path, image.filename())

session.commit()


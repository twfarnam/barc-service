import os
import json
from shutil import copyfile
from .neural_net import labels, load_model, load_image
from .models import Session, Category, Image, newID


def run(architecture):
    root = os.path.normpath(os.path.join(os.path.dirname(__file__), '..'))
    image_dir = os.path.join(root, 'import/uncategorized')

    model = load_model(architecture)

    for image in os.listdir(image_dir):
        if image.startswith('.'): continue

        src_path = os.path.join(image_dir, image)
        print(src_path)

        image = Image(id=newID())
        img_data = load_image(src_path, architecture)

        prediction = model.predict(img_data)[0]

        session = Session()

        result = [ ]
        for i, confidence in enumerate(prediction):

            if float(confidence) > .05:
                result.append({
                    'confidence' : float(confidence),
                    'label' : labels[i],
                })

            if float(confidence) > .25:
                cat = (
                    session.query(Category)
                    .filter(Category.label == labels[i])
                    .first()
                )
                if cat: image.categories.append(cat)

        image.result = json.dumps(sorted(result, key=lambda r: -r['confidence']))
        print(result)

        copyfile(src_path, image.filename())

        session.add(image)

        session.commit()



#! /usr/bin/env python

import os
import json
from keras.models import load_model
from keras.preprocessing.image import load_img, img_to_array
from keras.applications.inception_v3 import preprocess_input
from models import Session, Category, Image, newID
from shutil import copyfile

root = os.path.normpath(os.path.join(os.path.dirname(__file__), '..'))
image_dir = os.path.join(root, 'import/uncategorized')
model_path = os.path.join(root, 'model/inception.h5')
labels_path = os.path.join(root, 'model/labels.json')

model = load_model(model_path)
model._make_predict_function()


with open(labels_path, 'r') as fp:
    labels = json.load(fp)

files = sorted(os.listdir(image_dir), key=lambda f: int(f.split('.')[0])  )

for image in files:
    if image.startswith('.'): continue

    src_path = os.path.join(image_dir, image)
    print(src_path)

    image = Image(id=newID())
    img_data = img_to_array(load_img(src_path, target_size=(299, 299)))
    img_data = img_data.reshape((1,) + img_data.shape)
    img_data = preprocess_input(img_data)

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



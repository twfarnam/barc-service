#! /usr/bin/env python

import os
import json
from keras.models import load_model
from keras.preprocessing.image import load_img, img_to_array
from keras.applications.inception_v3 import preprocess_input
from ..models import Session, Category, Image, newID
from shutil import copyfile

root = os.path.normpath(os.path.dirname(__file__) + '/../..')
image_dir = os.path.join(root, 'import/uncategorized')
model_path = os.path.join(root, 'model/inception.h5')
labels_path = os.path.join(root, 'model/labels.json')

model = load_model(model_path)
model._make_predict_function()

session = Session()

with open(labels_path, 'r') as fp:
    labels = json.load(fp)

for image in os.listdir(image_dir):
    if image.startswith('.'): continue

    src_path = os.path.join(image_dir, image)
    print src_path

    id = newID()
    image = Image(id=id)

    img_data = img_to_array(load_img(src_path, target_size=(299, 299)))
    img_data = img_data.reshape((1,) + img_data.shape)
    img_data = preprocess_input(img_data)

    prediction = model.predict(img_data)[0]

    for i, confidence in enumerate(prediction):
        if float(confidence) > .5:
            cat = (
                session.query(Category)
                .filter(Category.label == labels[i])
                .first()
            )
            if cat: image.categories.append(cat)

    # images.categories.append( )

    copyfile(src_path, image.filename())

    session.add(image)


session.commit()




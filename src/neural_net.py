import os
import json
import keras
import keras_applications

keras_applications.set_keras_submodules(
    backend=keras.backend,
    engine=keras.engine,
    layers=keras.layers,
    models=keras.models,
    utils=keras.utils)

from keras_applications.mobilenet_v2 import relu6
from keras.preprocessing.image import load_img, img_to_array
from keras.applications.inception_v3 import preprocess_input

root = os.path.normpath(os.path.join(os.path.dirname(__file__), '..'))

labels_path = os.path.join(root, 'model/labels.json')
with open(labels_path, 'r') as fp:
    labels = json.load(fp)

def load_image(filename, architecture):
    if architecture == 'inception':
        target_size = (299, 299, )
    elif architecture == 'mobilenets':
        target_size = (224, 224, )
    else:
        raise ValueError('architecture must be inception or mobilenets.')

    img_data = img_to_array(load_img(filename, target_size=target_size))
    img_data = img_data.reshape((1,) + img_data.shape)
    return preprocess_input(img_data)

def load_model(architecture):
    if architecture == 'mobilenets':
        model_path = os.path.join(root, 'model/mobilenets.h5')
        model = keras.models.load_model(
                    model_path,
                    custom_objects={ 'relu6': relu6 })
        model._make_predict_function()
        return model
    elif architecture == 'inception':
        model_path = os.path.join(root, 'model/inception.h5')
        model = keras.models.load_model(model_path)
        model._make_predict_function()
        return model
    else:
        raise ValueError('architecture must be inception or mobilenets.')




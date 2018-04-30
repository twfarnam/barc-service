import os
import json
import keras
from keras.utils.generic_utils import CustomObjectScope
from keras.applications.mobilenet import relu6, DepthwiseConv2D
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
        layers = { 'relu6': relu6, 'DepthwiseConv2D': DepthwiseConv2D }
        with CustomObjectScope(layers):
            model = keras.models.load_model(model_path)
        model._make_predict_function()
        return model
    elif architecture == 'inception':
        model_path = os.path.join(root, 'model/inception.h5')
        model = keras.models.load_model(model_path)
        model._make_predict_function()
        return model
    else:
        raise ValueError('architecture must be inception or mobilenets.')




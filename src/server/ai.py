
# runs the AI and adds the result to the database
def classify_image(image_id):
    db = get_db()
    cursor = db.cursor()
    filename = os.path.join(
        app.config['UPLOAD_FOLDER'],
        str(image_id) + '.jpg'
    )

    start = time.time()
    result = ai(filename)
    latency = int((time.time()- start) * 1000.0)

    cursor.execute(
       "UPDATE images SET result = ?, latency = ? WHERE id = ?",
       (json.dumps(result), latency, image_id)
    )

    db.commit()

    return result

model = None
labels = None

def load_nn():
    global model, labels
    from keras.models import load_model

    model = load_model('model/nn.h5')
    # https://github.com/fchollet/keras/issues/6462
    model._make_predict_function()

    with open('model/labels.json', 'r') as fp:
        labels = json.load(fp)

def ai(image):
    global model, labels
    if not model: load_nn()
    from keras.preprocessing.image import load_img, img_to_array
    from keras.applications.inception_v3 import preprocess_input

    img = load_img(image, target_size=(299, 299))
    data = img_to_array(img)
    data = data.reshape((1,) + data.shape)
    data = preprocess_input(data)

    prediction = model.predict(data)

    top_5 = [ ]
    for i in prediction.argsort(axis=-1)[0][::-1][0:5]:
        top_5.append((float(prediction[0][i]), labels[i], ))

    return top_5


import json
from .neural_net import labels, load_model, load_image
from .models import Session, Category, Image, newID

def run(architecture):

    session = Session()

    images = (
        session.query(Image)
        .filter(Image.deleted_at == None)
        .order_by('created_at DESC')
        .limit(500)
    )

    model = load_model(architecture)

    for image in images:

        image_data = load_image(image.filename(), architecture)

        prediction = model.predict(image_data)[0]

        result = [ ]
        for i, confidence in enumerate(prediction):
            result.append({
                'confidence' : float(confidence),
                'label' : labels[i],
            })

        sorted_result = sorted(result, key=lambda r: -r['confidence'])
        image.result = json.dumps(sorted_result)

        session.commit()



# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from tensorflow.keras.models import load_model
# from tensorflow.keras.preprocessing import image
# import numpy as np

# app = Flask(__name__)
# CORS(app)  # Enable CORS for all routes

# # Load your pre-trained Keras model
# model = load_model("model_55.keras")

# # Assuming your model expects images of a certain size
# img_size = (224, 224)

# @app.route('/classify-waste', methods=['POST'])
# def classify_waste():
#     try:
#         # Receive the image from the request
#         img = image.load_img(request.files['image'], target_size=img_size)
#         img_array = image.img_to_array(img)
#         img_array = np.expand_dims(img_array, axis=0)
#         img_array /= 255.0  # Normalize the image data

#         # Perform prediction using the loaded model
#         result = model.predict(img_array)

#         # Convert the prediction result to a human-readable class (replace this with your actual mapping)
#         classes = ['Biomedical', 'Electrical', 'Organic','Recyclable']   # Replace with your class labels
#         predicted_class = classes[np.argmax(result)]

#         return jsonify({'result': predicted_class})
#     except Exception as e:
#         print(f"Error: {e}")
#         return jsonify({'error': str(e)}), 500


# if __name__ == '__main__':
#     app.run(port=5000)


from flask import Flask, request, jsonify
from flask_cors import CORS
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from PIL import Image
import numpy as np
import io

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load your pre-trained Keras model
model = load_model("model_55.keras")

# Assuming your model expects images of a certain size
img_size = (224, 224)

@app.route('/classify-waste', methods=['POST'])
def classify_waste():
    try:
        # Receive the image from the request
        img_file = request.files['image']
        img = Image.open(io.BytesIO(img_file.read()))
        img = img.convert('RGB')  # Ensure the image has RGB channels
        img = img.resize(img_size)
        img_array = np.asarray(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = img_array.astype('float32') / 255.0  # Normalize the image data

        # Perform prediction using the loaded model
        result = model.predict(img_array)

        # Convert the prediction result to a human-readable class (replace this with your actual mapping)
        classes = ['Biomedical', 'Electrical', 'Organic','Recyclable']   # Replace with your class labels
        predicted_class = classes[np.argmax(result)]

        return jsonify({'result': predicted_class})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000)

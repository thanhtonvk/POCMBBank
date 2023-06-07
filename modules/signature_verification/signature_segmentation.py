import tensorflow as tf
from keras.applications.mobilenet_v2 import preprocess_input
import numpy as np
import cv2
from config import config


def preprocessing(image: np.ndarray):
    image = cv2.resize(image, (224, 224))
    image = np.expand_dims(image, 0)
    return image


def load_model():
    model = tf.keras.models.load_model(config.MODEL_SEGMENT)
    return model


class SignatureSegmentation:
    model = load_model()

    def predict(self, image: np.ndarray):
        h, w, _ = image.shape
        origin = image.copy()
        image = preprocessing(image)
        preds = self.model.predict(image,verbose=False)[0]
        preds = cv2.resize(preds, (w, h))
        for i, values in enumerate(preds):
            for j, value in enumerate(values):
                if value < 0.5:
                    origin[i, j] = 255
        return origin

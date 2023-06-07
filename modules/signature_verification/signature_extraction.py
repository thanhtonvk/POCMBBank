import tensorflow as tf
from config import config
import numpy as np
from keras.applications.resnet_v2 import preprocess_input
import cv2
from sklearn.metrics.pairwise import cosine_similarity


def load_model():
    model = tf.keras.models.load_model(config.MODEL_EXTRACTOR)
    model = tf.keras.Sequential(model.layers[:-1])
    return model


def preprocessing(image: np.ndarray):
    image = cv2.resize(image, (224, 224))
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image = preprocess_input(image)
    image = np.expand_dims(image, 0)
    return image


def compare(feature1: np.ndarray, feature2: np.ndarray):
    if cosine_similarity(feature1, feature2)[0][0] > config.THRESHOLD_SIMILARITY:
        return True
    return False


class SignatureExtraction:
    model = load_model()

    def extract_feature(self, image: np.ndarray):
        image = preprocessing(image)
        feature = self.model.predict(image,verbose=False)
        return feature


if __name__ == '__main__':
    image = cv2.imread('./Sig 00001.jpg')
    feature_extractor = SignatureExtraction()
    feature = feature_extractor.extract_feature(image)
    print(feature)

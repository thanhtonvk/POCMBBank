from ultralytics import YOLO
from config import config
import numpy as np
import cv2


def load_model():
    model = YOLO(config.MODEL_DETECTION)
    return model


def get_signature(image: np.ndarray, bboxes, scores, cls, threshold=0.8, label=0):
    results = []
    for idx, box in enumerate(bboxes):
        if cls[idx] == label and scores[idx] > threshold:
            box = list(map(int, box))
            x_min, y_min, x_max, y_max = box
            results.append(image[y_min:y_max, x_min:x_max])
    return results


class SignatureDetection:
    model = load_model()
    def predict(self, image: np.ndarray):
        results = self.model(image)[0].cpu()  # predict on an image
        bboxes = results.boxes.xyxy.numpy()
        cls = results.boxes.cls.numpy()
        scores = results.boxes.conf.numpy()
        return bboxes, cls, scores


if __name__ == '__main__':
    image = cv2.imread('Sig 00001.jpg')
    detector = SignatureDetection()
    boxes, classes, scores = detector.predict(image)
    results = get_signature(image, boxes, scores, classes)
    cv2.imshow('frame', results[0])
    cv2.waitKey(0)

from modules.signature_verification.signature_segmentation import SignatureSegmentation
from modules.signature_verification.signature_detection import SignatureDetection, get_signature
from modules.signature_verification.signature_extraction import SignatureExtraction
import cv2
import numpy as np
import pickle
from config import config
from sklearn.metrics.pairwise import cosine_similarity
import os


def load_faiss_data():
    with open(config.FAISS_EMBEDDING, 'rb') as f:
        faiss_embeddings = pickle.load(f)
    with open(config.LABELS, 'rb') as f:
        labels = pickle.load(f)
    with open(config.EMBEDDING, 'rb') as f:
        embeddings = pickle.load(f)
    with open(config.IMAGE_PATH, 'rb') as f:
        image_paths = pickle.load(f)
    return faiss_embeddings, labels, embeddings,image_paths


class SignatureVerification:
    signature_detection = SignatureDetection()
    signature_segmentation = SignatureSegmentation()
    signature_extractor = SignatureExtraction()

    faiss_embeddings, labels, embeddings,image_paths = load_faiss_data()

    def signature_digitalized(self, image: np.ndarray):
        boxes, classes, scores = self.signature_detection.predict(image)
        signatures = get_signature(image, boxes, scores, classes)
        features = []
        for i, signature in enumerate(signatures):
            signature_clean = self.signature_segmentation.predict(signature)
            signatures[i] = signature_clean
            feature = self.signature_extractor.extract_feature(signature_clean)
            features.append(feature)
        return signatures, features

    def save_faiss_data(self):
        with open(config.FAISS_EMBEDDING, 'wb') as f:
            pickle.dump(self.faiss_embeddings, f)
        with open(config.LABELS, 'wb') as f:
            pickle.dump(self.labels, f)
        with open(config.EMBEDDING, 'wb') as f:
            pickle.dump(self.embeddings, f)
        with open(config.IMAGE_PATH, 'wb') as f:
            pickle.dump(self.image_paths, f)

    def verify(self, features):
        results_search, similarity_rates = self.search(features)
        result = []
        if len(results_search) > 0:
            for idx, rate in enumerate(similarity_rates):
                if rate == 1.0:
                    result.append({"status": "chữ ký dập", "idx": results_search[idx], "rate": rate})
                else:
                    result.append({"status": "chữ ký khớp", "idx": results_search[idx], "rate": rate})
        else:
            result.append({"status": "chữ ký không khớp", "idx": None, "rate": None})
        return result

    def search(self, features):
        duplicate_signature = []
        similarity_rates = []
        for feature in features:
            dists, indexes = self.faiss_embeddings.search(feature, k=10)
            for index in indexes[0]:
                if index > -1:
                    rate = cosine_similarity(self.embeddings[index], feature)[0][0]
                    if rate > config.THRESHOLD_SIMILARITY:
                        duplicate_signature.append(index)
                        similarity_rates.append(rate)
        final_duplicate,final_rates = [],[]
        for idx,dup in enumerate(duplicate_signature):
            if dup not in final_duplicate:
                final_duplicate.append(dup)
                final_rates.append(similarity_rates[idx])
        return final_duplicate, final_rates

    def save_to_database(self, name, signatures, features):
        if not os.path.exists('data_signature/' + name):
            os.mkdir('data_signature/' + name)
        for idx, feature in enumerate(features):
            self.labels.append(name)
            self.faiss_embeddings.add(feature)
            self.embeddings.append(feature)
            image_path ='data_signature/' + name + '/' + str(idx) + '.png' 
            self.image_paths.append(image_path)
            cv2.imwrite(image_path, signatures[idx])
        self.save_faiss_data()




import xgboost as xgb
from config import config
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from unidecode import unidecode
from sklearn.metrics import confusion_matrix, accuracy_score
import xgboost as xgb
import pandas as pd
import modules.name_classifier.filter_exception as filter


def preprocessing(real_x):
    data_train = pd.read_csv(config.path_data_train)
    x_train = data_train["name"]
    tfidf_vect_ngram_char = TfidfVectorizer(
        analyzer='char', max_features=30000, ngram_range=(2, 3))
    tfidf_vect_ngram_char.fit(x_train)
    real_tfidf_ngram_char = tfidf_vect_ngram_char.transform(real_x)
    return real_tfidf_ngram_char


class NameClassifier:
    model = xgb.XGBRFClassifier()
    model.load_model(config.model_name_classifier)

    def predict_to_csv(self, id, real_x, file_path_export):
        youden_threshold = 0.2

        real_tfidf_ngram_char = preprocessing(real_x)

        real_predictions_proba = self.model.predict_proba(
            real_tfidf_ngram_char)

        real_predictions_proba_youden = (
            real_predictions_proba > youden_threshold).astype(int)

        real_predictions_proba_youden = real_predictions_proba_youden[:, 1]

        columns = ["id", "name",  "ket qua du doan"]

        results = pd.DataFrame([id, real_x,  real_predictions_proba_youden])

        results = results.transpose()

        results.columns = columns

        results.to_csv(file_path_export)

        return file_path_export

    def predict_to_file(self, file_path):
        MAKH = 'MAKH'
        NAME = 'name'
        real_data = pd.read_excel(file_path)
        full_name = []
        ids = []
        for i, id in enumerate(real_data[MAKH]):
            tenkh = str(real_data[NAME][i])
            # tenkh= real_data[NAME][i]
            if filter.has_special_char(tenkh):
                real_data[NAME][i] = 'noname'
                full_name.append(tenkh)
                ids.append(id)
            else:
                try:
                    full_name.append(unidecode(tenkh).lower())
                    ids.append(id)
                except:
                    real_data[NAME][i] = 'noname'
                    full_name.append(tenkh)
                    ids.append(id)
        real_data = pd.DataFrame([ids, full_name])
        real_data = real_data.transpose()
        real_data.columns = [MAKH, NAME]
        real_x = real_data[NAME]
        file_name_export = file_path.split('/')[-1].split('.')[0]
        file_path_export = f"data/name_classifier/export/{file_name_export}.csv"
        self.predict_to_csv(ids, real_x, file_path_export)
        return file_path_export

    def predict(self, file_path):
        file_export = self.predict_to_file(file_path)
        # Check rule-based
        data = pd.read_csv(file_export)
        new_pred = []
        for i in range(len(data)):
            new_pred.append(data['ket qua du doan'][i])
            ten_kh = str(data['name'][i]).lower()
            if filter.has_over_2number(ten_kh) or filter.has_is_full_number(ten_kh) or filter.loc_tapmo_one_word(ten_kh) or filter.loc_tapmo_mutil_word(ten_kh):
                new_pred[i] = 'tap mo'
                if filter.loc_ngoai_le_ca_nhan_one_word(ten_kh) or filter.loc_ngoai_le_ca_nhan_mutil_word(ten_kh):
                    new_pred[i] = 1
                if filter.check_person_name(ten_kh):
                    new_pred[i] = 1
                if filter.loc_khtc2(ten_kh) or filter.loc_khtc1(ten_kh):
                    new_pred[i] = 0
            if data['ket qua du doan'][i] == 0:
                if filter.loc_ngoai_le_ca_nhan_one_word(ten_kh) or filter.loc_ngoai_le_ca_nhan_mutil_word(ten_kh):
                    new_pred[i] = 1
                if filter.check_person_name(ten_kh):
                    new_pred[i] = 1
            if data['ket qua du doan'][i] == 1:
                if filter.loc_khtc2(ten_kh) or filter.loc_khtc1(ten_kh):
                    new_pred[i] = 0
            if filter.loc_ngoai_le_one_word(ten_kh) or filter.loc_ngoai_le_mutil_word(ten_kh):
                new_pred[i] = 'ngoai le'
                if filter.loc_ngoai_le_ca_nhan_one_word(ten_kh) or filter.loc_ngoai_le_ca_nhan_mutil_word(ten_kh):
                    new_pred[i] = 1
                if filter.check_person_name(ten_kh):
                    new_pred[i] = 1
                if filter.loc_khtc2(ten_kh) or filter.loc_khtc1(ten_kh):
                    new_pred[i] = 0
        predict = np.array(new_pred)
        data.insert(column='ket qua du doan new', value=predict, loc=4)
        data.to_csv(file_export)

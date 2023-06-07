from modules.check_spelling.modules.predictor import Predictor
from config import config
import pandas as pd
import numpy as np
class SpellingChecker:
    predictor = Predictor(weight_path=config.model_spelling)
    def auto_correct(self,file_path):
        file_name = file_path.split('/')[-1]
        df = pd.read_excel(file_path)
        names = df['NAME']
        np_name = names.to_numpy()
        result = []
        for i,name in enumerate(np_name):
            result.append(self.predictor.spelling_correct(name))
        df['CORECT'] = np.array(result)
        file_export = f"data/spelling_checker/export/{file_name}"
        df.to_excel(file_export)
        return file_export
# ignore warnings
import warnings
warnings.filterwarnings("ignore")

import sys
import datetime
import json
import os
import pandas as pd
import numpy as np
import pickle

from konlpy.tag import Okt
from scipy.sparse import csr_matrix

model_path = "ml/models/model_0704.pickle"

with open(model_path, 'rb') as file:
    load_tfidfvect = pickle.load(file)
    load_model =  pickle.load(file)

path_test_dataset = ""

def test_dataset(path):
    file_extension = os.path.splitext(path)[1]

    if (file_extension == ".txt"):
        test_data_file = open(path, 'r', encoding='utf-8')

        test_data_list = []

        for line in test_data_file.readlines():
            test_data_list.append(line.rstrip())

        test_data_file.close()

        test_data = pd.DataFrame(test_data_list, columns=['PRDLST_NM'])

    elif (file_extension == ".json"):
        with open(path, 'r',encoding="UTF-8") as f:
            json_file = json.loads(f.read())
        
        test_data = pd.DataFrame(json_file)
    else :
        print("Error : input data must be \'.txt\' or \'.json\'")

    #df_head_list = pd.DataFrame.columns.values.tolist()
    #df_head0 = df_head_list[0]
    jvm_path = "/Library/Java/JavaVirtualMachines/zulu-15.jdk/Contents/Home/bin/java"
    okt = Okt(jvmpath=jvm_path)

    test_data = test_data.assign(PRDLST_CORPUS = np.nan)

    for i in range(0, len(test_data)):
        PRDLST_NM = okt.morphs(test_data["PRDLST_NM"][i]) # morphs 형태소 추출
        test_data['PRDLST_CORPUS'][i] = " ".join(PRDLST_NM)

    return test_data

def testData_return_dtm(tfidfvect, data):
    corpus = data["PRDLST_CORPUS"]

    test_dtm = tfidfvect.transform(corpus)

    # scipy.sparse.csr.csr_matrix -> numpy.array
    test_dtm = csr_matrix.toarray(test_dtm)

    return test_dtm

def predict(path, tfidfvect, model):
    predict_data = test_dataset(path)
    predict_dtm = testData_return_dtm(tfidfvect, predict_data)

    X_test = np.array(predict_dtm)

    y_predict = model.predict(X_test)

    return y_predict

def y_predict_save(y_predict):
    now = datetime.datetime.now().strftime("%y%m%d_%H%M%S")

    # predict_file_path = './dataset/predict_data/predict_list('+ now + ').json'
    predict_file_path = 'ml/dataset/predict_data/predict_list(*).json'

    data = {}
    data['item_list'] = []
    for i in range(0, len(y_predict)):
        data['item_list'].append({
            "item_id" : i,
            "item_name" : y_predict[i]
        })

    with open(predict_file_path, "w", encoding="UTF-8") as f:
        json.dump(data, f, indent=4, ensure_ascii = False)

def main():
    if len(sys.argv) != 2:
        print("Please run with args: $ python example.py /path/to/dataset")
    path_test_dataset = sys.argv[1]

    
    tfidfvect = load_tfidfvect
    model = load_model

    #예측
    y_predict = predict(path_test_dataset, tfidfvect, model)

    #예측값 저장
    y_predict_save(y_predict)
    
    print(y_predict)

if __name__ == "__main__":
    main()
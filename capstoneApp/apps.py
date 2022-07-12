from django.apps import AppConfig
import os
import pickle
from django.conf import settings
import subprocess


class CapstoneappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'capstoneApp'
'''
class ApiConfig(AppConfig):
    name = 'capstoneApp'
    MODEL_FILE = os.path.join(settings.MODELS, "model0701.pickle")
    # model = pickle.load(MODEL_FILE)
with open(MODEL_FILE, "rb") as f:
        pl = pickle.load(f)
    print(pl)

    subprocess.run('python ml/predict_0704.py ml/dataset/testdata/*.json', shell=True)
'''
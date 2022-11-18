# coding:UTF-8
from numpy import ndarray

from comparison.ScenarioDivision import ScenarioDivision
import tensorflow as tf
from tensorflow.python.keras.models import Sequential
from util.ManDist import ManDist
import os
from util.FileHelper import FileHelper


class LSTMBasedScenarioDivision(ScenarioDivision):
    def __init__(self, device, different_rate_threshold=0.5):
        super().__init__(device, different_rate_threshold)
        model_file = FileHelper.join('models', 'SiameseLSTM.h5')
        model = tf.keras.models.load_model(model_file, custom_objects={'ManDist': ManDist})
        model.summary()
        x = Sequential()
        x.add(model.get_layer('lstm'))
        self.intermediate_model = x

    def predict(self, vector: ndarray) -> ndarray:
        return self.intermediate_model.predict(vector)


if __name__ == '__main__':
    model_file = FileHelper.join('models', 'SiameseLSTM.h5')
    model = tf.keras.models.load_model(model_file, custom_objects={'ManDist': ManDist})

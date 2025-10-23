import os
import numpy as np
import tensorflow as tf
import tensorflow_datasets as tfds
from PIL import Image

IMG_SIZE = 224

class FlowerInfer:
    def __init__(self, model_path="saved_model/flowers_mnv2"):
        self.model = tf.keras.models.load_model(model_path)
        # классы в том порядке, как в tf_flowers
        info = tfds.builder("tf_flowers").info
        self.class_names = [str(n) for n in info.features["label"].names]

    def _prep(self, img: Image.Image):
        img = img.convert("RGB").resize((IMG_SIZE, IMG_SIZE))
        arr = tf.keras.applications.mobilenet_v2.preprocess_input(np.array(img, dtype=np.float32))
        return np.expand_dims(arr, 0)

    def predict(self, img: Image.Image, topk=3):
        x = self._prep(img)
        probs = self.model.predict(x, verbose=0)[0]
        idx = np.argsort(probs)[::-1][:topk]
        return [(self.class_names[i], float(probs[i])) for i in idx]

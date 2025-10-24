import os
import numpy as np
import tensorflow as tf
import tensorflow_datasets as tfds
from PIL import Image

IMG_SIZE = 224
MODEL_DIR = "saved_model"
KERAS_PATH = os.path.join(MODEL_DIR, "flowers_mnv2.keras")
H5_PATH = os.path.join(MODEL_DIR, "flowers_mnv2.h5")
LEGACY_DIR = os.path.join(MODEL_DIR, "flowers_mnv2")


class FlowerInfer:
    def __init__(self, model_path: str = None):
        # приоритет: .keras → .h5 → legacy SavedModel
        path = (
            model_path
            or (KERAS_PATH if os.path.exists(KERAS_PATH)
                else (H5_PATH if os.path.exists(H5_PATH) else LEGACY_DIR))
        )

        if path.endswith(".keras") or path.endswith(".h5"):
            # современный формат Keras v3 или h5
            self.model = tf.keras.models.load_model(path)
        elif os.path.isdir(path):
            # старый SavedModel (не поддерживается Keras 3)
            raise RuntimeError(
                "Обнаружен legacy SavedModel каталог.\n"
                "Пересохраните модель в формате `.keras` "
                "(см. model/train.py и запустите `make train`)."
            )
        else:
            # модели нет вообще
            raise FileNotFoundError(
                "Модель не найдена.\n"
                "Сначала обучите её (`make train`) — "
                "файл появится: saved_model/flowers_mnv2.keras"
            )

        # загрузим имена классов
        info = tfds.builder("tf_flowers").info
        self.class_names = [str(n) for n in info.features["label"].names]

    def _prep(self, img: Image.Image):
        img = img.convert("RGB").resize((IMG_SIZE, IMG_SIZE))
        arr = tf.keras.applications.mobilenet_v2.preprocess_input(
            np.array(img, dtype=np.float32)
        )
        return np.expand_dims(arr, 0)

    def predict(self, img: Image.Image, topk=3):
        x = self._prep(img)
        probs = self.model.predict(x, verbose=0)[0]
        idx = np.argsort(probs)[::-1][:topk]
        return [(self.class_names[i], float(probs[i])) for i in idx]

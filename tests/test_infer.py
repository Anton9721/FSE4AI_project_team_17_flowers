from PIL import Image
import numpy as np
import os
import pytest

from model.infer import FlowerInfer

@pytest.mark.skipif(
    not os.path.exists("saved_model/flowers_mnv2.keras"),
    reason="Model not trained yet"
)
def test_inference_topk_output():
    infer = FlowerInfer("saved_model/flowers_mnv2.keras")
    # создаём искусственную картинку
    img = Image.fromarray((np.random.rand(224, 224, 3) * 255).astype("uint8"))
    preds = infer.predict(img, topk=3)

    # проверяем формат
    assert isinstance(preds, list)
    assert len(preds) == 3
    assert all(isinstance(name, str) and isinstance(prob, float) for name, prob in preds)
    assert all(0.0 <= prob <= 1.0 for _, prob in preds)

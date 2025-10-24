from app.app import load_infer
from model.infer import FlowerInfer

def test_load_infer_returns_flower_infer():
    infer = load_infer()
    assert isinstance(infer, FlowerInfer)
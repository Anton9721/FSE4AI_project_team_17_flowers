import importlib

def test_import_app_and_model():
    # проверяем, что пакеты устанавливаются и импортируются
    assert importlib.import_module("app.app")
    assert importlib.import_module("model.infer")

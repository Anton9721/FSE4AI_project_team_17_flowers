import os

def test_project_structure():
    assert os.path.exists("model/train.py")
    assert os.path.exists("app/app.py")
    assert os.path.exists("pyproject.toml")

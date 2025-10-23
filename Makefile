.PHONY: setup train test run docker-build docker-run clean help

ifeq ($(OS),Windows_NT)
  PY   := .venv\Scripts\python.exe
  PIP  := .venv\Scripts\pip.exe
  ST   := .venv\Scripts\streamlit.exe
else
  PY   := .venv/bin/python
  PIP  := .venv/bin/pip
  ST   := .venv/bin/streamlit
endif

PORT ?= 8501
EPOCHS ?= 3
FTEPOCHS ?= 2

APP_PATH   := app/app.py
TRAIN_PATH := model/train.py

help:
	@echo "Targets: setup | train | test | run | docker-build | docker-run | clean"

setup:
	python -m venv .venv
	$(PY) -m pip install -U pip
	$(PIP) install -e .

train:
	$(PY) $(TRAIN_PATH) --epochs $(EPOCHS) --finetune-epochs $(FTEPOCHS)

test:
	$(PY) -m pytest -q

run:
	$(ST) run $(APP_PATH) --server.port=$(PORT)

docker-build:
	docker build -t flowers:latest .

docker-run:
	docker run -p $(PORT):8501 flowers:latest

clean:
	-$(PY) -c "import shutil; shutil.rmtree('.venv', ignore_errors=True)"

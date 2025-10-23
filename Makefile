# --- Cross-platform Makefile (Windows / Linux / macOS / WSL) ---

.PHONY: setup train test run docker-build docker-run clean help

# Detect platform and set tool paths
ifeq ($(OS),Windows_NT)
  PY   := .venv\Scripts\python.exe
  PIP  := .venv\Scripts\pip.exe
  ST   := .venv\Scripts\streamlit.exe
  SEP  := \ 
else
  PY   := .venv/bin/python
  PIP  := .venv/bin/pip
  ST   := .venv/bin/streamlit
  SEP  := / 
endif

PORT ?= 8501
EPOCHS ?= 3
FTEPOCHS ?= 2

help:
	@echo "Targets:"
	@echo "  setup         - create venv and install project (editable)"
	@echo "  train         - train model"
	@echo "  test          - run pytest"
	@echo "  run           - run Streamlit app"
	@echo "  docker-build  - build Docker image"
	@echo "  docker-run    - run Docker container"
	@echo "  clean         - remove .venv"

setup:
	python -m venv .venv
	$(PY) -m pip install -U pip
	$(PIP) install -e .

train:
	$(PY) model$(SEP)train.py --epochs $(EPOCHS) --finetune-epochs $(FTEPOCHS)

test:
	$(PY) -m pytest -q

run:
	$(ST) run app$(SEP)app.py --server.port=$(PORT)

docker-build:
	docker build -t flowers:latest .

docker-run:
	docker run -p $(PORT):8501 flowers:latest

clean:
	-$(PY) -c "import shutil; shutil.rmtree('.venv', ignore_errors=True)"

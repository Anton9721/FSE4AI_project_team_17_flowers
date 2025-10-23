.PHONY: setup train test run docker-build docker-run

setup:
\tpython -m venv .venv && . .venv/bin/activate && pip install -U pip && pip install -e .

train:
\tpython model/train.py --epochs 3 --finetune-epochs 2

test:
\tpytest

run:
\tstreamlit run app/app.py

docker-build:
\tdocker build -t flowers:latest .

docker-run:
\tdocker run -p 8501:8501 flowers:latest

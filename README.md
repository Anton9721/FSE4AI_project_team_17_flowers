# Flower Classifier 

Простой проект: классификация цветов (tf_flowers) с MobileNetV2 + Streamlit.

## Запуск локально
```bash
make setup
make train   # обучит и сохранит model в saved_model/flowers_mnv2
make run     # http://localhost:8501

# Testing & CI

- Testing framework: **pytest**
- Continuous Integration: **GitHub Actions**
- All tests automatically run on each push and pull request.
- Current status: ![CI](https://github.com/<username>/flowers-classifier/actions/workflows/ci.yml/badge.svg)

### Local run
```bash
pytest -v


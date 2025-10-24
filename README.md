# Flower Classification Demo (Team Project)

This project is a **team machine learning application** for flower image classification using **TensorFlow (MobileNetV2)** and **Streamlit** for interactive visualization.  
The model is trained on the **TensorFlow Flowers** dataset and deployed as a simple web app.

---

## Team Roles

- **Participant A** — Model development and training  
  - Implemented `model/train.py`
  - Trained the MobileNetV2 classifier and saved it as `.keras`
  - Wrote unit tests for model loading and inference.

- **Participant B** — Testing and Continuous Integration  
  - Added smoke tests for both the app and the model using `pytest`
  - Configured GitHub Actions CI for automated testing on each push/PR
  - Ensured reproducibility and dependency consistency.

- **Participant C (Anton9721)** — Infrastructure & Deployment  
  - Built cross-platform `Makefile` for Linux/Windows
  - Created Dockerfile and container deployment setup
  - Maintained overall project structure and documentation.

---

## Model Overview

The classifier is based on **MobileNetV2**, pre-trained on ImageNet and fine-tuned on the `tf_flowers` dataset.

- **Input:** RGB image, resized to 224×224  
- **Output:** One of five flower classes  
- **Framework:** TensorFlow / Keras 3  
- **Saved format:** `.keras` (for Keras 3 compatibility)

Model training script: `model/train.py`  
Model inference wrapper: `model/infer.py`  
Streamlit UI app: `app/app.py`

---

## Project Structure

├── app/
│ └── app.py # Streamlit interface
├── model/
│ ├── train.py # Model training
│ └── infer.py # Inference utilities
├── tests/
│ ├── test_app_smoke.py
│ └── test_imports.py
├── saved_model/ # Folder for trained model (flowers_mnv2.keras)
├── Dockerfile # Docker image definition
├── Makefile # Cross-platform build automation
├── pyproject.toml # Dependencies and build config
└── README.md


---

## Local Development

```bash
# Create virtual environment and install dependencies
make setup

# Train the model (saves to saved_model/flowers_mnv2.keras)
make train

# Run tests
make test

# Launch Streamlit app
make run
# Open http://localhost:8501

```


## Testing & CI

Testing framework: pytest

Continuous Integration: GitHub Actions

Tests automatically run on every push and pull request.

To run locally:

```bash
pytest -v
```

## Docker Deployment

You can run the full app inside a Docker container.
This allows anyone to reproduce the environment regardless of OS.

1️⃣ Build the image

```bash
docker build -t flowers:latest .
```

2️⃣ Run the container

If you already have a trained model:

```bash
docker run -d \
  -p 8501:8501 \
  -v "$PWD/saved_model:/app/saved_model" \
  --name flowers_app \
  flowers:latest
```


Then open http://localhost:8501
 in your browser.

3️⃣ (Optional) Train inside the container

If you prefer to train inside Docker:

```bash
docker run -it \
  -v "$PWD:/app" \
  flowers:latest \
  bash -c "python model/train.py --epochs 3 --finetune-epochs 2"
```

## Environment Summary
Component	Version
Python	3.11
TensorFlow	≥ 2.14
Streamlit	Latest
OS	Cross-platform (Linux/Windows via Makefile)

## Future Improvements

Add automatic model download on first launch

Implement cloud deployment (Streamlit Cloud / DockerHub)

Extend dataset with user-uploaded images

Introduce CI/CD workflow for Docker publishing




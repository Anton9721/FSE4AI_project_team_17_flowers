import streamlit as st
from PIL import Image

# Важно: импортируем FlowerInfer, но НЕ создаём его на верхнем уровне
from model.infer import FlowerInfer

st.set_page_config(page_title="Flower Classifier", page_icon="🌸")
st.title("🌸 Flower Classifier (MobileNetV2)")
st.write("Загрузите фото цветка — получите топ-3 класса с вероятностями.")

def get_infer():
    # Ленивая и кэшируемая загрузка модели: не мешает pytest импортам
    if "infer" not in st.session_state:
        try:
            st.session_state.infer = FlowerInfer()
        except Exception as e:
            st.error(
                "Модель не найдена или несовместима с Keras 3.\n\n"
                "👉 Переобучите и сохраните модель в формате `.keras` "
                "(см. README / model/train.py)."
            )
            st.stop()
    return st.session_state.infer

uploaded = st.file_uploader("Выберите изображение", type=["jpg", "jpeg", "png"])

if uploaded:
    infer = get_infer()
    img = Image.open(uploaded).convert("RGB")
    st.image(img, caption="Входное изображение", use_container_width=True)
    preds = infer.predict(img, topk=3)
    st.subheader("Результаты:")
    for name, p in preds:
        st.write(f"- **{name}** — {p:.2%}")

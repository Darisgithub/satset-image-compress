import streamlit as st
import numpy as np
from PIL import Image

st.title("SVD Image Compression")

uploaded_file = st.file_uploader("Upload Image")

if uploaded_file is not None:

    image = Image.open(uploaded_file).convert("L")

    img_array = np.array(image)

    st.subheader("Original Image")
    st.image(img_array)

    U, S, VT = np.linalg.svd(img_array)

    k = st.slider("Select Rank", 1, 100, 20)

    compressed = U[:, :k] @ np.diag(S[:k]) @ VT[:k, :]

    # FIX ERROR
    compressed = np.clip(compressed, 0, 255)
    compressed = compressed.astype(np.uint8)

    st.subheader("Compressed Image")
    st.image(compressed)
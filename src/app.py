import sys
from pathlib import Path
import importlib.util

sys.path.insert(0, str(Path(__file__).parent))

# Load compression module explicitly
spec = importlib.util.spec_from_file_location("compression", Path(__file__).parent / "compression.py")
compression = importlib.util.module_from_spec(spec)
spec.loader.exec_module(compression)

import streamlit as st
from PIL import Image

compress_image = compression.compress_image

st.set_page_config(layout="wide")
st.title("SVD Image Compression")

uploaded_file = st.file_uploader("Upload Image")

if uploaded_file:
    image = Image.open(uploaded_file)
    
    # Keep RGB/color if available, else convert
    if image.mode not in ['RGB', 'L']:
        image = image.convert('RGB')
    
    # Get optimal rank based on image dimensions
    max_rank = min(image.size)
    
    # Create columns for image and info
    col_slider = st.columns(1)[0]
    with col_slider:
        k = st.slider("Select Rank", 1, max_rank, min(80, max_rank // 2))
    
    compressed = compress_image(image, k)
    
    # Main display with 3 columns: image, image, info
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        st.subheader("Original Image")
        st.image(image, width=500)
    
    with col2:
        st.subheader("Compressed Image")
        st.image(compressed, width=500)
    
    with col3:
        st.subheader("Info")
        
        # Image dimensions
        width, height = image.size
        st.metric("Dimensions", f"{width} × {height}")
        
        # Number of pixels
        total_pixels = width * height
        st.metric("Total Pixels", f"{total_pixels:,}")
        
        # Channels
        if image.mode == 'RGB':
            channels = 3
        else:
            channels = 1
        st.metric("Channels", channels)
        
        # Original size (estimated)
        original_size_bytes = total_pixels * channels
        st.metric("Original Size", f"{original_size_bytes / 1024:.1f} KB")
        
        # Compressed size
        compressed_size_bytes = k * (width + height + 1) * channels
        st.metric("Compressed Size", f"{compressed_size_bytes / 1024:.1f} KB")
        
        # Compression ratio
        compression_ratio = (compressed_size_bytes / original_size_bytes) * 100
        st.metric("Compression Ratio", f"{compression_ratio:.1f}%")
        
        # Rank
        st.metric("Rank (k)", k)
import sys
from pathlib import Path
import importlib.util
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))

# Load compression module explicitly
spec = importlib.util.spec_from_file_location("compression", Path(__file__).parent / "compression.py")
compression = importlib.util.module_from_spec(spec)
spec.loader.exec_module(compression)

import streamlit as st
from PIL import Image
import os

compress_image = compression.compress_image

# Configure page
st.set_page_config(
    page_title="SVD Image Compression",
    page_icon="🖼️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for modern minimalist design
st.markdown("""
    <style>
        * {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
        }
        .main {
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        }
        h1 {
            text-align: center;
            color: #1a202c;
            font-weight: 600;
            margin-bottom: 1rem;
            letter-spacing: -0.5px;
        }
        h2 {
            color: #2d3748;
            font-weight: 500;
            font-size: 1.1rem;
        }
        .info-box {
            background: white;
            border-radius: 12px;
            padding: 1.5rem;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            border: 1px solid #e2e8f0;
        }
        .metric-label {
            color: #718096;
            font-size: 0.875rem;
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 0.5rem;
        }
        .metric-value {
            color: #1a202c;
            font-size: 1.5rem;
            font-weight: 600;
        }
        .button-container {
            display: flex;
            gap: 1rem;
            margin-top: 1.5rem;
            flex-wrap: wrap;
        }
        [data-testid="stButton"] > button {
            width: 100%;
            border-radius: 8px;
            border: none;
            font-weight: 500;
            padding: 0.75rem 1.5rem;
            transition: all 0.2s ease;
        }
        [data-testid="stButton"] > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }
        .slider-container {
            background: white;
            padding: 1.5rem;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            margin-bottom: 1.5rem;
        }
        .uploader-container {
            background: white;
            padding: 2rem;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            text-align: center;
            margin-bottom: 1.5rem;
            border: 2px dashed #cbd5e0;
        }
        .success-message {
            background: #f0fff4;
            border-left: 4px solid #48bb78;
            padding: 1rem;
            border-radius: 6px;
            color: #22543d;
        }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown("<h1>🖼️ SVD Image Compression</h1>", unsafe_allow_html=True)

# Create output folder if not exists
output_folder = Path(__file__).parent.parent / "output"
output_folder.mkdir(exist_ok=True)

# File uploader
st.markdown('<div class="uploader-container">', unsafe_allow_html=True)
uploaded_file = st.file_uploader("📤 Choose an image", type=['jpg', 'jpeg', 'png', 'bmp', 'gif', 'webp'])
st.markdown('</div>', unsafe_allow_html=True)

if uploaded_file:
    image = Image.open(uploaded_file)
    
    # Keep RGB/color if available, else convert
    if image.mode not in ['RGB', 'L']:
        image = image.convert('RGB')
    
    # Get optimal rank based on image dimensions
    max_rank = min(image.size)
    
    # Slider in container
    st.markdown('<div class="slider-container">', unsafe_allow_html=True)
    st.markdown("### Compression Level")
    k = st.slider("Select Rank (k)", 1, max_rank, min(80, max_rank // 2), label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Compress image
    with st.spinner("🔄 Compressing image..."):
        compressed = compress_image(image, k)
    compressed_image = Image.fromarray(compressed)
    
    # Display images and info
    col1, col2, col3 = st.columns([1.8, 1.8, 1], gap="medium")
    
    with col1:
        st.markdown("<h2>📸 Original Image</h2>", unsafe_allow_html=True)
        st.image(image, use_column_width=True)
    
    with col2:
        st.markdown("<h2>✨ Compressed Image</h2>", unsafe_allow_html=True)
        st.image(compressed_image, use_column_width=True)
    
    with col3:
        st.markdown("<h2>📊 Statistics</h2>", unsafe_allow_html=True)
        st.markdown('<div class="info-box">', unsafe_allow_html=True)
        
        # Image dimensions
        width, height = image.size
        st.markdown(f'<div class="metric-label">Dimensions</div><div class="metric-value">{width} × {height}</div>', unsafe_allow_html=True)
        
        # Number of pixels
        total_pixels = width * height
        st.markdown(f'<div class="metric-label">Pixels</div><div class="metric-value">{total_pixels:,}</div>', unsafe_allow_html=True)
        
        # Channels
        if image.mode == 'RGB':
            channels = 3
        else:
            channels = 1
        st.markdown(f'<div class="metric-label">Channels</div><div class="metric-value">{channels}</div>', unsafe_allow_html=True)
        
        # Original size (estimated)
        original_size_bytes = total_pixels * channels
        st.markdown(f'<div class="metric-label">Original Size</div><div class="metric-value">{original_size_bytes / 1024:.1f} KB</div>', unsafe_allow_html=True)
        
        # Compressed size
        compressed_size_bytes = k * (width + height + 1) * channels
        st.markdown(f'<div class="metric-label">Compressed Size</div><div class="metric-value">{compressed_size_bytes / 1024:.1f} KB</div>', unsafe_allow_html=True)
        
        # Compression ratio
        compression_ratio = (compressed_size_bytes / original_size_bytes) * 100
        st.markdown(f'<div class="metric-label">Ratio</div><div class="metric-value">{compression_ratio:.1f}%</div>', unsafe_allow_html=True)
        
        # Rank
        st.markdown(f'<div class="metric-label">Rank (k)</div><div class="metric-value">{k}</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Save buttons
    st.markdown("---")
    col_save1, col_save2, col_save3 = st.columns(3)
    
    with col_save1:
        if st.button("💾 Save Compressed Image", use_container_width=True):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"compressed_{timestamp}.png"
            filepath = output_folder / filename
            compressed_image.save(filepath)
            st.markdown(f'<div class="success-message">✅ Saved: {filename}</div>', unsafe_allow_html=True)
    
    with col_save2:
        if st.button("💾 Save Original Image", use_container_width=True):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"original_{timestamp}.png"
            filepath = output_folder / filename
            image.save(filepath)
            st.markdown(f'<div class="success-message">✅ Saved: {filename}</div>', unsafe_allow_html=True)
    
    with col_save3:
        # Download button
        png_image = compressed_image
        png_bytes = st.download_button(
            label="⬇️ Download Compressed",
            data=open(output_folder / f"temp_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png", "rb") if False else None,
            file_name=f"compressed_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png",
            mime="image/png",
            use_container_width=True
        ) if False else None
        
        # Alternative download button
        import io
        buffer = io.BytesIO()
        png_image.save(buffer, format="PNG")
        buffer.seek(0)
        st.download_button(
            label="⬇️ Download Compressed",
            data=buffer.getvalue(),
            file_name=f"compressed_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png",
            mime="image/png",
            use_container_width=True
        )
    
    # Show output folder info
    st.markdown("---")
    st.info(f"📁 Images saved to: `{output_folder}`")
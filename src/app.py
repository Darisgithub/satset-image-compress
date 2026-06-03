import sys
import io
import numpy as np
import importlib.util

from pathlib import Path

import streamlit as st
from PIL import Image

try:
    from streamlit_image_comparison import image_comparison
except ModuleNotFoundError:
    image_comparison = None

# Import UI components
from ui.styles import load_styles
from ui.header import render_header
from ui.controls import render_controls, get_default_k, render_compression_rank_slider, render_compress_button
from ui.comparison import render_comparison_section, render_interactive_comparison
from ui.metrics import render_metrics_section, calculate_metrics
from ui.download import render_download_section
from ui.footer import render_footer
from ui.visualization import render_analysis_section


# =========================================================
# CONFIGURATION
# =========================================================
BASE_DIR = Path(__file__).parent
OUTPUT_DIR = BASE_DIR.parent / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

# Configure Streamlit
st.set_page_config(
    page_title="LAB SATSET IMAGE COMPRESS",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Load compression module
sys.path.insert(0, str(BASE_DIR))
spec = importlib.util.spec_from_file_location(
    "compression",
    BASE_DIR / "compression.py"
)
compression = importlib.util.module_from_spec(spec)
spec.loader.exec_module(compression)
compress_image = compression.compress_image
compress_image_with_svd_data = compression.compress_image_with_svd_data


# =========================================================
# SESSION STATE
# =========================================================
if "compressed_image" not in st.session_state:
    st.session_state.compressed_image = None
if "singular_values" not in st.session_state:
    st.session_state.singular_values = None


# =========================================================
# APP INITIALIZATION
# =========================================================
load_styles()
render_header()


# =========================================================
# MAIN APPLICATION LOGIC
# =========================================================
def main():
    """Main application flow"""
    
    # Render controls and get inputs
    uploaded_file, quality_mode, filter_mode = render_controls()
    
    if uploaded_file is None:
        return
    
    # Load and validate image
    image = Image.open(uploaded_file)
    if image.mode not in ["RGB", "L"]:
        image = image.convert("RGB")
    
    width, height = image.size
    max_rank = min(width, height)
    channels = 3 if image.mode == "RGB" else 1
    
    # Calculate default compression rank
    default_k = get_default_k(quality_mode, max_rank)
    
    # Render compression rank slider
    k = render_compression_rank_slider(max_rank, default_k)
    
    # Render compress button
    compress_button = render_compress_button()
    
    # Execute compression if button clicked
    if compress_button:
        with st.spinner("⏳ SEDANG MENGOMPRESI..."):
            compressed_array, singular_values = compress_image_with_svd_data(image, k)
            compressed_array = np.clip(compressed_array, 0, 255).astype(np.uint8)
            st.session_state.compressed_image = Image.fromarray(compressed_array)
            st.session_state.singular_values = singular_values
    
    # Get compressed image from session
    compressed_image = st.session_state.compressed_image
    
    # Display results if compression was performed
    if compressed_image is not None:
        # Optional interactive comparison
        render_interactive_comparison(image_comparison, image, compressed_image)
        
        # Calculate compressed size
        buffer = io.BytesIO()
        compressed_image.save(buffer, format="JPEG", quality=85)
        buffer.seek(0)
        compressed_size = len(buffer.getvalue())
        
        # Render comparison section
        render_comparison_section(
            image, compressed_image, k,
            width, height, channels,
            uploaded_file, compressed_size
        )
        
        # Calculate and display metrics
        saved_ratio, compression_ratio = calculate_metrics(
            uploaded_file.size, compressed_size
        )
        render_metrics_section(
            uploaded_file.size, compressed_size, k,
            saved_ratio, compression_ratio
        )
        
        # Render download section
        render_download_section(compressed_image, OUTPUT_DIR, buffer)
        
        # Render analysis section with Matplotlib visualizations
        if st.session_state.singular_values is not None:
            render_analysis_section(
                st.session_state.singular_values,
                k,
                (height, width)
            )


# =========================================================
# RUN APPLICATION
# =========================================================
if __name__ == "__main__":
    main()
    render_footer()

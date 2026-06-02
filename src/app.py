import sys
import io
import numpy as np
import importlib.util

from pathlib import Path
from datetime import datetime

import streamlit as st

from PIL import Image

try:
    from streamlit_image_comparison import image_comparison
except ModuleNotFoundError:
    image_comparison = None


# =========================================================
# LOAD COMPRESSION MODULE
# =========================================================
BASE_DIR = Path(__file__).parent

sys.path.insert(0, str(BASE_DIR))

spec = importlib.util.spec_from_file_location(
    "compression",
    BASE_DIR / "compression.py"
)

compression = importlib.util.module_from_spec(spec)

spec.loader.exec_module(compression)

compress_image = compression.compress_image


# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="SVD Image Compression",
    page_icon="🖼️",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# =========================================================
# OUTPUT DIRECTORY
# =========================================================
OUTPUT_DIR = BASE_DIR.parent / "output"

OUTPUT_DIR.mkdir(exist_ok=True)


# =========================================================
# SESSION STATE
# =========================================================
if "compressed_image" not in st.session_state:
    st.session_state.compressed_image = None


# =========================================================
# CUSTOM CSS
# =========================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&family=Inter:wght@400;500;600;700&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,400,0,0');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    color: #e2e8f0;
}

[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(circle at top left, rgba(56,189,248,0.16), transparent 22%),
        radial-gradient(circle at bottom right, rgba(168,85,247,0.16), transparent 24%),
        linear-gradient(180deg, #020617 0%, #0f172a 100%);
    background-attachment: fixed;
}

main, .block-container {
    max-width: 1360px;
    margin: 0 auto;
    padding: 3rem 1.5rem 3rem;
}

.main-title {
    font-family: 'Press Start 2P', monospace;
    text-align: center;
    font-size: 2.2rem;
    line-height: 1.2;
    letter-spacing: 0.24em;
    color: #7dd3fc;
    margin: 1.2rem 0 0.4rem;
}

.subtitle {
    font-size: 1rem;
    margin-bottom: 2rem;
}

.section-row {
    display: grid;
    grid-template-columns: 1fr 420px;
    gap: 30px;
    align-items: start;
}

.responsive-columns {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 24px;
}

@media (max-width: 920px) {
    .section-row,
    .responsive-columns {
        grid-template-columns: 1fr;
    }
}

.subtitle {
    text-align: center;
    color: #94a3b8;
    font-size: 1rem;
    margin-bottom: 2rem;
}

.upload-box,
.slider-box,
.image-box,

    background: rgba(15,23,42,0.72);
    backdrop-filter: blur(14px);
    border-radius: 22px;
    padding: 22px;
    box-shadow: 0 24px 60px rgba(15,23,42,0.28);
}

.upload-box {
    border-style: dashed;
    border-color: rgba(56,189,248,0.32);
}

.image-box {
    padding: 18px;
    overflow: hidden;
}

.image-box img,
.stImage img,
img {
    max-width: 100% !important;
    width: 100% !important;
    height: auto !important;
    object-fit: contain !important;
    display: block !important;
}

[data-testid="stImage"] {
    width: 100% !important;
}

.stButton > button,
.stDownloadButton > button {
    width: 100%;
    border: none;
    border-radius: 16px;
    background: linear-gradient(135deg, #38bdf8, #7c3aed);
    color: #eef2ff;
    font-weight: 700;
    letter-spacing: 0.05em;
    padding: 14px 18px;
    transition: transform 0.18s ease, box-shadow 0.18s ease;
}

.stButton > button:hover,
.stDownloadButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 14px 30px rgba(56,189,248,0.24);
}

.stRadio > div,
.stSelectbox > div,
.stSlider > div {
    color: #cbd5e1;
}

.card-header {
    display: flex;
    align-items: center;
    gap: 0.9rem;
    margin-bottom: 1rem;
}

.card-header .material-symbols-outlined {
    font-variation-settings: 'FILL' 0, 'wght' 700, 'GRAD' 0, 'opsz' 48;
    color: #38bdf8;
}

.filter-panel {
    display: grid;
    grid-template-columns: repeat(3, minmax(120px, 1fr));
    gap: 12px;
    margin-top: 1rem;
}

.filter-chip {
    border: 1px solid rgba(148,163,184,0.16);
    padding: 14px 16px;
    border-radius: 16px;
    background: rgba(255,255,255,0.04);
    transition: transform 0.18s ease, box-shadow 0.18s ease;
}

.filter-chip:hover {
    transform: translateY(-1px);
    box-shadow: 0 12px 24px rgba(56,189,248,0.12);
}

.stat-card {
    margin-bottom: 12px;
}

.stat-key {
    color: #94a3b8;
    font-size: 0.85rem;
    text-transform: uppercase;
    letter-spacing: 0.12em;
}

.stat-value {
    color: #e2e8f0;
    font-size: 1.1rem;
    font-weight: 700;
}

.success-box {
    padding: 16px;
    border-radius: 16px;
    background: rgba(34,197,94,0.16);
    border: 1px solid rgba(34,197,94,0.28);
    color: #bbf7d0;
    margin-top: 1rem;
}

@media (max-width: 900px) {
    .card-header {
        flex-direction: column;
        align-items: flex-start;
    }
    .filter-panel {
        grid-template-columns: 1fr;
    }
}
</style>
""", unsafe_allow_html=True)


# =========================================================
# HEADER
# =========================================================
st.markdown(
    """
    <div class="card-header">
        <span class="material-symbols-outlined">auto_fix_high</span>
        <div>
            <div class="main-title">SVD Image Compression</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# FILE UPLOADER
# =========================================================
st.markdown(
    '<div class="upload-box">',
    unsafe_allow_html=True
)

uploaded_file = st.file_uploader(
    "Upload Image",
    type=[
        "jpg",
        "jpeg",
        "png",
        "bmp",
        "webp"
    ]
)

st.markdown(
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# MAIN APP
# =========================================================
if uploaded_file:

    # =====================================================
    # LOAD IMAGE
    # =====================================================
    image = Image.open(uploaded_file)

    if image.mode not in ["RGB", "L"]:
        image = image.convert("RGB")

    width, height = image.size

    max_rank = min(width, height)


    # =====================================================
    # CONTROL PANEL
    # =====================================================
    st.markdown(
        '<div class="slider-box">',
        unsafe_allow_html=True
    )

    st.subheader("Compression Settings")


    # =====================================================
    # QUALITY PRESET
    # =====================================================
    quality_mode = st.selectbox(
        "Quality Preset",
        [
            "Low Size",
            "Balanced",
            "High Quality"
        ]
    )


    # =====================================================
    # DEFAULT K
    # =====================================================
    if quality_mode == "Low Size":

        default_k = min(20, max_rank)

    elif quality_mode == "Balanced":

        default_k = max(1, min(80, max_rank // 2))

    else:

        default_k = max(1, min(150, max_rank))


    # =====================================================
    # SLIDER
    # =====================================================
    k = st.slider(
        "Compression Rank (k)",
        min_value=1,
        max_value=max_rank,
        value=default_k
    )

    preview_mode = st.radio(
        "Preview Mode",
        ["Side-by-side", "Slider Comparison"],
        index=1,
        horizontal=True
    )

    filter_mode = st.selectbox(
        "Compression Filter Style",
        ["Standard", "Retro", "Pro"],
        help="Pilih tampilan UI dan ringkasan kompresi saat preview"
    )


    # =====================================================
    # COMPRESS BUTTON
    # =====================================================
    compress_button = st.button(
        "Compress Image",
        use_container_width=True
    )

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )


    # =====================================================
    # COMPRESS PROCESS
    # =====================================================
    if compress_button:

        with st.spinner("Compressing image..."):

            compressed_array = compress_image(
                image,
                k
            )

            # =============================================
            # FIX ARRAY TYPE
            # =============================================
            compressed_array = np.clip(
                compressed_array,
                0,
                255
            ).astype(np.uint8)

            # =============================================
            # SAVE TO SESSION
            # =============================================
            st.session_state.compressed_image = Image.fromarray(
                compressed_array
            )


    # =====================================================
    # LOAD FROM SESSION
    # =====================================================
    compressed_image = st.session_state.compressed_image


    # =====================================================
    # DISPLAY RESULT
    # =====================================================
    if compressed_image is not None:

        if image_comparison is not None and preview_mode == "Slider Comparison":
            image_comparison(
                img1=image,
                img2=compressed_image,
                label1="Original",
                label2="Compressed"
            )
        else:
            col_a, col_b = st.columns(2)
            with col_a:
                st.markdown("#### Original")
                st.markdown('<div class="image-box">', unsafe_allow_html=True)
                st.image(image, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
            with col_b:
                st.markdown("#### Compressed")
                st.markdown('<div class="image-box">', unsafe_allow_html=True)
                st.image(compressed_image, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("---")


        # =================================================
        # DISPLAY SECTION
        # =================================================
        col1, col2, col3 = st.columns(
            [2.4, 2.4, 1]
        )


        # =============================================
        # ORIGINAL IMAGE
        # =============================================
        with col1:

            st.markdown("## Original Image")

            st.markdown(
                '<div class="image-box">',
                unsafe_allow_html=True
            )

            st.image(
                image,
                use_container_width=True
            )

            st.markdown(
                '</div>',
                unsafe_allow_html=True
            )


        # =============================================
        # COMPRESSED IMAGE
        # =============================================
        with col2:

            st.markdown("## Compressed Image")

            st.markdown(
                '<div class="image-box">',
                unsafe_allow_html=True
            )

            st.image(
                compressed_image,
                use_container_width=True
            )

            st.markdown(
                '</div>',
                unsafe_allow_html=True
            )


            # =============================================
            # STATISTICS
            # =============================================
        with col3:

            st.markdown(
                '<div class="stat-card">',
                unsafe_allow_html=True
            )

            st.markdown(
                '<div class="section-header"><h3>Statistics</h3><div class="section-note">Detail ringkas ukuran & kualitas</div></div>',
                unsafe_allow_html=True
            )

            # =========================================
            # ORIGINAL FILE SIZE
            # =========================================
            original_size = uploaded_file.size

            # =========================================
            # BUFFER
            # =========================================
            buffer = io.BytesIO()

            compressed_image.save(
                buffer,
                format="JPEG",
                quality=85
            )

            compressed_size = len(buffer.getvalue())

            buffer.seek(0)


            # =========================================
            # SAVED RATIO
            # =========================================
            saved_ratio = (
                (
                    original_size
                    - compressed_size
                )
                / original_size
            ) * 100


            # =========================================
            # STATS
            # =========================================
            stats = [

                (
                    "Dimensions",
                    f"{width} × {height}"
                ),

                (
                    "Pixels",
                    f"{width * height:,}"
                ),

                (
                    "Channels",
                    "3" if image.mode == "RGB" else "1"
                ),

                (
                    "Original Size",
                    f"{original_size / 1024:.1f} KB"
                ),

                (
                    "Compressed Size",
                    f"{compressed_size / 1024:.1f} KB"
                ),

                (
                    "Saved",
                    f"{saved_ratio:.1f}%"
                ),

                (
                    "Rank (k)",
                    f"{k}"
                )
            ]


            # =========================================
            # DISPLAY STATS
            # =========================================
            for label, value in stats:
                st.markdown(
                    f'<div class="stat-item"><div class="stat-key">{label}</div><div class="stat-value">{value}</div></div>',
                    unsafe_allow_html=True
                )

            st.markdown(
                '</div>',
                unsafe_allow_html=True
            )


        # =================================================
        # DOWNLOAD SECTION
        # =================================================
        st.markdown("---")

        c1, c2 = st.columns(2)


        # =============================================
        # SAVE BUTTON
        # =============================================
        with c1:

            if st.button(
                "Save Compressed Image",
                use_container_width=True
            ):

                timestamp = datetime.now().strftime(
                    "%Y%m%d_%H%M%S"
                )

                filename = (
                    f"compressed_{timestamp}.jpg"
                )

                filepath = OUTPUT_DIR / filename

                compressed_image.save(
                    filepath,
                    format="JPEG",
                    quality=85
                )

                st.markdown(
                    f"""
                    <div class="success-box">
                        ✅ Image saved successfully
                        <br><br>
                        <b>{filename}</b>
                    </div>
                    """,
                    unsafe_allow_html=True
                )


        # =============================================
        # DOWNLOAD BUTTON
        # =============================================
        with c2:

            st.download_button(
                label="Download Compressed Image",
                data=buffer.getvalue(),
                file_name=f"compressed_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg",
                mime="image/jpeg",
                use_container_width=True
            )


        # =================================================
        # OUTPUT INFO
        # =================================================
        st.info(
            f"Output Folder: {OUTPUT_DIR}"
        )
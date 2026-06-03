import streamlit as st
import base64
from io import BytesIO
import numpy as np
from PIL import Image


def _image_to_base64(img):
    if isinstance(img, np.ndarray):
        img = Image.fromarray(img)
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()


def render_comparison_section(image, compressed_image, k, width, height, channels, uploaded_file, compressed_size):
    """Render the professional image comparison section with original and compressed images"""
    st.markdown('''
    <style>
    .comparison-section-wrapper {
        margin-bottom: 3rem;
    }

    .brutal-title {
        display: flex;
        align-items: center;
        gap: 0.8rem;
        margin-bottom: 1.5rem;
        padding-bottom: 1rem;
        border-bottom: 4px solid black;
    }

    .brutal-card-inner {
        background: white;
        border: 4px solid black;
        box-shadow: 6px 6px 0px black;
        transition: transform 0.1s ease, box-shadow 0.1s ease;
        display: flex;
        flex-direction: column;
        height: 100%;
        margin-bottom: 1.5rem;
    }

    .brutal-card-inner:hover {
        transform: translate(2px, 2px);
        box-shadow: 4px 4px 0px black;
    }

    .comparison-card-modern-header {
        background: var(--accent-pink);
        padding: 1rem;
        border-bottom: 4px solid black;
        display: flex;
        justify-content: space-between;
        align-items: center;
        color: white;
    }

    .comparison-card-modern-header.compressed {
        background: var(--accent-cyan);
        color: black;
    }

    .comparison-card-modern-title {
        font-family: 'Press Start 2P', monospace;
        font-size: 0.7rem;
        margin: 0;
        text-transform: uppercase;
        color: inherit;
    }

    .comparison-badge-modern {
        background: var(--accent-yellow);
        color: black;
        padding: 0.3rem 0.5rem;
        font-family: 'Press Start 2P', monospace;
        font-size: 0.5rem;
        border: 2px solid black;
        text-transform: uppercase;
    }

    .comparison-preview-modern {
        width: 100%;
        aspect-ratio: 3 / 2;
        background: #000;
        display: flex;
        align-items: center;
        justify-content: center;
        overflow: hidden;
        position: relative;
        padding: 1rem;
        flex: 1;
        max-height: 400px;
    }

    .comparison-preview-modern img {
        width: 100%;
        height: 100%;
        object-fit: contain;
        object-position: center;
        display: block;
        image-rendering: pixelated;
    }

    .image-metadata-modern {
        display: grid;
        grid-template-columns: 1fr 1fr;
        border-top: 4px solid black;
    }

    .metadata-item-modern {
        background: var(--bg-surface);
        border-right: 4px solid black;
        border-bottom: 4px solid black;
        padding: 1rem;
    }

    .metadata-item-modern:nth-child(2n) { border-right: none; }
    .metadata-item-modern:nth-last-child(-n+2) { border-bottom: none; }

    .metadata-label-modern {
        font-size: 0.8rem;
        color: black;
        font-family: 'Press Start 2P', monospace;
        text-transform: uppercase;
        margin-bottom: 0.5rem;
    }

    .metadata-value-modern {
        font-size: 1.1rem;
        color: black;
        font-weight: 700;
    }
    </style>

    <div class="comparison-section-wrapper">
        <div class="brutal-title">
            <h2 class="pixel-text">PERBANDINGAN GAMBAR</h2>
        </div>
    </div>
    ''', unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        _render_original_card_modern(image, width, height, channels, uploaded_file)
    
    with col2:
        _render_compressed_card_modern(compressed_image, width, height, k, compressed_size)


def _render_original_card_modern(image, width, height, channels, uploaded_file):
    """Render the original image comparison card with modern styling"""
    img_b64 = _image_to_base64(image)
    st.markdown(f"""
        <div class="brutal-card-inner">
            <div class="comparison-card-modern-header">
                <div style="display: flex; align-items: center; gap: 0.8rem;">
                    <h4 class="comparison-card-modern-title">Gambar Asli</h4>
                </div>
                <span class="comparison-badge-modern">Sumber</span>
            </div>
            <div class="comparison-preview-modern">
                <img src="data:image/png;base64,{img_b64}" alt="Gambar Asli" />
            </div>
            <div class="image-metadata-modern">
                <div class="metadata-item-modern">
                    <div class="metadata-label-modern">Resolusi</div>
                    <div class="metadata-value-modern">{width} × {height}</div>
                </div>
                <div class="metadata-item-modern">
                    <div class="metadata-label-modern">Piksel</div>
                    <div class="metadata-value-modern">{width * height:,}</div>
                </div>
                <div class="metadata-item-modern">
                    <div class="metadata-label-modern">Ukuran File</div>
                    <div class="metadata-value-modern">{uploaded_file.size / 1024:.1f} KB</div>
                </div>
                <div class="metadata-item-modern">
                    <div class="metadata-label-modern">Mode Warna</div>
                    <div class="metadata-value-modern">{channels} Kanal</div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)


def _render_compressed_card_modern(compressed_image, width, height, k, compressed_size):
    """Render the compressed image comparison card with modern styling"""
    img_b64 = _image_to_base64(compressed_image)
    st.markdown(f"""
        <div class="brutal-card-inner">
            <div class="comparison-card-modern-header compressed">
                <div style="display: flex; align-items: center; gap: 0.8rem;">
                    <h4 class="comparison-card-modern-title">Gambar Kompresi</h4>
                </div>
                <span class="comparison-badge-modern">K = {k}</span>
            </div>
            <div class="comparison-preview-modern">
                <img src="data:image/png;base64,{img_b64}" alt="Gambar Kompresi" />
            </div>
            <div class="image-metadata-modern">
                <div class="metadata-item-modern">
                    <div class="metadata-label-modern">Resolusi</div>
                    <div class="metadata-value-modern">{width} × {height}</div>
                </div>
                <div class="metadata-item-modern">
                    <div class="metadata-label-modern">Piksel</div>
                    <div class="metadata-value-modern">{width * height:,}</div>
                </div>
                <div class="metadata-item-modern">
                    <div class="metadata-label-modern">Ukuran File</div>
                    <div class="metadata-value-modern">{compressed_size / 1024:.1f} KB</div>
                </div>
                <div class="metadata-item-modern">
                    <div class="metadata-label-modern">Peringkat (K)</div>
                    <div class="metadata-value-modern">{k}</div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)


def render_interactive_comparison(image_comparison_lib, image, compressed_image):
    """Render optional interactive comparison slider if library is available"""
    if image_comparison_lib is not None:
        st.markdown("""
        <div style="margin-top: 3rem; padding-top: 2rem;">
            <div class="brutal-title">
                <h2 class="pixel-text">PERBANDINGAN INTERAKTIF</h2>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        image_comparison_lib(
            img1=image,
            img2=compressed_image,
            label1="ASLI",
            label2="KOMPRESI"
        )
        return True
    return False


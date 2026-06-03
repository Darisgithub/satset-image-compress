from datetime import datetime
from pathlib import Path

import streamlit as st


def render_download_section(compressed_image, OUTPUT_DIR, buffer):
    """Render download and save controls with modern professional styling"""
    st.markdown("""
    <style>
    .download-section {
        margin-top: 2.5rem;
        padding-top: 2rem;
    }

    .success-message {
        background: var(--accent-neon-green);
        border: 4px solid black;
        box-shadow: 4px 4px 0px black;
        padding: 1rem 1.2rem;
        margin-top: 1rem;
        color: black;
        font-weight: 700;
        display: flex;
        align-items: center;
        gap: 0.8rem;
    }

    .output-info {
        background: var(--bg-surface);
        border: 4px solid black;
        box-shadow: 4px 4px 0px black;
        padding: 1rem;
        font-size: 0.85rem;
        color: black;
        margin-top: 1.5rem;
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 700;
    }
    
    .output-info strong {
        color: var(--accent-pink);
    }
    </style>

    <div class="download-section">
        <div class="brutal-title" style="margin-bottom: 1.5rem; padding-bottom: 1rem; border-bottom: 4px solid black; display: flex; align-items: center; gap: 0.8rem;">
            <h3 class="pixel-text" style="margin:0;">SIMPAN & UNDUH</h3>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col_dl1, col_dl2 = st.columns(2, gap="medium")
    
    with col_dl1:
        if st.button("💾 SIMPAN KOMPRESI", use_container_width=True, key="save", help="Simpan gambar hasil kompresi ke direktori output"):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"compressed_{timestamp}.jpg"
            filepath = OUTPUT_DIR / filename
            
            compressed_image.save(filepath, format="JPEG", quality=85)
            
            st.markdown(f"""
            <div class="success-message">
                <div>Tersimpan: <strong>{filename}</strong></div>
            </div>
            """, unsafe_allow_html=True)
    
    with col_dl2:
        st.download_button(
            label="⬇️ UNDUH GAMBAR",
            data=buffer.getvalue(),
            file_name=f"compressed_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg",
            mime="image/jpeg",
            use_container_width=True,
            key="download",
            help="Unduh gambar hasil kompresi langsung ke perangkat Anda"
        )
    
    st.markdown(f"""
    <div class="output-info">
        <div style="font-size: 0.8rem; word-break: break-all;">
            <strong>Direktori Output:</strong> {OUTPUT_DIR}
        </div>
    </div>
    """, unsafe_allow_html=True)

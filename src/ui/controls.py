import streamlit as st


def render_controls():
    """Render upload area and compression settings controls with brutalist design
    
    Returns:
        tuple: (uploaded_file, quality_mode, filter_mode)
    """
    col1, col2 = st.columns([1, 1], gap="medium")
    
    # ===== LEFT COLUMN: FILE UPLOAD =====
    with col1:
        st.markdown('''
        <div class="brutal-card" style="background: var(--accent-cyan);">
            <div style="display: flex; align-items: center; gap: 0.8rem; margin-bottom: 1rem;">
                <h2 class="pixel-text" style="font-size: 1rem; color: black; margin: 0;">UNGGAH GAMBAR</h2>
            </div>
            <div style="font-size: 0.9rem; color: black; font-weight: 700;">Pilih gambar untuk dikompresi menggunakan SVD</div>
        </div>
        ''', unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader(
            "Tarik atau pilih gambar",
            type=["jpg", "jpeg", "png", "bmp", "webp"],
            label_visibility="collapsed",
            key="img_upload",
            help="Format didukung: JPG, PNG, BMP, WebP"
        )
    
    # ===== RIGHT COLUMN: SETTINGS =====
    with col2:
        st.markdown('''
        <div class="brutal-card" style="background: var(--accent-yellow);">
            <div style="display: flex; align-items: center; gap: 0.8rem; margin-bottom: 1rem;">
                <h2 class="pixel-text" style="font-size: 1rem; color: black; margin: 0;">PENGATURAN</h2>
            </div>
            <div style="font-size: 0.9rem; color: black; font-weight: 700;">Konfigurasi parameter kompresi</div>
        </div>
        ''', unsafe_allow_html=True)
        
        col_q, col_f = st.columns(2, gap="small")
        
        with col_q:
            quality_mode = st.selectbox(
                "Tingkat Kualitas",
                ["Ukuran Kecil", "Seimbang", "Kualitas Tinggi"],
                label_visibility="visible",
                key="quality",
                help="Pilih tingkat kompresi"
            )
        
        with col_f:
            filter_mode = st.selectbox(
                "Tipe Filter",
                ["Standar", "Retro", "Pro"],
                label_visibility="visible",
                key="filter",
                help="Mode pemrosesan"
            )
    
    return uploaded_file, quality_mode, filter_mode


def get_default_k(quality_mode, max_rank):
    """Calculate default compression rank based on quality mode
    
    Args:
        quality_mode (str): Quality mode selection
        max_rank (int): Maximum possible rank value
    
    Returns:
        int: Default compression rank
    """
    if quality_mode == "Ukuran Kecil":
        return min(20, max_rank)
    elif quality_mode == "Seimbang":
        return max(1, min(80, max_rank // 2))
    else:  # Kualitas Tinggi
        return max(1, min(150, max_rank))


def render_compression_rank_slider(max_rank, default_k):
    """Render the compression rank slider with modern styling
    
    Args:
        max_rank (int): Maximum possible rank
        default_k (int): Default rank value
    
    Returns:
        int: Selected compression rank
    """
    st.markdown('''
    <div class="brutal-card" style="margin-top: 1rem; padding: 1rem; border-width: 2px;">
        <div style="display: flex; align-items: center; gap: 0.8rem;">
            <h4 class="pixel-text" style="font-size: 0.8rem; margin: 0; color: black;">PERINGKAT KOMPRESI (K)</h4>
        </div>
        <p style="font-size: 0.9rem; color: black; margin-top: 0.5rem; font-weight: 600;">
            K tinggi = Kualitas lebih baik tapi ukuran file besar. K rendah = Kompresi maksimal tapi kualitas menurun.
        </p>
    </div>
    ''', unsafe_allow_html=True)
    
    k = st.slider(
        "Peringkat Kompresi",
        min_value=1,
        max_value=max_rank,
        value=default_k,
        label_visibility="collapsed",
        help=f"Pilih nilai antara 1 dan {max_rank}. Rentang direkomendasikan: 10-{min(100, max_rank)}"
    )
    
    return k


def render_compress_button():
    """Render the main compression button with modern styling
    
    Returns:
        bool: Whether the button was clicked
    """
    st.markdown('<div style="margin: 2rem 0;"></div>', unsafe_allow_html=True)
    
    col_btn = st.columns([1, 2, 1])
    with col_btn[1]:
        compress_button = st.button(
            "⚡ KOMPRESI GAMBAR",
            use_container_width=True,
            key="compress",
            help="Klik untuk menerapkan kompresi SVD pada gambar yang diunggah"
        )
    
    return compress_button


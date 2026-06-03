import streamlit as st


def render_metrics_section(original_size, compressed_size, k, saved_ratio, compression_ratio):
    """Render the professional metrics display section"""
    st.markdown('''
    <style>
    .metrics-section { margin: 3rem 0; }
    .brutal-title {
        display: flex;
        align-items: center;
        gap: 0.8rem;
        margin-bottom: 2rem;
        padding-bottom: 1rem;
        border-bottom: 4px solid black;
    }
    
    .metrics-grid-modern {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 1.5rem;
    }

    .metric-card-modern {
        background: var(--bg-surface);
        border: 4px solid black;
        box-shadow: 4px 4px 0px black;
        padding: 1.5rem;
        text-align: center;
        transition: transform 0.1s ease, box-shadow 0.1s ease;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }

    .metric-card-modern:hover {
        transform: translate(2px, 2px);
        box-shadow: 2px 2px 0px black;
    }

    .metric-card-modern.success {
        background: var(--accent-neon-green);
    }
    .metric-card-modern.success:hover {
        background: var(--accent-yellow);
    }

    .metric-icon-modern {
        font-size: 2.5rem;
        margin-bottom: 1rem;
        display: inline-block;
        color: black;
    }

    .metric-label-modern {
        font-family: 'Press Start 2P', monospace;
        font-size: 0.6rem;
        color: black;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.8rem;
    }

    .metric-value-modern {
        font-size: 1.8rem;
        font-weight: 700;
        color: black;
        font-family: 'Space Grotesk', sans-serif;
        margin-bottom: 0.5rem;
    }

    .metric-subtext-modern {
        font-size: 0.8rem;
        color: #222;
        font-weight: 600;
    }

    @media (max-width: 1024px) {
        .metrics-grid-modern { grid-template-columns: repeat(2, 1fr); }
    }
    @media (max-width: 768px) {
        .metrics-grid-modern { grid-template-columns: repeat(2, 1fr); }
    }
    @media (max-width: 480px) {
        .metrics-grid-modern { grid-template-columns: 1fr; }
    }
    </style>

    <div class="metrics-section">
        <div class="brutal-title">
            <h2 class="pixel-text">STATISTIK KOMPRESI</h2>
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    col_m1, col_m2, col_m3, col_m4 = st.columns(4, gap="medium")
    
    with col_m1:
        _render_metric_card_modern(
            label="Rasio Kompresi",
            value=f"{compression_ratio:.2f}x",
            subtext="Reduksi Ukuran",
            is_success=True
        )
    
    with col_m2:
        _render_metric_card_modern(
            label="Ruang Tersimpan",
            value=f"{saved_ratio:.1f}%",
            subtext="Reduksi Data",
            is_success=True
        )
    
    with col_m3:
        _render_metric_card_modern(
            label="Peringkat (K)",
            value=str(k),
            subtext="Komponen SVD",
            is_success=False
        )
    
    with col_m4:
        quality_retained = max(50, 100 - (saved_ratio * 0.5))
        _render_metric_card_modern(
            label="Retensi Kualitas",
            value=f"{quality_retained:.0f}%",
            subtext="Fidelitas Visual",
            is_success=False
        )


def _render_metric_card_modern(label, value, subtext, is_success=False):
    success_class = "success" if is_success else ""
    st.markdown(f"""
    <div class="metric-card-modern {success_class}">
        <div>
            <div class="metric-label-modern">{label}</div>
            <div class="metric-value-modern">{value}</div>
        </div>
        <div class="metric-subtext-modern">{subtext}</div>
    </div>
    """, unsafe_allow_html=True)


def calculate_metrics(original_size, compressed_size):
    saved_ratio = ((original_size - compressed_size) / original_size) * 100
    compression_ratio = original_size / compressed_size if compressed_size > 0 else 0
    return saved_ratio, compression_ratio

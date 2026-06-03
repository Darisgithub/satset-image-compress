import streamlit as st


def load_styles():
    """Load and apply all CSS styles to the application"""
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&family=Space+Grotesk:wght@400;600;700&family=JetBrains+Mono:wght@700&family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-200..200&display=swap');

    :root {
        /* Brutalism x Pixel Art Theme */
        --bg-primary: #f4f4f0;
        --bg-surface: #ffffff;
        --accent-neon-green: #39FF14;
        --accent-pink: #FF00FF;
        --accent-cyan: #00FFFF;
        --accent-yellow: #FFEA00;
        --accent-orange: #FF5E00;
        --text-primary: #000000;
        --text-secondary: #222222;
        --border-thick: 4px;
        --border-thin: 2px;
        --shadow-brutal: 4px 4px 0px #000000;
        --shadow-brutal-hover: 2px 2px 0px #000000;
        --shadow-brutal-lg: 8px 8px 0px #000000;
    }

    /* =====================================================
       MATERIAL SYMBOLS ICONS
       ===================================================== */
    .material-symbols-outlined {
        font-variation-settings: 'FILL' 1, 'wght' 700, 'GRAD' 0, 'opsz' 24;
        font-size: 24px;
        line-height: 1;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        vertical-align: middle;
        color: var(--text-primary);
    }
    .icon-sm { font-size: 18px; }
    .icon-md { font-size: 24px; }
    .icon-lg { font-size: 32px; }
    .icon-xl { font-size: 48px; }

    /* =====================================================
       GLOBAL & RESET
       ===================================================== */
    * {
        box-sizing: border-box;
    }
    html, body, [class*="css"] {
        font-family: 'Space Grotesk', sans-serif;
        color: var(--text-primary);
        background: var(--bg-primary);
        line-height: 1.6;
    }

    [data-testid="stAppViewContainer"] {
        background: var(--bg-primary);
        background-image: 
            linear-gradient(rgba(0, 0, 0, 0.05) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0, 0, 0, 0.05) 1px, transparent 1px);
        background-size: 20px 20px;
    }

    .block-container, main {
        max-width: 1300px;
        margin: 0 auto;
        padding: 2rem 1rem !important;
    }

    /* =====================================================
       PIXEL & BRUTALIST ELEMENTS
       ===================================================== */
    .brutal-card {
        background: var(--bg-surface);
        border: var(--border-thick) solid var(--text-primary);
        box-shadow: var(--shadow-brutal);
        padding: 1.5rem;
        position: relative;
        transition: transform 0.1s ease, box-shadow 0.1s ease;
        margin-bottom: 2rem;
    }
    
    .pixel-text {
        font-family: 'Press Start 2P', monospace;
        letter-spacing: -0.05em;
    }

    /* =====================================================
       IMAGE PREVIEW overrides
       ===================================================== */
    [data-testid="stImage"] {
        width: 100% !important;
        height: 100% !important;
        border: var(--border-thick) solid var(--text-primary);
        background: #000;
    }
    [data-testid="stImage"] img {
        width: 100% !important;
        height: 100% !important;
        object-fit: contain !important;
        object-position: center !important;
        image-rendering: pixelated; /* Retro pixel feel for images */
    }

    /* =====================================================
       STREAMLIT ELEMENT OVERRIDES
       ===================================================== */
    h1, h2, h3, h4, h5, h6 {
        color: var(--text-primary);
        margin-top: 1.5rem;
        margin-bottom: 1rem;
        font-weight: 700;
        font-family: 'Press Start 2P', monospace;
        text-transform: uppercase;
        line-height: 1.4;
    }
    h1 { font-size: 1.8rem; }
    h2 { font-size: 1.4rem; }
    h3 { font-size: 1rem; }

    .stDivider, hr {
        background: var(--text-primary);
        border: none;
        height: var(--border-thick);
        margin: 2rem 0 !important;
    }

    /* Form Elements */
    .stSelectbox [role="listbox"], .stSlider input {
        border-radius: 0 !important;
        border: var(--border-thick) solid var(--text-primary) !important;
        box-shadow: var(--shadow-brutal) !important;
        background: var(--bg-surface) !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 700 !important;
    }
    
    .stSelectbox label, .stSlider label {
        color: var(--text-primary) !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        font-family: 'Press Start 2P', monospace !important;
        font-size: 0.7rem !important;
        margin-bottom: 0.5rem !important;
    }

    /* File uploader */
    .uploadedFileData, [data-testid="stFileUploaderDropzone"] {
        border: var(--border-thick) dashed var(--text-primary) !important;
        border-radius: 0 !important;
        background: var(--accent-yellow) !important;
        padding: 2rem !important;
        transition: background 0.2s ease;
    }
    [data-testid="stFileUploaderDropzone"]:hover {
        background: var(--accent-cyan) !important;
    }

    /* Input fields */
    [data-testid="stNumberInput"] input,
    [data-testid="stTextInput"] input,
    [data-testid="stTextArea"] textarea {
        border: var(--border-thick) solid var(--text-primary) !important;
        border-radius: 0 !important;
        background: var(--bg-surface) !important;
        color: var(--text-primary) !important;
        padding: 0.75rem !important;
        font-size: 1rem !important;
        font-weight: 700 !important;
        box-shadow: var(--shadow-brutal);
    }

    /* Slider */
    .stSlider [role="slider"] {
        background: var(--accent-pink) !important;
        border: 2px solid var(--text-primary) !important;
        width: 24px !important;
        height: 24px !important;
        border-radius: 0 !important;
        box-shadow: 2px 2px 0px #000 !important;
    }
    .stSlider .stSliderValue {
        font-family: 'Press Start 2P', monospace !important;
        font-size: 0.7rem !important;
        color: var(--text-primary) !important;
        background: var(--accent-yellow) !important;
        padding: 0.2rem 0.5rem !important;
        border: 2px solid var(--text-primary) !important;
    }
    
    /* Buttons */
    .stButton > button, .stDownloadButton > button {
        border: var(--border-thick) solid var(--text-primary) !important;
        background: var(--accent-neon-green) !important;
        color: var(--text-primary) !important;
        text-transform: uppercase !important;
        font-weight: 700 !important;
        font-family: 'Press Start 2P', monospace !important;
        font-size: 0.8rem !important;
        padding: 1rem 1.5rem !important;
        box-shadow: var(--shadow-brutal-lg) !important;
        border-radius: 0 !important;
        cursor: pointer !important;
        transition: all 0.1s linear !important;
        line-height: 1.5 !important;
    }
    .stButton > button:hover, .stDownloadButton > button:hover {
        transform: translate(4px, 4px) !important;
        box-shadow: var(--shadow-brutal) !important;
        background: var(--accent-yellow) !important;
    }
    .stButton > button:active, .stDownloadButton > button:active {
        transform: translate(8px, 8px) !important;
        box-shadow: none !important;
    }
    
    .stDownloadButton > button {
        background: var(--accent-cyan) !important;
    }

    /* Spinner */
    .stSpinner > div > div {
        border-color: var(--accent-pink) !important;
        border-bottom-color: var(--text-primary) !important;
        border-width: 4px !important;
    }
    .stSpinner > div > span {
        font-family: 'Press Start 2P', monospace !important;
        font-size: 0.8rem !important;
        text-transform: uppercase !important;
    }

    /* Alerts */
    .stSuccess {
        background: var(--accent-neon-green) !important;
        border: var(--border-thick) solid var(--text-primary) !important;
        color: var(--text-primary) !important;
        border-radius: 0 !important;
        box-shadow: var(--shadow-brutal);
    }
    .stWarning {
        background: var(--accent-yellow) !important;
        border: var(--border-thick) solid var(--text-primary) !important;
        color: var(--text-primary) !important;
        border-radius: 0 !important;
        box-shadow: var(--shadow-brutal);
    }
    .stError {
        background: #FF0000 !important;
        border: var(--border-thick) solid var(--text-primary) !important;
        color: #FFF !important;
        border-radius: 0 !important;
        box-shadow: var(--shadow-brutal);
    }
    .stInfo {
        background: var(--accent-cyan) !important;
        border: var(--border-thick) solid var(--text-primary) !important;
        color: var(--text-primary) !important;
        border-radius: 0 !important;
        box-shadow: var(--shadow-brutal);
    }
    
    @media (max-width: 768px) {
        h1 { font-size: 1.2rem; }
        h2 { font-size: 1rem; }
        h3 { font-size: 0.8rem; }
    }
    </style>
    """, unsafe_allow_html=True)

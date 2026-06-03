import streamlit as st


def render_footer():
    st.markdown("""
<style>
.brutal-footer {
background: var(--bg-surface);
border: 4px solid black;
box-shadow: 6px 6px 0px black;
padding: 2rem;
margin-top: 4rem;
text-align: center;
transition: transform 0.1s ease, box-shadow 0.1s ease;
}

.brutal-footer:hover {
transform: translate(2px, 2px);
box-shadow: 4px 4px 0px black;
}

.footer-title {
font-family: 'Press Start 2P', monospace;
font-size: 0.9rem;
color: black;
margin-bottom: 1rem;
text-transform: uppercase;
letter-spacing: 0.05em;
}

.footer-text {
font-family: 'Space Grotesk', sans-serif;
color: black;
font-size: 1rem;
font-weight: 700;
margin: 0.5rem 0;
text-transform: uppercase;
}

.footer-institution {
font-family: 'Space Grotesk', sans-serif;
color: black;
font-size: 1rem;
font-weight: 700;
margin: 0.5rem 0;
}

.footer-divider {
width: 100%;
height: 4px;
background: black;
margin: 1.5rem 0;
}

.footer-credit {
color: black;
font-size: 0.8rem;
font-weight: 700;
margin-top: 1.5rem;
}

.footer-badge {
display: inline-block;
background: var(--accent-yellow);
color: black;
padding: 0.5rem 1rem;
font-size: 0.7rem;
font-family: 'Press Start 2P', monospace;
border: 2px solid black;
margin-top: 1rem;
box-shadow: 2px 2px 0px black;
text-transform: uppercase;
}
</style>

<div class="brutal-footer">
<div class="footer-content">
<div class="footer-title">LAB SATSET IMAGE COMPRESS</div>
<div class="footer-divider"></div>

<div class="footer-text">Kelompok 2 Teknik Informatika</div>
<div class="footer-institution">Universitas Muhammadiyah Tangerang</div>
<div class="footer-text">Tahun Ajaran 2026</div>

<div class="footer-credit">
Dibuat dengan Python, NumPy, Pillow, Matplotlib & Streamlit 
</div>

<div class="footer-badge">
PROYEK AKADEMIK
</div>
</div>
</div>
""", unsafe_allow_html=True)

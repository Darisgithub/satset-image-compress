import streamlit as st


def render_header():
    """Render the main application header with brutalist pixel design"""
    st.markdown("""
    <div class="brutal-card" style="background: var(--accent-pink); color: white; text-align: center; border-color: black;">
        <div style="display: flex; align-items: center; justify-content: center; gap: 1rem; margin-bottom: 0.8rem;">
            <div class="pixel-text" style="font-size: 1.8rem; line-height: 1.4; color: white; text-shadow: 4px 4px 0px black;">
                SATSET IMAGE COMPRESS
            </div>
        </div>
        <div style="font-size: 1.1rem; font-weight: 700; margin-bottom: 2rem; color: black; background: var(--accent-yellow); padding: 0.5rem; display: inline-block; border: 2px solid black;">
            Alat Profesional Kompresi Gambar Berbasis Singular Value Decomposition
        </div>
        <div style="display: flex; gap: 1rem; flex-wrap: wrap; justify-content: center; align-items: center;">
       <div class="pixel-text" style="background: var(--accent-cyan); color: black; padding: 0.5rem 1rem; border: 2px solid black; font-size: 0.7rem;">PYTHON</div>
        <div class="pixel-text" style="background: var(--accent-neon-green); color: black; padding: 0.5rem 1rem; border: 2px solid black; font-size: 0.7rem;">NUMPY</div>
        <div class="pixel-text" style="background: var(--accent-yellow); color: black; padding: 0.5rem 1rem; border: 2px solid black; font-size: 0.7rem;">PILLOW</div>
        <div class="pixel-text" style="background: #FF6B6B; color: black; padding: 0.5rem 1rem; border: 2px solid black; font-size: 0.7rem;">MATPLOTLIB</div>
        <div class="pixel-text" style="background: var(--bg-surface); color: black; padding: 0.5rem 1rem; border: 2px solid black; font-size: 0.7rem;">STREAMLIT</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import streamlit as st
import base64
from io import BytesIO


# Color scheme matching the application theme
COLORS = {
    'cyan': '#00FFFF',
    'purple': '#FF00FF',
    'emerald': '#39FF14',
    'yellow': '#FFEA00',
    'bg_light': '#f4f4f0',
    'bg_surface': '#ffffff',
    'text_primary': '#000000',
    'border': '#000000',
}

CHANNEL_COLORS = {
    'R': '#FF0000',  # Red
    'G': '#00FF00',  # Green
    'B': '#0000FF',  # Blue
    'L': '#00FFFF',  # Cyan for grayscale
}


def _fig_to_base64(fig):
    buf = BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")
    plt.close(fig)
    return base64.b64encode(buf.getvalue()).decode("utf-8")


def create_singular_value_chart(singular_values_dict, max_display=100):
    """
    Create Matplotlib line chart of singular value distribution
    """
    fig, ax = plt.subplots(figsize=(12, 6))
    fig.patch.set_facecolor(COLORS['bg_light'])
    ax.set_facecolor(COLORS['bg_surface'])
    
    # Plot singular values for each channel
    for channel, S in singular_values_dict.items():
        S_limited = S[:min(len(S), max_display)]
        indices = np.arange(1, len(S_limited) + 1)
        
        color = CHANNEL_COLORS.get(channel, COLORS['cyan'])
        ax.plot(indices, S_limited, marker='s', markersize=6, linewidth=3,
                label=f'Kanal {channel}', color=color, alpha=0.9, markeredgecolor='black', markeredgewidth=2)
    
    # Styling
    ax.set_xlabel('Indeks Nilai Singular', fontsize=12, fontweight=900, color=COLORS['text_primary'], fontfamily='monospace')
    ax.set_ylabel('Magnitudo Nilai Singular', fontsize=12, fontweight=900, color=COLORS['text_primary'], fontfamily='monospace')
    ax.set_title('Distribusi Nilai Singular', fontsize=14, fontweight=900, 
                 color=COLORS['text_primary'], pad=20, fontfamily='monospace')
    
    # Grid
    ax.grid(True, alpha=1.0, linestyle='-', linewidth=2, color=COLORS['border'])
    ax.set_axisbelow(True)
    
    # Spines
    for spine in ax.spines.values():
        spine.set_color(COLORS['border'])
        spine.set_linewidth(4)
    
    # Tick styling
    ax.tick_params(colors=COLORS['text_primary'], labelsize=10, width=2, length=6)
    
    # Legend
    legend = ax.legend(loc='upper right', framealpha=1.0, fancybox=False, shadow=True,
              fontsize=10, frameon=True, edgecolor='black')
    legend.get_frame().set_linewidth(2)
    
    plt.tight_layout()
    return fig


def create_cumulative_retention_chart(singular_values_dict, max_display=100):
    """
    Create Matplotlib line chart of cumulative information retention
    """
    fig, ax = plt.subplots(figsize=(12, 6))
    fig.patch.set_facecolor(COLORS['bg_light'])
    ax.set_facecolor(COLORS['bg_surface'])
    
    for channel, S in singular_values_dict.items():
        S_limited = S[:min(len(S), max_display)]
        cumsum = np.cumsum(S_limited)
        total = np.sum(S_limited)
        cumulative_percent = (cumsum / total) * 100
        
        indices = np.arange(1, len(cumulative_percent) + 1)
        
        color = CHANNEL_COLORS.get(channel, COLORS['cyan'])
        ax.plot(indices, cumulative_percent, marker='s', markersize=6, linewidth=3,
                label=f'Kanal {channel}', color=color, alpha=0.9, markeredgecolor='black', markeredgewidth=2)
    
    # Styling
    ax.set_xlabel('Jumlah Nilai Singular (k)', fontsize=12, fontweight=900, 
                  color=COLORS['text_primary'], fontfamily='monospace')
    ax.set_ylabel('Retensi Informasi Kumulatif (%)', fontsize=12, fontweight=900, 
                  color=COLORS['text_primary'], fontfamily='monospace')
    ax.set_title('Retensi Informasi Berdasarkan Nilai Singular', fontsize=14, fontweight=900, 
                 color=COLORS['text_primary'], pad=20, fontfamily='monospace')
    
    ax.set_ylim([0, 105])
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f'{int(y)}%'))
    
    # Grid
    ax.grid(True, alpha=1.0, linestyle='-', linewidth=2, color=COLORS['border'])
    ax.set_axisbelow(True)
    
    # Add reference lines
    ax.axhline(y=90, color=COLORS['purple'], linestyle='--', linewidth=3, label='Retensi 90%')
    ax.axhline(y=95, color=COLORS['emerald'], linestyle='--', linewidth=3, label='Retensi 95%')
    
    # Spines
    for spine in ax.spines.values():
        spine.set_color(COLORS['border'])
        spine.set_linewidth(4)
    
    # Tick styling
    ax.tick_params(colors=COLORS['text_primary'], labelsize=10, width=2, length=6)
    
    # Legend
    legend = ax.legend(loc='lower right', framealpha=1.0, fancybox=False, shadow=True,
              fontsize=10, frameon=True, edgecolor='black')
    legend.get_frame().set_linewidth(2)
    
    plt.tight_layout()
    return fig


def generate_analysis_insights(singular_values_dict, k, original_shape):
    """
    Generate automated analysis insights based on SVD data
    """
    insights = []
    
    # Insight 1: Information concentration
    for channel, S in singular_values_dict.items():
        total_info = np.sum(S)
        first_10_percent = np.sum(S[:max(1, len(S)//10)]) / total_info * 100
        
        insights.append(
            f"<b>Kanal {channel}: Konsentrasi Informasi</b><br>"
            f"10% nilai singular pertama menyimpan <b>{first_10_percent:.1f}%</b> "
            f"dari total informasi gambar."
        )
    
    # Insight 2: Rank selection impact
    if len(singular_values_dict) > 0:
        first_channel = list(singular_values_dict.values())[0]
        total_info = np.sum(first_channel)
        selected_info = np.sum(first_channel[:k])
        retention = (selected_info / total_info) * 100
        
        insights.append(
            f"<b>Retensi Informasi Peringkat k={k}:</b><br>"
            f"Penggunaan {k} nilai singular mempertahankan sekitar <b>{retention:.1f}%</b> "
            f"energi matriks citra berhasil dipertahankan."
        )
    
    # Insight 3: Compression efficiency
    original_elements = original_shape[0] * original_shape[1]
    if len(singular_values_dict) > 0:
        first_channel = list(singular_values_dict.values())[0]
        svd_elements = (original_shape[0] * k) + k + (k * original_shape[1])
        compression_ratio = original_elements / svd_elements
        
        insights.append(
            f"<b>Efisiensi Kompresi SVD:</b><br>"
            f"Rasio kompresi teoretis: <b>{compression_ratio:.1f}:1</b><br>"
            f"Berdasarkan penyimpanan matriks U ({original_shape[0]}×{k}), "
            f"Σ ({k}), dan V<sup>T</sup> ({k}×{original_shape[1]})."
        )
    
    # Insight 4: Quality vs compression trade-off
    insights.append(
        f"<b>Trade-off Kualitas dan Kompresi:</b><br>"
        f"Nilai k rendah (misal 10-50) memberikan kompresi maksimal dengan risiko artefak visual.<br>"
        f"Nilai k tinggi (misal 100-200) mempertahankan kualitas tapi mengurangi rasio kompresi.<br>"
        f"Pilihan saat ini: k={k}"
    )
    
    # Insight 5: Mathematical background
    insights.append(
        f"<b>Singular Value Decomposition (SVD):</b><br>"
        f"SVD memecah matriks gambar menjadi A = UΣV<sup>T</sup>, di mana nilai singular "
        f"(Σ) mewakili kepentingan tiap komponen. Membuang komponen dengan nilai terkecil "
        f"akan mengkompresi gambar."
    )
    
    return insights


def render_analysis_section(singular_values_dict, k, original_shape):
    """
    Render the complete analysis section with charts and insights
    """
    st.markdown('''
    <style>
    .analysis-section { margin: 4rem 0 2rem; }
    .brutal-title {
        display: flex;
        align-items: center;
        gap: 0.8rem;
        margin-bottom: 2rem;
        padding-bottom: 1rem;
        border-bottom: 4px solid black;
    }

    .chart-container {
        background: var(--bg-surface);
        border: 4px solid black;
        box-shadow: 4px 4px 0px black;
        padding: 1.5rem;
        margin-bottom: 2rem;
    }

    .insights-grid {
        display: flex;
        flex-direction: column;
        gap: 1.5rem;
    }

    .insight-card {
        background: var(--accent-yellow);
        border: 4px solid black;
        box-shadow: 4px 4px 0px black;
        padding: 1.5rem;
        font-size: 0.95rem;
        line-height: 1.6;
        color: black;
        font-family: 'Space Grotesk', sans-serif;
    }
    </style>
    ''', unsafe_allow_html=True)
    
    # Header
    st.markdown(
        '<div class="analysis-section"><div class="brutal-title">'
        '<h2 class="pixel-text">ANALISIS KOMPRESI</h2>'
        '</div></div>',
        unsafe_allow_html=True
    )
    
    col1, col2 = st.columns([1, 1.2], gap="large")
    
    with col1:
        # Generated Insights
        st.markdown('<div class="insights-grid">', unsafe_allow_html=True)
        insights = generate_analysis_insights(singular_values_dict, k, original_shape)
        
        for insight in insights:
            st.markdown(
                f'<div class="insight-card">{insight}</div>',
                unsafe_allow_html=True
            )
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        # Singular Value Distribution Chart
        fig1 = create_singular_value_chart(singular_values_dict)
        fig1_b64 = _fig_to_base64(fig1)
        
        st.markdown(f'''
        <div class="chart-container">
            <div class="pixel-text" style="margin-bottom: 1rem;">Distribusi Nilai Singular</div>
            <img src="data:image/png;base64,{fig1_b64}" style="width: 100%; height: auto; display: block; border: 2px solid black; margin-bottom: 1rem;" />
            <div style="font-family: 'Space Grotesk', sans-serif; font-size: 0.9rem; color: black; line-height: 1.5;">
                <b>Grafik ini menunjukkan peluruhan nilai singular. Sebagian besar informasi visual terkonsentrasi pada beberapa nilai singular pertama.</b>
            </div>
        </div>
        ''', unsafe_allow_html=True)
        
        # Cumulative Information Retention Chart
        fig2 = create_cumulative_retention_chart(singular_values_dict)
        fig2_b64 = _fig_to_base64(fig2)
        
        st.markdown(f'''
        <div class="chart-container">
            <div class="pixel-text" style="margin-bottom: 1rem;">Retensi Informasi Berdasarkan Nilai Singular</div>
            <img src="data:image/png;base64,{fig2_b64}" style="width: 100%; height: auto; display: block; border: 2px solid black; margin-bottom: 1rem;" />
            <div style="font-family: 'Space Grotesk', sans-serif; font-size: 0.9rem; color: black; line-height: 1.5;">
                <b>Persentase kumulatif dari informasi yang dipertahankan seiring peningkatan peringkat (k). Kurva yang curam menandakan sedikit komponen sudah bisa mewakili sebagian besar informasi gambar.</b>
            </div>
        </div>
        ''', unsafe_allow_html=True)

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import joblib

# ── SAYFA AYARLARI ──
st.set_page_config(
    page_title="CustomerIQ — E-Commerce Analytics",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── GLOBAL CSS ──
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap');

:root {
    --bg-primary: #0a0a0f;
    --bg-secondary: #111118;
    --bg-card: #16161f;
    --bg-card-hover: #1c1c28;
    --accent-cyan: #00d4ff;
    --accent-purple: #7c3aed;
    --accent-green: #10b981;
    --accent-orange: #f59e0b;
    --accent-red: #ef4444;
    --text-primary: #f1f5f9;
    --text-secondary: #94a3b8;
    --text-muted: #475569;
    --border: #1e2035;
    --border-glow: rgba(0, 212, 255, 0.3);
}

html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"], .main, .block-container {
    background-color: var(--bg-primary) !important;
    font-family: 'Space Grotesk', sans-serif !important;
    color: var(--text-primary) !important;
}

[data-testid="stHeader"] {
    background-color: var(--bg-primary) !important;
}

[data-testid="stSidebar"] {
    background-color: var(--bg-secondary) !important;
    border-right: 1px solid var(--border) !important;
}

[data-testid="stSidebar"] * {
    color: var(--text-primary) !important;
}

h1, h2, h3 {
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 700 !important;
    color: var(--text-primary) !important;
}

.main-header {
    background: linear-gradient(135deg, #0a0a0f 0%, #16161f 50%, #0d0d1a 100%);
    border-bottom: 1px solid var(--border);
    padding: 2rem 0 1.5rem;
    margin-bottom: 2rem;
}

.brand-title {
    font-size: 2.4rem;
    font-weight: 700;
    background: linear-gradient(90deg, var(--accent-cyan), var(--accent-purple));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: -0.03em;
    line-height: 1;
}

.brand-subtitle {
    color: var(--text-secondary);
    font-size: 0.9rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    margin-top: 0.4rem;
}

.kpi-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.4rem;
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
}

.kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, var(--accent-cyan), var(--accent-purple));
}

.kpi-card:hover {
    border-color: var(--border-glow);
    transform: translateY(-2px);
}

.kpi-label {
    color: var(--text-secondary);
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    font-weight: 500;
}

.kpi-value {
    font-size: 2rem;
    font-weight: 700;
    color: var(--text-primary);
    font-family: 'JetBrains Mono', monospace;
    line-height: 1.2;
    margin: 0.3rem 0;
}

.kpi-delta-positive {
    color: var(--accent-green);
    font-size: 0.8rem;
    font-weight: 600;
}

.kpi-delta-negative {
    color: var(--accent-red);
    font-size: 0.8rem;
    font-weight: 600;
}

.section-title {
    font-size: 1.1rem;
    font-weight: 600;
    color: var(--text-primary);
    letter-spacing: -0.01em;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.section-title::after {
    content: '';
    flex: 1;
    height: 1px;
    background: var(--border);
    margin-left: 0.5rem;
}

.segment-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 1.2rem;
    transition: all 0.25s ease;
}

.segment-card:hover {
    border-color: rgba(124, 58, 237, 0.4);
    background: var(--bg-card-hover);
}

.insight-box {
    background: linear-gradient(135deg, rgba(0,212,255,0.05), rgba(124,58,237,0.05));
    border: 1px solid rgba(0,212,255,0.15);
    border-radius: 10px;
    padding: 1rem 1.2rem;
    margin: 0.5rem 0;
    font-size: 0.88rem;
    color: var(--text-secondary);
}

.insight-box strong {
    color: var(--accent-cyan);
}

.badge {
    display: inline-block;
    padding: 0.2rem 0.6rem;
    border-radius: 999px;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.05em;
    text-transform: uppercase;
}

.badge-champion { background: rgba(16,185,129,0.15); color: #10b981; border: 1px solid rgba(16,185,129,0.3); }
.badge-loyal    { background: rgba(0,212,255,0.15);  color: #00d4ff; border: 1px solid rgba(0,212,255,0.3);  }
.badge-sleeping { background: rgba(245,158,11,0.15); color: #f59e0b; border: 1px solid rgba(245,158,11,0.3); }
.badge-lost     { background: rgba(239,68,68,0.15);  color: #ef4444; border: 1px solid rgba(239,68,68,0.3);  }

.stButton > button {
    background: linear-gradient(135deg, var(--accent-cyan), var(--accent-purple)) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 600 !important;
    letter-spacing: 0.03em !important;
    padding: 0.6rem 1.5rem !important;
    transition: opacity 0.2s !important;
}

.stButton > button:hover {
    opacity: 0.85 !important;
}

[data-testid="stSelectbox"] > div > div,
[data-testid="stNumberInput"] > div > div > input {
    background-color: var(--bg-card) !important;
    border-color: var(--border) !important;
    color: var(--text-primary) !important;
}

.stSlider > div > div > div { background: var(--accent-cyan) !important; }

hr { border-color: var(--border) !important; }

.stTabs [data-baseweb="tab-list"] {
    background-color: var(--bg-secondary) !important;
    border-radius: 10px;
    padding: 4px;
    gap: 4px;
}

.stTabs [data-baseweb="tab"] {
    background-color: transparent !important;
    color: var(--text-secondary) !important;
    border-radius: 7px !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 500 !important;
}

.stTabs [aria-selected="true"] {
    background-color: var(--bg-card) !important;
    color: var(--text-primary) !important;
}

.stDataFrame { border-radius: 10px; overflow: hidden; }

[data-testid="stSlider"] label p,
[data-testid="stSelectbox"] label p,
[data-testid="stMultiSelect"] label p,
[data-testid="stNumberInput"] label p {
    color: #f1f5f9 !important;
    font-size: 0.9rem !important;
    font-weight: 500 !important;
}
</style>
""", unsafe_allow_html=True)

# ── VERİ & MODEL ──
@st.cache_data
def load_data():
    rfm = pd.read_csv('data/rfm_segments.csv')
    return rfm

@st.cache_resource
def load_model():
    return joblib.load('data/churn_model.pkl')

rfm = load_data()
model = load_model()

@st.cache_data
def compute_predictions(_model, df):
    df = df.copy()
    df['avg_order_value'] = df['monetary'] / df['frequency']
    df['is_one_time'] = (df['frequency'] == 1).astype(int)
    df['high_spender'] = (df['monetary'] > df['monetary'].quantile(0.75)).astype(int)
    df['rfm_score_norm'] = df['rfm_score'] / 12
    features = ['frequency', 'monetary', 'avg_order_value', 'is_one_time', 'high_spender', 'rfm_score_norm']
    df['churn_risk'] = _model.predict(df[features])
    df['churn_probability'] = _model.predict_proba(df[features])[:, 1]
    return df

rfm = compute_predictions(model, rfm)

SEGMENT_COLORS = {
    'Şampiyonlar':       '#10b981',
    'Sadık Müşteriler':  '#00d4ff',
    'Uykudakiler':       '#f59e0b',
    'Kayıp Adayları':    '#ef4444'
}

PLOTLY_THEME = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(family='Space Grotesk', color='#f1f5f9', size=12),
    xaxis=dict(gridcolor='#1e2035', linecolor='#1e2035', tickfont=dict(color='#cbd5e1')),
    yaxis=dict(gridcolor='#1e2035', linecolor='#1e2035', tickfont=dict(color='#cbd5e1')),
    legend=dict(bgcolor='rgba(0,0,0,0)', font=dict(color='#f1f5f9', size=12)),
    margin=dict(l=10, r=10, t=30, b=10)
)

# ── SIDEBAR ──
with st.sidebar:
    st.markdown("""
    <div style='padding: 1rem 0 1.5rem;'>
        <div style='font-size:1.4rem; font-weight:700; background: linear-gradient(90deg, #00d4ff, #7c3aed); -webkit-background-clip:text; -webkit-text-fill-color:transparent;'>⚡ CustomerIQ</div>
        <div style='color:#94a3b8; font-size:0.75rem; letter-spacing:0.08em; text-transform:uppercase; margin-top:0.3rem;'>Analytics Platform</div>
    </div>
    """, unsafe_allow_html=True)

    page = st.radio("", [
        "Genel Bakış",
        "Segment Analizi",
        "Trend Analizi",
        "Churn Tahmini",
        "Kampanya Simülatörü",
        "Müşteri Sorgulama",
        "Cohort Analizi",
        "CLV Analizi",
        "Model Performansı",
        "Gelişmiş Analiz"
    ], label_visibility="collapsed")

    st.divider()
    st.markdown(f"""
    <div style='font-size:0.78rem; color:#475569;'>
        <div style='margin-bottom:0.4rem;'>📦 <span style='color:#94a3b8;'>Toplam Müşteri</span></div>
        <div style='font-family: JetBrains Mono; color:#00d4ff; font-size:1rem; font-weight:600;'>{len(rfm):,}</div>
        <div style='margin:0.8rem 0 0.4rem;'>📅 <span style='color:#94a3b8;'>Veri Aralığı</span></div>
        <div style='font-family: JetBrains Mono; color:#00d4ff; font-size:0.85rem; font-weight:600;'>Oct 2019 — Feb 2020</div>
    </div>
    """, unsafe_allow_html=True)

# ── HEADER ──
st.markdown("""
<div class='main-header'>
    <div class='brand-title'>⚡ CustomerIQ</div>
    <div class='brand-subtitle'>E-Commerce Intelligence Platform</div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════
# SAYFA 1: GENEL BAKIŞ
# ══════════════════════════════════════════
if page == "Genel Bakış":
    total = len(rfm)
    churn_n = int(rfm['churn_risk'].sum())
    total_rev = rfm['monetary'].sum()
    at_risk_rev = rfm[rfm['churn_risk']==1]['monetary'].sum()
    avg_order = rfm['monetary'].mean()
    champions = len(rfm[rfm['segment']=='Şampiyonlar'])

    c1, c2, c3, c4, c5, c6 = st.columns(6)
    cards = [
        (c1, "Toplam Müşteri", f"{total:,}", f"+{champions:,} şampiyon", True),
        (c2, "Churn Riski", f"{churn_n:,}", f"%{churn_n/total*100:.1f} oran", False),
        (c3, "Toplam Gelir", f"${total_rev:,.0f}", "5 aylık dönem", True),
        (c4, "Risk Altındaki Gelir", f"${at_risk_rev:,.0f}", "Kurtarılabilir", False),
        (c5, "Ort. Müşteri Değeri", f"${avg_order:.1f}", "Tüm dönem", True),
        (c6, "Şampiyon Müşteri", f"{champions:,}", f"%{champions/total*100:.1f} oran", True),
    ]
    for col, label, value, delta, positive in cards:
        with col:
            delta_class = "kpi-delta-positive" if positive else "kpi-delta-negative"
            st.markdown(f"""
            <div class='kpi-card'>
                <div class='kpi-label'>{label}</div>
                <div class='kpi-value'>{value}</div>
                <div class='{delta_class}'>{delta}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("<div class='section-title'>Segment Dağılımı</div>", unsafe_allow_html=True)
        seg = rfm['segment'].value_counts().reset_index()
        seg.columns = ['segment', 'count']
        fig = px.pie(seg, values='count', names='segment',
                     color='segment', color_discrete_map=SEGMENT_COLORS, hole=0.55)
        fig.update_traces(textfont_size=13, textfont_color='white',
                          marker=dict(line=dict(color='#0a0a0f', width=2)))
        fig.update_layout(**PLOTLY_THEME, height=320)
        fig.update_layout(legend=dict(orientation='h', y=-0.1, x=0.5, xanchor='center',
                                      bgcolor='rgba(0,0,0,0)', font=dict(color='#f1f5f9')))
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.markdown("<div class='section-title'>Segment Başına Ortalama Gelir</div>", unsafe_allow_html=True)
        rev = rfm.groupby('segment')['monetary'].mean().reset_index()
        rev.columns = ['segment', 'avg_revenue']
        rev = rev.sort_values('avg_revenue')
        fig = px.bar(rev, x='avg_revenue', y='segment', orientation='h',
                     color='segment', color_discrete_map=SEGMENT_COLORS)
        fig.update_traces(marker_line_width=0)
        fig.update_layout(**PLOTLY_THEME, height=320, showlegend=False,
                          xaxis_title="Ortalama Gelir ($)", yaxis_title="")
        st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("<div class='section-title'>RFM Dağılımı</div>", unsafe_allow_html=True)
        sample = rfm.sample(min(3000, len(rfm)), random_state=42)
        fig = px.scatter(sample, x='frequency', y='monetary',
                         color='segment', color_discrete_map=SEGMENT_COLORS, opacity=0.6,
                         labels={'frequency': 'Alışveriş Sıklığı', 'monetary': 'Toplam Harcama ($)'})
        fig.update_traces(marker=dict(size=4))
        fig.update_layout(**PLOTLY_THEME, height=300)
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.markdown("<div class='section-title'>Churn Riski — Segment Bazlı</div>", unsafe_allow_html=True)
        churn_seg = rfm.groupby('segment')['churn_risk'].mean().reset_index()
        churn_seg['pct'] = churn_seg['churn_risk'] * 100
        fig = px.bar(churn_seg, x='segment', y='pct',
                     color='pct', color_continuous_scale=['#10b981', '#f59e0b', '#ef4444'],
                     labels={'pct': 'Churn Riski (%)', 'segment': ''})
        fig.update_traces(marker_line_width=0)
        fig.update_layout(**PLOTLY_THEME, height=300, coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("<div class='section-title'>💡 Önemli Bulgular</div>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"""<div class='insight-box'>
        <strong>${at_risk_rev:,.0f}</strong> değerinde gelir risk altında.
        Müdahale edilirse önemli bir kısmı kurtarılabilir.
        </div>""", unsafe_allow_html=True)
    with c2:
        champ_rev = rfm[rfm['segment']=='Şampiyonlar']['monetary'].sum()
        champ_pct = champ_rev / total_rev * 100
        st.markdown(f"""<div class='insight-box'>
        Şampiyonlar toplam gelirin <strong>%{champ_pct:.1f}'ini</strong> oluşturuyor.
        Müşterilerin sadece %{champions/total*100:.1f}'i bu segmentte.
        </div>""", unsafe_allow_html=True)
    with c3:
        avg_freq = rfm['frequency'].mean()
        st.markdown(f"""<div class='insight-box'>
        Ortalama alışveriş sıklığı <strong>{avg_freq:.1f} kez</strong>.
        Uykudakileri aktive etmek bu sayıyı artırabilir.
        </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════
# SAYFA 2: SEGMENT ANALİZİ
# ══════════════════════════════════════════
elif page == "Segment Analizi":
    st.markdown("### Segment Detay Analizi")
    selected_seg = st.selectbox("Segment seç:", list(SEGMENT_COLORS.keys()))
    seg_data = rfm[rfm['segment'] == selected_seg]

    action_map = {
        'Şampiyonlar': ['VIP programına al', 'Yeni ürünleri ilk göster', 'Teşekkür e-postası gönder', 'Erken erişim kampanyası'],
        'Sadık Müşteriler': ['Sadakat puanı ver', 'Özel indirim kodu (%15)', 'Ücretsiz kargo sun', 'Referral programı'],
        'Uykudakiler': ['"Sizi özledik" e-postası', 'Cazip kampanya sun (%20)', 'Hatırlatma bildirimi', 'Sepet hatırlatıcısı'],
        'Kayıp Adayları': ['Büyük indirim teklif et (%30)', 'Acil geri kazanım e-postası', 'Son şans kampanyası', 'Anket gönder (neden gittiler?)']
    }

    c1, c2, c3, c4 = st.columns(4)
    for col, label, val in [
        (c1, "Müşteri Sayısı", f"{len(seg_data):,}"),
        (c2, "Toplam Gelir", f"${seg_data['monetary'].sum():,.0f}"),
        (c3, "Ort. Harcama", f"${seg_data['monetary'].mean():.1f}"),
        (c4, "Ort. Sıklık", f"{seg_data['frequency'].mean():.1f}x"),
    ]:
        with col:
            st.markdown(f"""<div class='kpi-card'>
                <div class='kpi-label'>{label}</div>
                <div class='kpi-value' style='font-size:1.5rem;'>{val}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns([1.2, 0.8])
    with col1:
        st.markdown("<div class='section-title'>Harcama Dağılımı</div>", unsafe_allow_html=True)
        fig = px.histogram(seg_data, x='monetary', nbins=50,
                           color_discrete_sequence=[SEGMENT_COLORS[selected_seg]])
        fig.update_traces(marker_line_width=0, opacity=0.85)
        fig.update_layout(**PLOTLY_THEME, height=300,
                          xaxis_title="Toplam Harcama ($)", yaxis_title="Müşteri Sayısı")
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.markdown("<div class='section-title'>🎯 Aksiyon Önerileri</div>", unsafe_allow_html=True)
        for action in action_map[selected_seg]:
            st.markdown(f"""<div class='insight-box' style='color:#f1f5f9;'>→ {action}</div>""", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div class='section-title'>Recency Dağılımı</div>", unsafe_allow_html=True)
        fig = px.histogram(seg_data, x='recency', nbins=40,
                           color_discrete_sequence=[SEGMENT_COLORS[selected_seg]])
        fig.update_layout(**PLOTLY_THEME, height=250,
                          xaxis_title="Son Alışverişten Geçen Gün", yaxis_title="")
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.markdown("<div class='section-title'>Frequency Dağılımı</div>", unsafe_allow_html=True)
        fig = px.histogram(seg_data, x='frequency', nbins=40,
                           color_discrete_sequence=[SEGMENT_COLORS[selected_seg]])
        fig.update_layout(**PLOTLY_THEME, height=250,
                          xaxis_title="Alışveriş Sıklığı", yaxis_title="")
        st.plotly_chart(fig, use_container_width=True)

# ══════════════════════════════════════════
# SAYFA 3: TREND ANALİZİ
# ══════════════════════════════════════════
elif page == "Trend Analizi":
    st.markdown("### Haftalık & Aylık Trend Analizi")

    @st.cache_data
    def load_trends():
        daily    = pd.read_csv('data/daily_trend.csv')
        weekly   = pd.read_csv('data/weekly_trend.csv')
        monthly  = pd.read_csv('data/monthly_trend.csv')
        hourly   = pd.read_csv('data/hourly_trend.csv')
        dow      = pd.read_csv('data/dow_trend.csv')
        ev_month = pd.read_csv('data/event_monthly.csv')
        return daily, weekly, monthly, hourly, dow, ev_month

    daily, weekly, monthly, hourly, dow, event_monthly = load_trends()
    tab1, tab2, tab3 = st.tabs(["📅 Günlük", "📆 Haftalık/Aylık", "⏰ Saat & Gün Analizi"])

    with tab1:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=daily['date'], y=daily['gelir'],
            fill='tozeroy', fillcolor='rgba(0,212,255,0.08)',
            line=dict(color='#00d4ff', width=2), name='Günlük Gelir ($)'))
        fig.update_layout(**PLOTLY_THEME, height=350,
                          title=dict(text='Günlük Satış Geliri', font=dict(color='#f1f5f9', size=14)))
        st.plotly_chart(fig, use_container_width=True)
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(x=daily['date'], y=daily['satis'],
            marker_color='#7c3aed', opacity=0.8, name='Satış Sayısı'))
        fig2.update_layout(**PLOTLY_THEME, height=280,
                           title=dict(text='Günlük Satış Adedi', font=dict(color='#f1f5f9', size=14)))
        st.plotly_chart(fig2, use_container_width=True)

    with tab2:
        col1, col2 = st.columns(2)
        with col1:
            fig = px.bar(weekly, x='week', y='gelir', color_discrete_sequence=['#7c3aed'],
                         labels={'gelir': 'Haftalık Gelir ($)', 'week': ''})
            fig.update_layout(**PLOTLY_THEME, height=300,
                              title=dict(text='Haftalık Gelir', font=dict(color='#f1f5f9')))
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            fig = px.bar(monthly, x='month', y='gelir', color_discrete_sequence=['#10b981'],
                         labels={'gelir': 'Aylık Gelir ($)', 'month': ''})
            fig.update_layout(**PLOTLY_THEME, height=300,
                              title=dict(text='Aylık Gelir', font=dict(color='#f1f5f9')))
            st.plotly_chart(fig, use_container_width=True)
        fig = px.line(event_monthly, x='month', y='count', color='event_type',
                      color_discrete_sequence=['#00d4ff','#7c3aed','#10b981','#f59e0b'],
                      labels={'count': 'İşlem Sayısı', 'month': '', 'event_type': 'Event'})
        fig.update_layout(**PLOTLY_THEME, height=300,
                          title=dict(text='Aylık Event Tipi Trendi', font=dict(color='#f1f5f9')))
        st.plotly_chart(fig, use_container_width=True)

    with tab3:
        col1, col2 = st.columns(2)
        with col1:
            fig = px.bar(hourly, x='hour', y='count', color='count',
                         color_continuous_scale='Blues',
                         labels={'count': 'Satış Sayısı', 'hour': 'Saat'})
            fig.update_layout(**PLOTLY_THEME, height=300, coloraxis_showscale=False,
                              title=dict(text='Saate Göre Satış Dağılımı', font=dict(color='#f1f5f9')))
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            day_order = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
            dow['dayofweek'] = pd.Categorical(dow['dayofweek'], categories=day_order, ordered=True)
            dow = dow.sort_values('dayofweek')
            fig = px.bar(dow, x='dayofweek', y='count', color='count',
                         color_continuous_scale='Purples',
                         labels={'count': 'Satış Sayısı', 'dayofweek': ''})
            fig.update_layout(**PLOTLY_THEME, height=300, coloraxis_showscale=False,
                              title=dict(text='Güne Göre Satış Dağılımı', font=dict(color='#f1f5f9')))
            st.plotly_chart(fig, use_container_width=True)

# ══════════════════════════════════════════
# SAYFA 4: CHURN TAHMİNİ
# ══════════════════════════════════════════
elif page == "Churn Tahmini":
    st.markdown("### Churn Tahmin Modeli")

    c1, c2, c3 = st.columns(3)
    churn_n = int(rfm['churn_risk'].sum())
    safe_n = len(rfm) - churn_n
    avg_risk = rfm['churn_probability'].mean()
    with c1:
        st.markdown(f"""<div class='kpi-card'>
            <div class='kpi-label'>⚠️ Churn Riski Taşıyan</div>
            <div class='kpi-value' style='color:#ef4444;'>{churn_n:,}</div>
            <div class='kpi-delta-negative'>%{churn_n/len(rfm)*100:.1f} oran</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class='kpi-card'>
            <div class='kpi-label'>✅ Aktif Müşteri</div>
            <div class='kpi-value' style='color:#10b981;'>{safe_n:,}</div>
            <div class='kpi-delta-positive'>%{safe_n/len(rfm)*100:.1f} oran</div>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""<div class='kpi-card'>
            <div class='kpi-label'>📊 Ortalama Churn Riski</div>
            <div class='kpi-value' style='color:#f59e0b;'>%{avg_risk*100:.1f}</div>
            <div class='kpi-delta-negative'>Tüm müşteriler</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("<div class='section-title'>🔍 Müşteri ID ile Churn Sorgula</div>", unsafe_allow_html=True)
        st.markdown("<p style='color:#94a3b8; font-size:0.85rem; margin-bottom:1rem;'>Gerçek müşteri verisine dayalı tahmin yapar.</p>", unsafe_allow_html=True)
        user_id_input = st.number_input("Müşteri ID",
            min_value=int(rfm['user_id'].min()),
            max_value=int(rfm['user_id'].max()),
            value=int(rfm['user_id'].iloc[0]))

        if st.button("🔮 Churn Riskini Hesapla"):
            result = rfm[rfm['user_id'] == user_id_input]
            if len(result) == 0:
                st.error("Müşteri bulunamadı.")
            else:
                r = result.iloc[0]
                prob = r['churn_probability']
                pred = r['churn_risk']
                st.markdown(f"""
                <div style='background:#16161f; border:1px solid #1e2035; border-radius:10px; padding:1rem; margin:1rem 0;'>
                    <div style='display:grid; grid-template-columns:1fr 1fr; gap:0.8rem;'>
                        <div><span style='color:#94a3b8; font-size:0.75rem; text-transform:uppercase; letter-spacing:0.08em;'>Segment</span>
                        <div style='color:#f1f5f9; font-weight:600; margin-top:0.2rem;'>{r['segment']}</div></div>
                        <div><span style='color:#94a3b8; font-size:0.75rem; text-transform:uppercase; letter-spacing:0.08em;'>RFM Skoru</span>
                        <div style='color:#00d4ff; font-family:JetBrains Mono; font-weight:700; margin-top:0.2rem;'>{int(r['rfm_score'])}/12</div></div>
                        <div><span style='color:#94a3b8; font-size:0.75rem; text-transform:uppercase; letter-spacing:0.08em;'>Alışveriş Sıklığı</span>
                        <div style='color:#f1f5f9; font-weight:600; margin-top:0.2rem;'>{int(r['frequency'])}x</div></div>
                        <div><span style='color:#94a3b8; font-size:0.75rem; text-transform:uppercase; letter-spacing:0.08em;'>Toplam Harcama</span>
                        <div style='color:#f1f5f9; font-weight:600; margin-top:0.2rem;'>${r['monetary']:.1f}</div></div>
                        <div><span style='color:#94a3b8; font-size:0.75rem; text-transform:uppercase; letter-spacing:0.08em;'>Recency</span>
                        <div style='color:#f1f5f9; font-weight:600; margin-top:0.2rem;'>{int(r['recency'])} gün önce</div></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                if pred == 1:
                    st.markdown(f"""<div style='background:rgba(239,68,68,0.12); border:1px solid rgba(239,68,68,0.4);
                    border-radius:10px; padding:1.4rem;'>
                    <div style='color:#ff6b6b; font-size:1.2rem; font-weight:700;'>⚠️ YÜKSEK CHURN RİSKİ</div>
                    <div style='color:#e2e8f0; margin-top:0.6rem;'>Kayıp olasılığı:
                    <span style='color:#ff6b6b; font-family:JetBrains Mono; font-weight:700; font-size:1.1rem;'> %{prob*100:.1f}</span></div>
                    <div style='color:#cbd5e1; margin-top:0.8rem; font-size:0.85rem;'>👉 Hemen %25 indirim kuponu gönder!</div>
                    </div>""", unsafe_allow_html=True)
                else:
                    st.markdown(f"""<div style='background:rgba(16,185,129,0.12); border:1px solid rgba(16,185,129,0.4);
                    border-radius:10px; padding:1.4rem;'>
                    <div style='color:#34d399; font-size:1.2rem; font-weight:700;'>✅ DÜŞÜK CHURN RİSKİ</div>
                    <div style='color:#e2e8f0; margin-top:0.6rem;'>Aktif kalma olasılığı:
                    <span style='color:#34d399; font-family:JetBrains Mono; font-weight:700; font-size:1.1rem;'> %{(1-prob)*100:.1f}</span></div>
                    <div style='color:#cbd5e1; margin-top:0.8rem; font-size:0.85rem;'>👉 Sadakat programına dahil et!</div>
                    </div>""", unsafe_allow_html=True)

                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown("<div class='section-title'>Bu Müşteri Neden Riskli?</div>", unsafe_allow_html=True)
                st.markdown("<p style='color:#94a3b8; font-size:0.83rem; margin-bottom:1rem;'>SHAP analizi — hangi özellikler bu tahmini yönlendiriyor?</p>", unsafe_allow_html=True)
                try:
                    import shap
                    features = ['frequency', 'monetary', 'avg_order_value', 'is_one_time', 'high_spender', 'rfm_score_norm']
                    avg_order_val = r['monetary'] / r['frequency']
                    is_one_time = 1 if r['frequency'] == 1 else 0
                    high_spender = 1 if r['monetary'] > rfm['monetary'].quantile(0.75) else 0
                    rfm_score_norm = r['rfm_score'] / 12
                    inp = pd.DataFrame([[r['frequency'], r['monetary'], avg_order_val,
                        is_one_time, high_spender, rfm_score_norm]], columns=features)
                    explainer = shap.TreeExplainer(model)
                    shap_vals = explainer.shap_values(inp)
                    if isinstance(shap_vals, list):
                        sv = shap_vals[1][0]
                    elif len(np.array(shap_vals).shape) == 3:
                        sv = np.array(shap_vals)[0, :, 1]
                    else:
                        sv = shap_vals[0]
                    shap_df = pd.DataFrame({'Feature': features, 'Deger': inp.values[0], 'SHAP': sv})
                    shap_df = shap_df.sort_values('SHAP', key=abs, ascending=False)
                    colors = ['#ef4444' if x > 0 else '#10b981' for x in shap_df['SHAP']]
                    fig_s = go.Figure(go.Bar(x=shap_df['SHAP'], y=shap_df['Feature'],
                        orientation='h', marker_color=colors,
                        text=[f"{v:.3f}" for v in shap_df['SHAP']],
                        textposition='outside', textfont=dict(color='#f1f5f9')))
                    fig_s.add_vline(x=0, line_color='#475569', line_width=1)
                    fig_s.update_layout(**PLOTLY_THEME, height=280)
                    fig_s.update_layout(xaxis_title='SHAP Degeri (+ churn riskini artiriyor, - azaltiyor)',
                                        yaxis=dict(autorange='reversed'))
                    st.plotly_chart(fig_s, use_container_width=True)
                    top = shap_df.iloc[0]
                    direction = "artırıyor" if top['SHAP'] > 0 else "azaltıyor"
                    st.markdown(f"""<div class='insight-box' style='color:#f1f5f9;'>
                    En etkili faktör: <strong>{top['Feature']}</strong> (değer: <strong>{top['Deger']:.2f}</strong>)
                    — bu müşterinin churn riskini en çok <strong>{direction}</strong>.
                    </div>""", unsafe_allow_html=True)
                except Exception as e:
                    st.info(f"SHAP analizi yüklenemedi: {e}")

    with col2:
        st.markdown("<div class='section-title'>Churn Olasılığı Dağılımı</div>", unsafe_allow_html=True)
        fig = px.histogram(rfm, x='churn_probability', nbins=50, color_discrete_sequence=['#7c3aed'])
        fig.add_vline(x=0.5, line_dash="dash", line_color="#ef4444",
                      annotation_text="Risk Eşiği", annotation_font_color="#f87171")
        fig.update_layout(**PLOTLY_THEME, height=320,
                          xaxis_title="Churn Olasılığı", yaxis_title="Müşteri Sayısı")
        st.plotly_chart(fig, use_container_width=True)
        churn_seg = rfm.groupby('segment').agg(
            churn_oran=('churn_risk','mean'), toplam=('user_id','count')).reset_index()
        churn_seg['churn_pct'] = (churn_seg['churn_oran']*100).round(1)
        fig2 = px.bar(churn_seg, x='segment', y='churn_pct',
                      color='segment', color_discrete_map=SEGMENT_COLORS,
                      labels={'churn_pct':'Churn Oranı (%)', 'segment':''}, text='churn_pct')
        fig2.update_traces(texttemplate='%{text}%', textposition='outside', textfont=dict(color='#f1f5f9'))
        fig2.update_layout(**PLOTLY_THEME, height=280, showlegend=False)
        st.plotly_chart(fig2, use_container_width=True)

    st.divider()
    st.markdown("<div class='section-title'>⚡ En Yüksek Riskli 20 Müşteri</div>", unsafe_allow_html=True)
    high_risk = rfm[rfm['churn_risk']==1].nlargest(20, 'churn_probability')[
        ['user_id','segment','frequency','monetary','recency','churn_probability']].copy()
    high_risk['churn_probability'] = (high_risk['churn_probability']*100).round(1).astype(str) + '%'
    high_risk['monetary'] = high_risk['monetary'].round(1).astype(str) + '$'
    high_risk.columns = ['Müşteri ID','Segment','Sıklık','Harcama','Recency (gün)','Risk']
    st.dataframe(high_risk, use_container_width=True, hide_index=True)

# ══════════════════════════════════════════
# SAYFA 5: KAMPANYA SİMÜLATÖRÜ (YENİ)
# ══════════════════════════════════════════
elif page == "Kampanya Simülatörü":
    st.markdown("### Kampanya Simülatörü")
    st.markdown("<div style='color:#94a3b8; margin-bottom:1.5rem;'>Churn riski taşıyan müşterilere yönelik kampanya ROI'sini CLV bazlı olarak hesapla.</div>", unsafe_allow_html=True)

    @st.cache_data
    def load_clv_camp():
        return pd.read_csv('data/clv_data.csv')
    clv_data = load_clv_camp()

    col1, col2 = st.columns([1, 1.4])

    with col1:
        st.markdown("<div class='section-title'>Kampanya Parametreleri</div>", unsafe_allow_html=True)
        target_segments = st.multiselect("Hedef Segmentler",
            list(SEGMENT_COLORS.keys()),
            default=['Uykudakiler', 'Kayıp Adayları'])
        discount_rate   = st.slider("İndirim Oranı (%)", 0, 50, 20)
        conversion_rate = st.slider("Tahmini Dönüşüm Oranı (%)", 1, 50, 15)
        cost_per_contact = st.slider("Müşteri Başına İletişim Maliyeti ($)", 0.0, 5.0, 0.05, step=0.05,
                                    help="E-posta ~$0.01-0.05 | SMS ~$0.05-0.20 | Direkt posta ~$1-3")
        avg_clv_mult    = st.slider("Kurtarılan Müşteri CLV Çarpanı", 0.1, 1.0, 0.5, step=0.05,
                                    help="Kurtarılan müşterinin CLV'sinin ne kadarını realize edebileceğimiz tahmini.")

    with col2:
        st.markdown("<div class='section-title'>📊 Simülasyon Sonuçları</div>", unsafe_allow_html=True)

        if target_segments:
            # Sadece churn_risk=1 müşterileri hedefle
            churn_targets = rfm[(rfm['segment'].isin(target_segments)) & (rfm['churn_risk'] == 1)]
            target_count  = len(churn_targets)
            converted     = int(target_count * conversion_rate / 100)

            # CLV'yi merge et
            merged = churn_targets.merge(clv_data[['user_id','predicted_clv']], on='user_id', how='left')
            avg_clv   = merged['predicted_clv'].mean() if len(merged) > 0 else 0
            avg_spend = merged['monetary'].mean() if len(merged) > 0 else 0

            # Hesaplamalar
            saved_rev     = converted * avg_clv * avg_clv_mult
            contact_cost  = target_count * cost_per_contact
            discount_cost = converted * avg_spend * (discount_rate / 100)
            total_cost    = contact_cost + discount_cost
            net_gain      = saved_rev - total_cost
            roi           = (net_gain / total_cost * 100) if total_cost > 0 else 0
            breakeven     = int(total_cost / (avg_clv * avg_clv_mult)) if (avg_clv * avg_clv_mult) > 0 else 0

            # 8 metrik kartı
            metrics_data = [
                ("🎯 Hedef Müşteri (Churn)", f"{target_count:,}", "#94a3b8"),
                ("✅ Tahmini Dönüşüm", f"{converted:,}", "#00d4ff"),
                ("💡 Ort. CLV", f"${avg_clv:,.0f}", "#7c3aed"),
                ("💰 Kurtarılan Gelir (CLV)", f"${saved_rev:,.0f}", "#10b981"),
                ("📬 İletişim Maliyeti", f"${contact_cost:,.0f}", "#f59e0b"),
                ("🏷️ İndirim Maliyeti", f"${discount_cost:,.0f}", "#f59e0b"),
                ("💸 Toplam Maliyet", f"${total_cost:,.0f}", "#ef4444"),
                ("📈 Net Kazanç", f"${net_gain:,.0f}", "#10b981" if net_gain >= 0 else "#ef4444"),
            ]
            c1, c2 = st.columns(2)
            for i, (label, val, color) in enumerate(metrics_data):
                col = c1 if i % 2 == 0 else c2
                with col:
                    st.markdown(f"""<div class='kpi-card' style='margin-bottom:0.5rem; padding:0.8rem;'>
                    <div style='display:flex; justify-content:space-between; align-items:center;'>
                        <span style='color:#94a3b8; font-size:0.78rem;'>{label}</span>
                        <span style='font-family:JetBrains Mono; color:{color}; font-weight:700; font-size:0.95rem;'>{val}</span>
                    </div></div>""", unsafe_allow_html=True)

            # ROI kutusu
            roi_color = "#10b981" if roi >= 0 else "#ef4444"
            roi_icon  = "🚀" if roi >= 100 else ("✅" if roi >= 0 else "⚠️")
            st.markdown(f"""<div style='background:{"rgba(16,185,129,0.1)" if roi>=0 else "rgba(239,68,68,0.1)"};
            border:1px solid {"rgba(16,185,129,0.35)" if roi>=0 else "rgba(239,68,68,0.35)"};
            border-radius:10px; padding:1rem 1.2rem; margin:0.5rem 0;'>
            <div style='display:flex; justify-content:space-between; align-items:center;'>
                <span style='color:#f1f5f9; font-weight:600;'>{roi_icon} Tahmini ROI</span>
                <span style='font-family:JetBrains Mono; color:{roi_color}; font-weight:700; font-size:1.3rem;'>%{roi:.0f}</span>
            </div>
            </div>""", unsafe_allow_html=True)

            # Break-even insight
            st.markdown(f"""<div class='insight-box' style='color:#f1f5f9;'>
            🎯 Break-even için en az <strong>{breakeven:,}</strong> müşteri kazanılmalı.
            Mevcut tahmin: <strong>{converted:,}</strong> dönüşüm
            {'— ✅ hedef aşılıyor!' if converted >= breakeven else '— ⚠️ hedefin altında.'}
            </div>""", unsafe_allow_html=True)
        else:
            st.info("En az bir segment seçin.")

    if target_segments and target_count > 0:
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)

        with col1:
            # Senaryo karşılaştırması
            st.markdown("<div class='section-title'>📊 İndirim Senaryosu Karşılaştırması</div>", unsafe_allow_html=True)
            scenarios = []
            for d in [10, 20, 30, 40, 50]:
                s_disc  = converted * avg_spend * (d / 100)
                s_cost  = contact_cost + s_disc
                s_gain  = saved_rev - s_cost
                s_roi   = (s_gain / s_cost * 100) if s_cost > 0 else 0
                scenarios.append({'İndirim': f'%{d}', 'Net Kazanç': round(s_gain), 'ROI': round(s_roi)})
            sc_df = pd.DataFrame(scenarios)

            fig_sc = go.Figure()
            fig_sc.add_trace(go.Bar(
                x=sc_df['İndirim'], y=sc_df['Net Kazanç'],
                name='Net Kazanç ($)',
                marker_color=['#10b981' if v >= 0 else '#ef4444' for v in sc_df['Net Kazanç']],
                text=[f"${v:,.0f}" for v in sc_df['Net Kazanç']],
                textposition='outside', textfont=dict(color='#f1f5f9'), yaxis='y'
            ))
            fig_sc.add_trace(go.Scatter(
                x=sc_df['İndirim'], y=sc_df['ROI'],
                name='ROI (%)', mode='lines+markers',
                line=dict(color='#f59e0b', width=2),
                marker=dict(size=8, color='#f59e0b'), yaxis='y2'
            ))
            fig_sc.update_layout(**PLOTLY_THEME, height=320)
            fig_sc.update_layout(
                yaxis=dict(title='Net Kazanç ($)', gridcolor='#1e2035', tickfont=dict(color='#cbd5e1')),
                yaxis2=dict(title='ROI (%)', overlaying='y', side='right',
                            gridcolor='rgba(0,0,0,0)', tickfont=dict(color='#f59e0b')),
                legend=dict(orientation='h', y=-0.2, x=0.5, xanchor='center',
                            bgcolor='rgba(0,0,0,0)', font=dict(color='#f1f5f9'))
            )
            st.plotly_chart(fig_sc, use_container_width=True)

        with col2:
            # Öncelikli hedef müşteriler
            st.markdown("<div class='section-title'>🎯 Öncelikli Hedef Müşteriler</div>", unsafe_allow_html=True)
            st.markdown("<p style='color:#94a3b8; font-size:0.83rem; margin-bottom:0.8rem;'>Yüksek CLV + churn riskli — en değerli aksiyon grubu.</p>", unsafe_allow_html=True)
            priority = merged.nlargest(15, 'predicted_clv')[
                ['user_id','segment','predicted_clv','churn_probability','monetary']].copy()
            priority['predicted_clv']    = priority['predicted_clv'].round(0).astype(int).astype(str) + '$'
            priority['churn_probability'] = (priority['churn_probability']*100).round(1).astype(str) + '%'
            priority['monetary']          = priority['monetary'].round(1).astype(str) + '$'
            priority.columns = ['ID','Segment','CLV','Churn Riski','Harcama']
            st.dataframe(priority, use_container_width=True, hide_index=True)

# ══════════════════════════════════════════
# SAYFA 6: MÜŞTERİ SORGULAMA
# ══════════════════════════════════════════
elif page == "Müşteri Sorgulama":
    st.markdown("### Müşteri Detay Sorgulama")

    col1, col2 = st.columns([1, 2])
    with col1:
        user_id = st.number_input("Müşteri ID", min_value=int(rfm['user_id'].min()),
                                   max_value=int(rfm['user_id'].max()),
                                   value=int(rfm['user_id'].iloc[0]))
        search = st.button("🔍 Müşteriyi Sorgula")

    if search:
        result = rfm[rfm['user_id'] == user_id]
        if len(result) == 0:
            st.error("Müşteri bulunamadı.")
        else:
            r = result.iloc[0]
            seg = r['segment']
            badge = {'Şampiyonlar':'badge-champion','Sadık Müşteriler':'badge-loyal',
                     'Uykudakiler':'badge-sleeping','Kayıp Adayları':'badge-lost'}[seg]
            st.markdown(f"""
            <div class='kpi-card' style='margin-bottom:1.5rem;'>
                <div style='display:flex; justify-content:space-between; align-items:center;'>
                    <div>
                        <div style='color:#94a3b8; font-size:0.75rem; text-transform:uppercase; letter-spacing:0.08em;'>Müşteri</div>
                        <div style='font-family:JetBrains Mono; font-size:1.4rem; color:#f1f5f9; font-weight:700;'>{int(r['user_id'])}</div>
                    </div>
                    <span class='badge {badge}'>{seg}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

            c1, c2, c3, c4 = st.columns(4)
            for col, label, val in [
                (c1, "Recency", f"{int(r['recency'])} gün"),
                (c2, "Frequency", f"{int(r['frequency'])}x"),
                (c3, "Monetary", f"${r['monetary']:.1f}"),
                (c4, "RFM Skoru", f"{int(r['rfm_score'])}/12"),
            ]:
                with col:
                    st.markdown(f"""<div class='kpi-card'>
                        <div class='kpi-label'>{label}</div>
                        <div class='kpi-value' style='font-size:1.4rem;'>{val}</div>
                    </div>""", unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            churn_prob = r['churn_probability']
            risk_color = '#ef4444' if churn_prob > 0.5 else '#10b981'
            st.markdown(f"""
            <div class='insight-box'>
                <strong>Churn Riski:</strong>
                <span style='color:{risk_color}; font-family:JetBrains Mono; font-weight:700;'>%{churn_prob*100:.1f}</span>
                {"— ⚠️ Yüksek risk! Acil müdahale önerilir." if churn_prob > 0.5 else "— ✅ Düşük risk, müşteri aktif."}
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br><div class='section-title'>Rastgele Müşteri Örnekleri</div>", unsafe_allow_html=True)
    sample = rfm.sample(10)[['user_id','segment','recency','frequency','monetary','rfm_score','churn_probability']].copy()
    sample['churn_probability'] = (sample['churn_probability']*100).round(1).astype(str) + '%'
    sample['monetary'] = sample['monetary'].round(1).astype(str) + '$'
    sample.columns = ['ID','Segment','Recency','Sıklık','Harcama','RFM Skoru','Churn Riski']
    st.dataframe(sample, use_container_width=True, hide_index=True)

# ══════════════════════════════════════════
# SAYFA 7: COHORT ANALİZİ
# ══════════════════════════════════════════
elif page == "Cohort Analizi":
    st.markdown("### Cohort Analizi — Müşteri Retention")
    st.markdown("<div style='color:#94a3b8; margin-bottom:1.5rem;'>Her ay gelen yeni müşterilerin sonraki aylarda ne kadarı geri döndüğünü gösterir.</div>", unsafe_allow_html=True)

    @st.cache_data
    def load_cohort():
        retention = pd.read_csv('data/cohort_retention.csv', index_col=0)
        counts    = pd.read_csv('data/cohort_counts.csv', index_col=0)
        return retention, counts

    retention, counts = load_cohort()
    retention.columns = [f'Ay {int(float(c))}' for c in retention.columns]
    counts.columns    = [f'Ay {int(float(c))}' for c in counts.columns]

    avg_month1   = retention['Ay 1'].mean()
    avg_month2   = retention['Ay 2'].mean()
    best_cohort  = retention['Ay 1'].idxmax()

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"""<div class='kpi-card'>
            <div class='kpi-label'>📅 Ort. 1. Ay Retention</div>
            <div class='kpi-value' style='color:#00d4ff;'>%{avg_month1:.1f}</div>
            <div class='kpi-delta-negative'>İlk ayda geri dönen</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class='kpi-card'>
            <div class='kpi-label'>📅 Ort. 2. Ay Retention</div>
            <div class='kpi-value' style='color:#7c3aed;'>%{avg_month2:.1f}</div>
            <div class='kpi-delta-negative'>İkinci ayda geri dönen</div>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""<div class='kpi-card'>
            <div class='kpi-label'>🏆 En İyi Cohort</div>
            <div class='kpi-value' style='color:#10b981; font-size:1.3rem;'>{best_cohort}</div>
            <div class='kpi-delta-positive'>En yüksek 1. ay retention</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>🌡️ Retention Isı Haritası (%)</div>", unsafe_allow_html=True)
    st.markdown("<p style='color:#94a3b8; font-size:0.85rem; margin-bottom:1rem;'>Ay 0 = müşterinin ilk alışveriş ayı (%100). Sonraki aylar geri dönüş oranını gösterir.</p>", unsafe_allow_html=True)

    text_values = [[f'{v:.1f}%' if not np.isnan(v) else '' for v in row] for row in retention.values]
    fig = go.Figure(data=go.Heatmap(
        z=retention.values, x=retention.columns.tolist(), y=retention.index.tolist(),
        colorscale=[[0.0,'#0a0a0f'],[0.1,'#1a1a3e'],[0.2,'#2d1b69'],
                    [0.4,'#7c3aed'],[0.7,'#00d4ff'],[1.0,'#10b981']],
        text=text_values, texttemplate='%{text}', textfont=dict(color='white', size=13),
        hoverongaps=False, showscale=True,
        colorbar=dict(tickfont=dict(color='#f1f5f9'),
                      title=dict(text='Retention %', font=dict(color='#f1f5f9')))
    ))
    fig.update_layout(**PLOTLY_THEME, height=350)
    fig.update_layout(
        xaxis=dict(title='Cohort Ayı', tickfont=dict(color='#f1f5f9'), gridcolor='#1e2035'),
        yaxis=dict(title='İlk Alışveriş Ayı', tickfont=dict(color='#f1f5f9'), gridcolor='#1e2035')
    )
    st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div class='section-title'>📉 Retention Trendi</div>", unsafe_allow_html=True)
        avg_retention = retention.mean()
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=avg_retention.index, y=avg_retention.values,
            mode='lines+markers', line=dict(color='#00d4ff', width=3),
            marker=dict(size=10, color='#7c3aed'),
            fill='tozeroy', fillcolor='rgba(0,212,255,0.08)'))
        fig2.update_layout(**PLOTLY_THEME, height=280,
                           yaxis_title='Ort. Retention (%)', xaxis_title='Cohort Ayı')
        st.plotly_chart(fig2, use_container_width=True)
    with col2:
        st.markdown("<div class='section-title'>👥 Cohort Büyüklükleri</div>", unsafe_allow_html=True)
        cohort_sizes = counts['Ay 0'].reset_index()
        cohort_sizes.columns = ['Cohort', 'Müşteri Sayısı']
        fig3 = px.bar(cohort_sizes, x='Cohort', y='Müşteri Sayısı',
                      color='Müşteri Sayısı',
                      color_continuous_scale=['#1a1a3e', '#7c3aed', '#00d4ff'])
        fig3.update_layout(**PLOTLY_THEME, height=280, coloraxis_showscale=False)
        st.plotly_chart(fig3, use_container_width=True)

    st.markdown("<div class='section-title'>💡 Önemli Bulgular</div>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"""<div class='insight-box'>
        İlk aydan sonra müşterilerin <strong>%{100-avg_month1:.0f}'i</strong> bir daha gelmedi.
        Onboarding kampanyası bu grubu hedeflemeli.
        </div>""", unsafe_allow_html=True)
    with c2:
        oct_ret = float(retention.loc['2019-10', 'Ay 1']) if '2019-10' in retention.index else 0
        st.markdown(f"""<div class='insight-box'>
        En büyük cohort <strong>Ekim 2019</strong> — 1. ay retention <strong>%{oct_ret:.1f}</strong>.
        İlk 30 gün müşteri deneyimi kritik.
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""<div class='insight-box'>
        2. aydan sonra retention <strong>%{avg_month2:.1f}</strong> seviyesinde sabitlenmiş.
        Bu oran sadık müşteri tabanını temsil ediyor.
        </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════
# SAYFA 8: CLV ANALİZİ
# ══════════════════════════════════════════
elif page == "CLV Analizi":
    st.markdown("### Customer Lifetime Value Analizi")
    st.markdown("<div style='color:#94a3b8; margin-bottom:1.5rem;'>Müşterilerin tahmini yaşam boyu değeri — önümüzdeki aylarda ne kadar gelir getireceklerini gösterir.</div>", unsafe_allow_html=True)

    @st.cache_data
    def load_clv():
        return pd.read_csv('data/clv_data.csv')
    clv = load_clv()

    c1, c2, c3, c4 = st.columns(4)
    top10_pct = clv.nlargest(int(len(clv)*0.1), 'predicted_clv')['predicted_clv'].sum() / clv['predicted_clv'].sum() * 100
    for col, label, val, color in [
        (c1, "Toplam CLV",    f"${clv['predicted_clv'].sum():,.0f}",    "#00d4ff"),
        (c2, "Ortalama CLV",  f"${clv['predicted_clv'].mean():,.0f}",   "#7c3aed"),
        (c3, "Medyan CLV",    f"${clv['predicted_clv'].median():,.0f}", "#10b981"),
        (c4, "Top %10 Katkısı", f"%{top10_pct:.0f}",                   "#f59e0b"),
    ]:
        with col:
            st.markdown(f"""<div class='kpi-card'>
                <div class='kpi-label'>{label}</div>
                <div class='kpi-value' style='color:{color}; font-size:1.5rem;'>{val}</div>
                <div class='kpi-delta-positive'>Tüm müşteriler</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div class='section-title'>CLV Dağılımı</div>", unsafe_allow_html=True)
        clv_filtered = clv[clv['predicted_clv'] < clv['predicted_clv'].quantile(0.95)]
        fig = px.histogram(clv_filtered, x='predicted_clv', nbins=50, color_discrete_sequence=['#7c3aed'])
        fig.add_vline(x=clv['predicted_clv'].mean(), line_dash="dash", line_color="#00d4ff",
                      annotation_text="Ortalama", annotation_font_color="#00d4ff")
        fig.update_layout(**PLOTLY_THEME, height=300,
                          xaxis_title="Tahmini CLV ($)", yaxis_title="Müşteri Sayısı")
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.markdown("<div class='section-title'>Segment Bazlı Ortalama CLV</div>", unsafe_allow_html=True)
        seg_clv = clv.groupby('segment')['predicted_clv'].mean().reset_index()
        seg_clv.columns = ['segment', 'avg_clv']
        seg_clv = seg_clv.sort_values('avg_clv', ascending=False)
        fig2 = px.bar(seg_clv, x='segment', y='avg_clv',
                      color='segment', color_discrete_map=SEGMENT_COLORS,
                      labels={'avg_clv': 'Ortalama CLV ($)', 'segment': ''}, text='avg_clv')
        fig2.update_traces(texttemplate='$%{text:.0f}', textposition='outside', textfont=dict(color='#f1f5f9'))
        fig2.update_layout(**PLOTLY_THEME, height=300, showlegend=False)
        st.plotly_chart(fig2, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div class='section-title'>Segment CLV Payı</div>", unsafe_allow_html=True)
        seg_total = clv.groupby('segment')['predicted_clv'].sum().reset_index()
        fig3 = px.pie(seg_total, values='predicted_clv', names='segment',
                      color='segment', color_discrete_map=SEGMENT_COLORS, hole=0.55)
        fig3.update_layout(**PLOTLY_THEME, height=300)
        fig3.update_layout(legend=dict(orientation='h', y=-0.1, x=0.5, xanchor='center',
                                       bgcolor='rgba(0,0,0,0)', font=dict(color='#f1f5f9')))
        st.plotly_chart(fig3, use_container_width=True)
    with col2:
        st.markdown("<div class='section-title'>En Değerli 10 Müşteri</div>", unsafe_allow_html=True)
        top10 = clv.nlargest(10, 'predicted_clv')[
            ['user_id', 'segment', 'monetary', 'frequency', 'predicted_clv']].copy()
        top10['predicted_clv'] = top10['predicted_clv'].round(1).astype(str) + '$'
        top10['monetary']      = top10['monetary'].round(1).astype(str) + '$'
        top10.columns = ['ID', 'Segment', 'Toplam Harcama', 'Sıklık', 'Tahmini CLV']
        st.dataframe(top10, use_container_width=True, hide_index=True)

    st.markdown("<div class='section-title'>CLV & Churn Riski Matrisi</div>", unsafe_allow_html=True)
    st.markdown("<p style='color:#94a3b8; font-size:0.85rem; margin-bottom:1rem;'>Sağ üst köşe = yüksek değerli ama riskli müşteriler — Öncelikli aksiyon grubu!</p>", unsafe_allow_html=True)
    clv_churn = clv.merge(rfm[['user_id', 'churn_probability']], on='user_id', how='left')
    sample = clv_churn.sample(min(2000, len(clv_churn)), random_state=42)
    fig4 = px.scatter(sample, x='churn_probability', y='predicted_clv',
                      color='segment', color_discrete_map=SEGMENT_COLORS, opacity=0.6,
                      labels={'churn_probability':'Churn Riski','predicted_clv':'Tahmini CLV ($)','segment':'Segment'})
    fig4.add_vline(x=0.5, line_dash="dash", line_color="#ef4444",
                   annotation_text="Risk Eşiği", annotation_font_color="#ef4444")
    fig4.update_layout(**PLOTLY_THEME, height=350)
    st.plotly_chart(fig4, use_container_width=True)

    high_value_at_risk = clv_churn[(clv_churn['churn_probability'] > 0.5) &
                                    (clv_churn['predicted_clv'] > clv['predicted_clv'].quantile(0.75))]
    champ_clv = seg_clv[seg_clv['segment']=='Şampiyonlar']['avg_clv'].values
    champ_val = champ_clv[0] if len(champ_clv) > 0 else 0

    st.markdown("<div class='section-title'>Önemli Bulgular</div>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"""<div class='insight-box'>
        Müşterilerin en değerli <strong>%10'u</strong> toplam CLV'nin
        <strong>%{top10_pct:.0f}'ini</strong> oluşturuyor. Bu grubu elde tutmak kritik.
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class='insight-box'>
        <strong>{len(high_value_at_risk):,}</strong> yüksek değerli müşteri churn riski taşıyor.
        Bu grup için acil retention kampanyası önerilir.
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""<div class='insight-box'>
        Şampiyonların ortalama CLV'si <strong>${champ_val:.0f}</strong>.
        Sadık müşterilere kıyasla çok daha yüksek değer üretiyorlar.
        </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════
# SAYFA 9: MODEL PERFORMANSI
# ══════════════════════════════════════════
elif page == "Model Performansı":
    st.markdown("### Churn Model Performans Analizi")
    st.markdown("<div style='color:#94a3b8; margin-bottom:1.5rem;'>Random Forest modelinin detaylı performans metrikleri ve açıklanabilirlik analizleri.</div>", unsafe_allow_html=True)

    import json

    @st.cache_data
    def load_model_data():
        with open('data/model_metrics.json', 'r') as f:
            metrics = json.load(f)
        roc      = pd.read_csv('data/roc_curve.csv')
        lift     = pd.read_csv('data/lift_curve.csv')
        pr       = pd.read_csv('data/pr_curve.csv')
        shap_m   = pd.read_csv('data/shap_mean.csv')
        feat_imp = pd.read_csv('data/feature_importance.csv')
        return metrics, roc, lift, pr, shap_m, feat_imp

    metrics, roc, lift, pr, shap_m, feat_imp = load_model_data()
    cm = metrics['confusion_matrix']

    c1, c2, c3, c4, c5 = st.columns(5)
    for col, label, val, color in [
        (c1, "Accuracy",  f"%{metrics['accuracy']*100:.1f}",  "#00d4ff"),
        (c2, "Precision", f"%{metrics['precision']*100:.1f}", "#7c3aed"),
        (c3, "Recall",    f"%{metrics['recall']*100:.1f}",    "#10b981"),
        (c4, "F1 Score",  f"%{metrics['f1']*100:.1f}",        "#f59e0b"),
        (c5, "ROC AUC",   f"{metrics['roc_auc']:.3f}",        "#ef4444"),
    ]:
        with col:
            st.markdown(f"""<div class='kpi-card'>
                <div class='kpi-label'>{label}</div>
                <div class='kpi-value' style='color:{color}; font-size:1.6rem;'>{val}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div class='section-title'>Confusion Matrix</div>", unsafe_allow_html=True)
        cm_data   = [[cm['tn'], cm['fp']], [cm['fn'], cm['tp']]]
        cm_labels = [['TN', 'FP'], ['FN', 'TP']]
        cm_text   = [[f"{cm_labels[i][j]}<br>{cm_data[i][j]:,}" for j in range(2)] for i in range(2)]
        fig_cm = go.Figure(data=go.Heatmap(
            z=cm_data, x=['Tahmin: Aktif', 'Tahmin: Churn'], y=['Gerçek: Aktif', 'Gerçek: Churn'],
            colorscale=[[0,'#1a1a3e'],[0.5,'#7c3aed'],[1,'#10b981']],
            text=cm_text, texttemplate='%{text}', textfont=dict(color='white', size=14), showscale=False))
        fig_cm.update_layout(**PLOTLY_THEME, height=300)
        st.plotly_chart(fig_cm, use_container_width=True)
        mape_val = metrics.get('mape', 0)
        st.markdown(f"""<div class='insight-box' style='color:#f1f5f9;'>
        <strong>MAPE:</strong> %{mape_val:.1f} — Model tahmin olasılıkları gerçek etiketlerden
        ortalama <strong>%{mape_val:.1f}</strong> sapıyor.
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='section-title'>ROC Eğrisi (AUC = {:.3f})</div>".format(metrics['roc_auc']), unsafe_allow_html=True)
        fig_roc = go.Figure()
        fig_roc.add_trace(go.Scatter(x=roc['fpr'], y=roc['tpr'], mode='lines',
            name=f"Model (AUC={metrics['roc_auc']:.3f})",
            line=dict(color='#00d4ff', width=3),
            fill='tozeroy', fillcolor='rgba(0,212,255,0.08)'))
        fig_roc.add_trace(go.Scatter(x=[0,1], y=[0,1], mode='lines', name='Rastgele Tahmin',
            line=dict(color='#475569', width=1, dash='dash')))
        fig_roc.update_layout(**PLOTLY_THEME, height=300,
                              xaxis_title='False Positive Rate', yaxis_title='True Positive Rate')
        st.plotly_chart(fig_roc, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div class='section-title'>Lift Eğrisi</div>", unsafe_allow_html=True)
        fig_lift = go.Figure()
        fig_lift.add_trace(go.Bar(x=lift['decile_label'].astype(str)+'%', y=lift['lift'],
            marker_color='#7c3aed', text=lift['lift'].round(2),
            texttemplate='%{text}x', textposition='outside', textfont=dict(color='#f1f5f9')))
        fig_lift.add_hline(y=1.0, line_dash='dash', line_color='#475569',
                           annotation_text='Baseline', annotation_font_color='#94a3b8')
        fig_lift.update_layout(**PLOTLY_THEME, height=300,
                               xaxis_title='Müşteri Yüzdesi (En Riskli → En Az Riskli)', yaxis_title='Lift')
        st.plotly_chart(fig_lift, use_container_width=True)
    with col2:
        st.markdown("<div class='section-title'>Precision-Recall Eğrisi</div>", unsafe_allow_html=True)
        fig_pr = go.Figure()
        fig_pr.add_trace(go.Scatter(x=pr['recall'], y=pr['precision'], mode='lines',
            line=dict(color='#10b981', width=3),
            fill='tozeroy', fillcolor='rgba(16,185,129,0.08)'))
        fig_pr.update_layout(**PLOTLY_THEME, height=300,
                             xaxis_title='Recall', yaxis_title='Precision')
        st.plotly_chart(fig_pr, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div class='section-title'>SHAP — Feature Etki Analizi</div>", unsafe_allow_html=True)
        st.markdown("<p style='color:#94a3b8; font-size:0.83rem; margin-bottom:0.8rem;'>Modelin tahmin yaparken her feature'a ne kadar ağırlık verdiğini gösterir.</p>", unsafe_allow_html=True)
        fig_shap = go.Figure(go.Bar(
            x=shap_m['shap_value'], y=shap_m['feature'], orientation='h',
            marker=dict(color=shap_m['shap_value'],
                        colorscale=[[0,'#1a1a3e'],[0.5,'#7c3aed'],[1,'#00d4ff']], showscale=False),
            text=shap_m['shap_value'].round(3), textposition='outside', textfont=dict(color='#f1f5f9')))
        fig_shap.update_layout(**PLOTLY_THEME, height=300)
        fig_shap.update_layout(xaxis_title='Ortalama |SHAP Degeri|', yaxis=dict(autorange='reversed'))
        st.plotly_chart(fig_shap, use_container_width=True)
    with col2:
        st.markdown("<div class='section-title'>Feature Importance</div>", unsafe_allow_html=True)
        fig_fi = go.Figure(go.Bar(
            x=feat_imp['importance'], y=feat_imp['feature'], orientation='h',
            marker=dict(color=feat_imp['importance'],
                        colorscale=[[0,'#1a1a3e'],[0.5,'#f59e0b'],[1,'#10b981']], showscale=False),
            text=(feat_imp['importance']*100).round(1), texttemplate='%{text}%',
            textposition='outside', textfont=dict(color='#f1f5f9')))
        fig_fi.update_layout(**PLOTLY_THEME, height=300)
        fig_fi.update_layout(xaxis_title='Onem Skoru', yaxis=dict(autorange='reversed'))
        st.plotly_chart(fig_fi, use_container_width=True)

    st.markdown("<div class='section-title'>Önemli Bulgular</div>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    top_shap = shap_m.iloc[0]
    lift_top = lift.iloc[0]['lift']
    with c1:
        st.markdown(f"""<div class='insight-box' style='color:#f1f5f9;'>
        En etkili feature <strong>{top_shap['feature']}</strong> — SHAP değeri
        <strong>{top_shap['shap_value']:.3f}</strong>. Modelin tahminlerini
        en çok bu değişken yönlendiriyor.
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class='insight-box' style='color:#f1f5f9;'>
        Model en riskli <strong>%10 müşteriyi</strong> rastgele tahminden
        <strong>{lift_top:.1f}x</strong> daha iyi tespit ediyor.
        Kampanya bütçesi bu gruba odaklanmalı.
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""<div class='insight-box' style='color:#f1f5f9;'>
        Model <strong>{cm['fp']:,}</strong> aktif müşteriyi yanlışlıkla riskli gördü (FP),
        <strong>{cm['fn']:,}</strong> churn müşteriyi kaçırdı (FN).
        FN maliyeti genellikle daha yüksektir.
        </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════
# SAYFA 10: GELİŞMİŞ ANALİZ
# Aksiyon Penceresi + Mevsimsellik
# ══════════════════════════════════════════
elif page == "Gelişmiş Analiz":
    st.markdown("### Gelişmiş Analiz")

    import json, os

    tab1, tab2 = st.tabs(["🎯 Aksiyon Penceresi", "🌊 Mevsimsellik"])

    # ─────────────────────────────────────
    # TAB 1: AKSİYON PENCERESİ
    # ─────────────────────────────────────
    with tab1:
        st.markdown("<div style='color:#94a3b8; margin-bottom:1.5rem;'>Model kaç gün önceden churn riskini tespit edebiliyor? Hangi recency eşiğinde aksiyon almalısın?</div>", unsafe_allow_html=True)

        @st.cache_data
        def load_action_data():
            aw  = pd.read_csv('data/action_window.csv')
            rt  = pd.read_csv('data/recency_threshold.csv')
            src = pd.read_csv('data/segment_recency_churn.csv')
            return aw, rt, src

        try:
            aw, rt, src = load_action_data()

            # KPI'lar
            # Churn'ün %50'yi ilk aştığı recency günü
            threshold_day = rt[rt['avg_churn_prob'] >= 0.5]['recency_day'].min()
            early_warn    = rt[rt['avg_churn_prob'] >= 0.3]['recency_day'].min()
            high_risk_day = rt[rt['avg_churn_prob'] >= 0.7]['recency_day'].min()

            c1, c2, c3 = st.columns(3)
            with c1:
                st.markdown(f"""<div class='kpi-card'>
                    <div class='kpi-label'>⚡ Erken Uyarı Eşiği</div>
                    <div class='kpi-value' style='color:#f59e0b;'>{int(early_warn)} gün</div>
                    <div class='kpi-delta-negative'>Risk %30'u aşıyor</div>
                </div>""", unsafe_allow_html=True)
            with c2:
                st.markdown(f"""<div class='kpi-card'>
                    <div class='kpi-label'>⚠️ Kritik Eşik</div>
                    <div class='kpi-value' style='color:#ef4444;'>{int(threshold_day)} gün</div>
                    <div class='kpi-delta-negative'>Risk %50'yi aşıyor</div>
                </div>""", unsafe_allow_html=True)
            with c3:
                st.markdown(f"""<div class='kpi-card'>
                    <div class='kpi-label'>🔴 Yüksek Risk Eşiği</div>
                    <div class='kpi-value' style='color:#7c3aed;'>{int(high_risk_day)} gün</div>
                    <div class='kpi-delta-negative'>Risk %70'i aşıyor</div>
                </div>""", unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("<div class='section-title'>📈 Recency → Churn Riski İlişkisi</div>", unsafe_allow_html=True)
                st.markdown("<p style='color:#94a3b8; font-size:0.83rem; margin-bottom:0.8rem;'>Son alışverişten kaç gün geçtikçe churn riski nasıl değişiyor?</p>", unsafe_allow_html=True)

                # Smoothed line
                rt_smooth = rt[rt['recency_day'] <= 150].copy()
                rt_smooth['smooth'] = rt_smooth['avg_churn_prob'].rolling(5, min_periods=1, center=True).mean()

                fig_aw = go.Figure()
                fig_aw.add_trace(go.Scatter(
                    x=rt_smooth['recency_day'], y=rt_smooth['smooth'] * 100,
                    mode='lines', name='Churn Riski (%)',
                    line=dict(color='#00d4ff', width=3),
                    fill='tozeroy', fillcolor='rgba(0,212,255,0.08)'
                ))
                # Eşik çizgileri
                fig_aw.add_hline(y=30, line_dash='dot', line_color='#f59e0b',
                                 annotation_text='%30 Erken Uyarı',
                                 annotation_font_color='#f59e0b')
                fig_aw.add_hline(y=50, line_dash='dash', line_color='#ef4444',
                                 annotation_text='%50 Kritik',
                                 annotation_font_color='#ef4444')
                fig_aw.add_hline(y=70, line_dash='dot', line_color='#7c3aed',
                                 annotation_text='%70 Yüksek Risk',
                                 annotation_font_color='#a78bfa')
                fig_aw.update_layout(**PLOTLY_THEME, height=320,
                                     xaxis_title='Son Alışverişten Geçen Gün (Recency)',
                                     yaxis_title='Ortalama Churn Riski (%)')
                st.plotly_chart(fig_aw, use_container_width=True)

            with col2:
                st.markdown("<div class='section-title'>🪣 Recency Bucket — Risk Dağılımı</div>", unsafe_allow_html=True)
                st.markdown("<p style='color:#94a3b8; font-size:0.83rem; margin-bottom:0.8rem;'>Hangi recency aralığında kaç müşteri var ve ortalama riski nedir?</p>", unsafe_allow_html=True)

                fig_bucket = go.Figure()
                bar_colors = ['#10b981' if v < 30 else ('#f59e0b' if v < 50 else '#ef4444')
                              for v in aw['avg_churn_prob_pct']]
                fig_bucket.add_trace(go.Bar(
                    x=aw['recency_bucket'].astype(str),
                    y=aw['avg_churn_prob_pct'],
                    marker_color=bar_colors,
                    text=aw['avg_churn_prob_pct'],
                    texttemplate='%{text}%',
                    textposition='outside',
                    textfont=dict(color='#f1f5f9'),
                    name='Churn Riski (%)'
                ))
                fig_bucket.update_layout(**PLOTLY_THEME, height=320,
                                         xaxis_title='Recency Aralığı (gün)',
                                         yaxis_title='Ort. Churn Riski (%)')
                st.plotly_chart(fig_bucket, use_container_width=True)

            # Segment bazlı aksiyon penceresi
            st.markdown("<div class='section-title'>🎯 Segment Bazlı Aksiyon Penceresi</div>", unsafe_allow_html=True)
            fig_seg = go.Figure()
            seg_colors = [SEGMENT_COLORS.get(s, '#94a3b8') for s in src['segment']]
            fig_seg.add_trace(go.Bar(
                x=src['segment'], y=src['avg_recency'],
                marker_color=seg_colors,
                text=src['avg_recency'].round(0),
                texttemplate='%{text} gün',
                textposition='outside',
                textfont=dict(color='#f1f5f9'),
                name='Ort. Recency (gün)'
            ))
            fig_seg.add_trace(go.Scatter(
                x=src['segment'],
                y=src['avg_churn_prob'] * 100,
                mode='lines+markers',
                name='Ort. Churn Riski (%)',
                line=dict(color='#f59e0b', width=2),
                marker=dict(size=10, color='#f59e0b'),
                yaxis='y2'
            ))
            fig_seg.update_layout(**PLOTLY_THEME, height=300)
            fig_seg.update_layout(
                yaxis=dict(title='Ort. Recency (gün)', gridcolor='#1e2035', tickfont=dict(color='#cbd5e1')),
                yaxis2=dict(title='Churn Riski (%)', overlaying='y', side='right',
                            gridcolor='rgba(0,0,0,0)', tickfont=dict(color='#f59e0b')),
                legend=dict(orientation='h', y=-0.25, x=0.5, xanchor='center',
                            bgcolor='rgba(0,0,0,0)', font=dict(color='#f1f5f9'))
            )
            st.plotly_chart(fig_seg, use_container_width=True)

            # Insight kutuları
            st.markdown("<div class='section-title'>💡 Önemli Bulgular</div>", unsafe_allow_html=True)
            c1, c2, c3 = st.columns(3)
            with c1:
                st.markdown(f"""<div class='insight-box' style='color:#f1f5f9;'>
                Model, son alışverişten <strong>{int(early_warn)} gün</strong> sonra
                erken uyarı verebiliyor. Bu pencerede müdahale en az maliyetli.
                </div>""", unsafe_allow_html=True)
            with c2:
                st.markdown(f"""<div class='insight-box' style='color:#f1f5f9;'>
                Churn riski <strong>~60. günde</strong> ani sıçrama yapıyor — bu modelin
                churn tanımından kaynaklanıyor (recency &gt; 60). Kampanyayı
                <strong>45-55. günler</strong> arasında başlatmak ideal:
                risk henüz düşükken müdahale en az maliyetli.
                </div>""", unsafe_allow_html=True)
            with c3:
                st.markdown(f"""<div class='insight-box' style='color:#f1f5f9;'>
                <strong>{int(high_risk_day)} günden</strong> sonra risk %70'i aşıyor.
                Bu noktada müşteri neredeyse kayıp — kampanya maliyeti artar.
                </div>""", unsafe_allow_html=True)

        except FileNotFoundError:
            st.warning("⚠️ Veri dosyaları bulunamadı. Lütfen önce `python src/advanced_analysis.py` komutunu çalıştır.")

    # ─────────────────────────────────────
    # TAB 2: MEVSİMSELLİK
    # ─────────────────────────────────────
    with tab2:
        st.markdown("<div style='color:#94a3b8; margin-bottom:1.5rem;'>Satışlardaki haftalık, aylık ve saatlik mevsimsel pattern'ler.</div>", unsafe_allow_html=True)

        @st.cache_data
        def load_season_data():
            hm   = pd.read_csv('data/seasonality_heatmap.csv')
            ms   = pd.read_csv('data/monthly_seasonality.csv')
            ts   = pd.read_csv('data/timeslot_revenue.csv')
            wp   = pd.read_csv('data/weekly_pattern.csv')
            with open('data/seasonality_summary.json') as f:
                summary = json.load(f)
            return hm, ms, ts, wp, summary

        try:
            hm, ms, ts, wp, summary = load_season_data()

            # KPI'lar
            c1, c2, c3, c4 = st.columns(4)
            for col, label, val, color in [
                (c1, "🏆 Peak Gün",    summary['peak_day'],           "#00d4ff"),
                (c2, "⏰ Peak Saat",   f"{summary['peak_hour']}:00",  "#7c3aed"),
                (c3, "📅 Peak Ay",     summary['peak_month'],         "#10b981"),
                (c4, "📦 Top. Sipariş", f"{summary['total_orders']:,}", "#f59e0b"),
            ]:
                with col:
                    st.markdown(f"""<div class='kpi-card'>
                        <div class='kpi-label'>{label}</div>
                        <div class='kpi-value' style='color:{color}; font-size:1.3rem;'>{val}</div>
                    </div>""", unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            # Gün × Saat ısı haritası
            st.markdown("<div class='section-title'>🌡️ Gün × Saat Gelir Isı Haritası</div>", unsafe_allow_html=True)
            st.markdown("<p style='color:#94a3b8; font-size:0.83rem; margin-bottom:0.8rem;'>Haftanın hangi günü, hangi saatte en çok satış yapılıyor?</p>", unsafe_allow_html=True)

            day_order = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
            hm['dayofweek'] = pd.Categorical(hm['dayofweek'], categories=day_order, ordered=True)
            hm_pivot = hm.pivot_table(index='dayofweek', columns='hour', values='revenue', aggfunc='sum')
            hm_pivot = hm_pivot.reindex(day_order)

            fig_hm = go.Figure(data=go.Heatmap(
                z=hm_pivot.values,
                x=[f"{h}:00" for h in hm_pivot.columns],
                y=['Pzt','Sal','Çar','Per','Cum','Cmt','Paz'],
                colorscale=[
                    [0.0, '#0a0a0f'], [0.2, '#1a1a3e'],
                    [0.5, '#7c3aed'], [0.8, '#00d4ff'], [1.0, '#10b981']
                ],
                showscale=True,
                colorbar=dict(tickfont=dict(color='#f1f5f9'),
                              title=dict(text='Gelir ($)', font=dict(color='#f1f5f9')))
            ))
            fig_hm.update_layout(**PLOTLY_THEME, height=320,
                                  xaxis_title='Saat', yaxis_title='Gün')
            st.plotly_chart(fig_hm, use_container_width=True)

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("<div class='section-title'>📅 Aylık Gelir Trendi</div>", unsafe_allow_html=True)
                fig_ms = go.Figure()
                fig_ms.add_trace(go.Bar(
                    x=ms['month'], y=ms['revenue'],
                    marker_color='#7c3aed', opacity=0.85,
                    name='Gelir ($)',
                    text=ms['revenue'].apply(lambda x: f"${x:,.0f}"),
                    textposition='outside', textfont=dict(color='#f1f5f9', size=10)
                ))
                fig_ms.add_trace(go.Scatter(
                    x=ms['month'], y=ms['avg_order_value'],
                    mode='lines+markers', name='Ort. Sipariş ($)',
                    line=dict(color='#00d4ff', width=2),
                    marker=dict(size=8), yaxis='y2'
                ))
                fig_ms.update_layout(**PLOTLY_THEME, height=300)
                fig_ms.update_layout(
                    yaxis=dict(title='Toplam Gelir ($)', gridcolor='#1e2035', tickfont=dict(color='#cbd5e1')),
                    yaxis2=dict(title='Ort. Sipariş ($)', overlaying='y', side='right',
                                gridcolor='rgba(0,0,0,0)', tickfont=dict(color='#00d4ff')),
                    legend=dict(orientation='h', y=-0.3, x=0.5, xanchor='center',
                                bgcolor='rgba(0,0,0,0)', font=dict(color='#f1f5f9'))
                )
                st.plotly_chart(fig_ms, use_container_width=True)

            with col2:
                st.markdown("<div class='section-title'>⏰ Gün İçi Zaman Dilimi Analizi</div>", unsafe_allow_html=True)
                ts_agg = ts.groupby('time_slot')['revenue'].sum().reset_index()
                ts_agg = ts_agg.sort_values('revenue', ascending=False)
                slot_colors = {'Akşam (18-24)':'#7c3aed','Öğle (12-18)':'#00d4ff',
                               'Sabah (06-12)':'#10b981','Gece (00-06)':'#475569'}
                fig_ts = px.pie(ts_agg, values='revenue', names='time_slot',
                                color='time_slot',
                                color_discrete_map=slot_colors, hole=0.55)
                fig_ts.update_traces(textfont_size=12, textfont_color='white',
                                     marker=dict(line=dict(color='#0a0a0f', width=2)))
                fig_ts.update_layout(**PLOTLY_THEME, height=300)
                fig_ts.update_layout(legend=dict(orientation='h', y=-0.15, x=0.5, xanchor='center',
                                                  bgcolor='rgba(0,0,0,0)', font=dict(color='#f1f5f9')))
                st.plotly_chart(fig_ts, use_container_width=True)

            # Ayın haftası pattern
            st.markdown("<div class='section-title'>📆 Ayın Haftası — Gelir Dağılımı</div>", unsafe_allow_html=True)
            st.markdown("<p style='color:#94a3b8; font-size:0.83rem; margin-bottom:0.8rem;'>Ayın 1. haftası mı daha yoğun, yoksa son haftası mı?</p>", unsafe_allow_html=True)
            wp_agg = wp.groupby('weekofmonth')['revenue'].mean().reset_index()
            wp_agg['week_label'] = wp_agg['weekofmonth'].apply(lambda x: f"{x}. Hafta")
            fig_wp = px.bar(wp_agg, x='week_label', y='revenue',
                            color='revenue',
                            color_continuous_scale=['#1a1a3e','#7c3aed','#00d4ff','#10b981'],
                            labels={'revenue':'Ort. Gelir ($)', 'week_label':''},
                            text='revenue')
            fig_wp.update_traces(texttemplate='$%{text:,.0f}', textposition='outside',
                                  textfont=dict(color='#f1f5f9'))
            fig_wp.update_layout(**PLOTLY_THEME, height=280, coloraxis_showscale=False)
            st.plotly_chart(fig_wp, use_container_width=True)

            # Insight kutuları
            st.markdown("<div class='section-title'>💡 Önemli Bulgular</div>", unsafe_allow_html=True)
            top_slot = ts_agg.iloc[0]['time_slot']
            top_slot_pct = ts_agg.iloc[0]['revenue'] / ts_agg['revenue'].sum() * 100
            c1, c2, c3 = st.columns(3)
            with c1:
                st.markdown(f"""<div class='insight-box' style='color:#f1f5f9;'>
                En yoğun zaman dilimi <strong>{top_slot}</strong> —
                toplam gelirin <strong>%{top_slot_pct:.0f}'ini</strong> oluşturuyor.
                Kampanyaları bu saatlere zamanla.
                </div>""", unsafe_allow_html=True)
            with c2:
                st.markdown(f"""<div class='insight-box' style='color:#f1f5f9;'>
                Peak gün <strong>{summary['peak_day']}</strong>, peak saat
                <strong>{summary['peak_hour']}:00</strong>. İndirim bildirimleri
                bu pencerede gönderilmeli.
                </div>""", unsafe_allow_html=True)
            with c3:
                best_week = wp_agg.loc[wp_agg['revenue'].idxmax(), 'week_label']
                st.markdown(f"""<div class='insight-box' style='color:#f1f5f9;'>
                Ayın <strong>{best_week}</strong> diğer haftalara göre
                daha yüksek gelir üretiyor. Büyük kampanyaları bu haftaya planla.
                </div>""", unsafe_allow_html=True)

        except FileNotFoundError:
            st.warning("⚠️ Veri dosyaları bulunamadı. Lütfen önce `python src/advanced_analysis.py` komutunu çalıştır.")



import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import joblib

# Sayfa ayarları
st.set_page_config(
    page_title="E-Commerce Analytics",
    page_icon="🛒",
    layout="wide"
)

# Veriyi yükle
@st.cache_data
def load_data():
    rfm = pd.read_csv('data/rfm_segments.csv')
    return rfm

rfm = load_data()

# Churn modelini yükle
@st.cache_resource
def load_model():
    return joblib.load('data/churn_model.pkl')

model = load_model()

# Churn tahminini ekle
rfm['churn_risk'] = model.predict(rfm[['frequency', 'monetary']])
rfm['churn_probability'] = model.predict_proba(rfm[['frequency', 'monetary']])[:, 1]

# ── BAŞLIK ──
st.title("🛒 E-Commerce Müşteri Analiz Platformu")
st.markdown("Müşteri segmentasyonu, churn riski ve gelir analizi")
st.divider()

# ── ÜST KPI KARTLARI ──
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("👥 Toplam Müşteri", f"{len(rfm):,}")

with col2:
    churn_count = rfm['churn_risk'].sum()
    st.metric("⚠️ Churn Riski", f"{churn_count:,}", 
              delta=f"%{churn_count/len(rfm)*100:.1f} oran", 
              delta_color="inverse")

with col3:
    total_revenue = rfm['monetary'].sum()
    st.metric("💰 Toplam Gelir", f"${total_revenue:,.0f}")

with col4:
    at_risk_revenue = rfm[rfm['churn_risk']==1]['monetary'].sum()
    st.metric("🚨 Risk Altındaki Gelir", f"${at_risk_revenue:,.0f}",
              delta="Kurtarılabilir",
              delta_color="inverse")

st.divider()

# ── SEGMENT ANALİZİ ──
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Müşteri Segment Dağılımı")
    segment_counts = rfm['segment'].value_counts().reset_index()
    segment_counts.columns = ['segment', 'count']
    
    colors = {
        'Şampiyonlar': '#2ecc71',
        'Sadık Müşteriler': '#3498db', 
        'Uykudakiler': '#f39c12',
        'Kayıp Adayları': '#e74c3c'
    }
    
    fig = px.pie(segment_counts, values='count', names='segment',
                 color='segment', color_discrete_map=colors,
                 hole=0.4)
    fig.update_layout(height=350)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("💰 Segment Başına Ortalama Gelir")
    segment_revenue = rfm.groupby('segment')['monetary'].mean().reset_index()
    segment_revenue.columns = ['segment', 'avg_revenue']
    segment_revenue = segment_revenue.sort_values('avg_revenue', ascending=True)
    
    fig = px.bar(segment_revenue, x='avg_revenue', y='segment',
                 orientation='h', color='segment',
                 color_discrete_map=colors)
    fig.update_layout(height=350, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

st.divider()

# ── CHURN ANALİZİ ──
col1, col2 = st.columns(2)

with col2:
    st.subheader("🔴 Churn Riski Dağılımı")
    churn_by_segment = rfm.groupby('segment')['churn_risk'].mean().reset_index()
    churn_by_segment['churn_pct'] = churn_by_segment['churn_risk'] * 100
    
    fig = px.bar(churn_by_segment, x='segment', y='churn_pct',
                 color='churn_pct',
                 color_continuous_scale='RdYlGn_r',
                 labels={'churn_pct': 'Churn Riski (%)'})
    fig.update_layout(height=350)
    st.plotly_chart(fig, use_container_width=True)

with col1:
    st.subheader("📈 RFM Dağılımı")
    fig = px.scatter(rfm, x='frequency', y='monetary',
                     color='segment', color_discrete_map=colors,
                     opacity=0.5, size_max=5,
                     labels={'frequency': 'Alışveriş Sıklığı', 
                             'monetary': 'Toplam Harcama ($)'})
    fig.update_layout(height=350)
    st.plotly_chart(fig, use_container_width=True)

st.divider()

# ── AKSIYON ÖNERİLERİ ──
st.subheader("🎯 Segment Bazlı Aksiyon Önerileri")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.success("🏆 Şampiyonlar")
    st.write("• VIP programına al")
    st.write("• Yeni ürünleri ilk göster")
    st.write("• Teşekkür e-postası gönder")

with col2:
    st.info("💛 Sadık Müşteriler")
    st.write("• Sadakat puanı ver")
    st.write("• Özel indirim kodu")
    st.write("• Ücretsiz kargo sun")

with col3:
    st.warning("😴 Uykudakiler")
    st.write("• 'Sizi özledik' e-postası")
    st.write("• Cazip kampanya sun")
    st.write("• Hatırlatma bildirimi")

with col4:
    st.error("⚠️ Kayıp Adayları")
    st.write("• Büyük indirim teklif et")
    st.write("• Acil geri kazanım")
    st.write("• Son şans kampanyası")

st.divider()

# ── MÜŞTERİ SORGULAMA ──
st.subheader("🔍 Müşteri Churn Risk Sorgulama")
st.markdown("Bir müşterinin churn riskini tahmin et:")

col1, col2 = st.columns(2)
with col1:
    frequency = st.slider("Alışveriş Sıklığı", min_value=1, max_value=100, value=5)
with col2:
    monetary = st.slider("Toplam Harcama ($)", min_value=1, max_value=5000, value=200)

if st.button("🔮 Churn Riskini Hesapla"):
    input_data = pd.DataFrame([[frequency, monetary]], 
                               columns=['frequency', 'monetary'])
    prediction = model.predict(input_data)[0]
    probability = model.predict_proba(input_data)[0][1]
    
    if prediction == 1:
        st.error(f"⚠️ YÜKSEK CHURN RİSKİ — Kayıp olasılığı: %{probability*100:.1f}")
        st.write("👉 Öneri: Bu müşteriye hemen özel indirim kuponu gönder!")
    else:
        st.success(f"✅ DÜŞÜK CHURN RİSKİ — Aktif kalma olasılığı: %{(1-probability)*100:.1f}")
        st.write("👉 Öneri: Sadakat programına dahil et, elde tut!")
# ⚡ CustomerIQ — E-Commerce Analytics Platform

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Scikit-learn](https://img.shields.io/badge/Scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)

**20 milyon satır e-ticaret verisi üzerinde uçtan uca müşteri analitik platformu.**

RFM segmentasyonu · Churn tahmini · Cohort analizi · CLV tahmini · Kampanya simülatörü

</div>

---

## 📌 Proje Hakkında

CustomerIQ, gerçek bir e-ticaret veri seti (Kaggle) üzerinde geliştirilen kapsamlı bir müşteri analitik platformudur. Ham veri işlemeden makine öğrenimi modellerine, interaktif dashboard'dan kampanya simülasyonuna kadar tam bir veri bilimi pipeline'ı içermektedir.

**Veri Seti:** [eCommerce Events History](https://www.kaggle.com/datasets/mkechinov/ecommerce-events-history-in-cosmetics-shop) — Kozmetik mağazası, Ekim 2019 – Şubat 2020  
**Boyut:** ~20.7 milyon satır · 110.518 benzersiz müşteri

---

## 🚀 Özellikler

### 📊 Genel Bakış
- 6 temel KPI kartı: toplam müşteri, churn riski, toplam gelir, risk altındaki gelir, ortalama müşteri değeri, şampiyon müşteri sayısı
- Segment dağılımı pasta grafiği
- RFM skoru dağılım histogramı

### 👥 Segment Analizi
- RFM tabanlı 4 segment: Şampiyonlar, Sadık Müşteriler, Uykudakiler, Kayıp Adayları
- Her segment için harcama, recency ve frequency dağılımları
- Segmente özel aksiyon önerileri

### 📈 Trend Analizi
- Günlük/haftalık/aylık satış ve gelir trendleri
- Saatlik ve haftalık alışveriş yoğunluk haritaları
- Event tipi bazlı trend analizi (view, cart, purchase)

### 🔮 Churn Tahmini
- Random Forest modeli ile **%91.2 doğruluk**
- Müşteri ID bazlı gerçek zamanlı churn riski sorgulama
- En yüksek riskli 20 müşteri listesi
- Segment bazlı churn oranı karşılaştırması

### 🎯 Kampanya Simülatörü
- 4 farklı kampanya tipi (e-posta, indirim kuponu, VIP erişim, geri kazanım)
- Segment bazlı hedefleme
- Tahmini dönüşüm, gelir ve ROI hesaplama
- Gerçekçi ROI uyarı sistemi

### 🔍 Müşteri Sorgulama
- Müşteri ID ile anlık RFM profili
- Churn riski göstergesi
- Rastgele müşteri örnekleme

### 🔄 Cohort Analizi
- Aylık cohort bazlı retention ısı haritası
- Retention trendi ve cohort büyüklükleri
- Otomatik iş içgörüleri

### 💰 CLV Analizi
- Gradient Boosting ile müşteri yaşam boyu değeri tahmini (**R² = 0.99**)
- Segment bazlı ortalama ve toplam CLV
- CLV & Churn riski matrisi (öncelikli aksiyon grubu tespiti)
- En değerli 10 müşteri tablosu

---

## 🛠️ Teknolojiler

| Kategori | Teknoloji |
|---|---|
| Dil | Python 3.10+ |
| Dashboard | Streamlit |
| Görselleştirme | Plotly Express, Plotly Graph Objects |
| Veri İşleme | Pandas, NumPy |
| Makine Öğrenimi | Scikit-learn (Random Forest, Gradient Boosting) |
| Model Kaydetme | Joblib |

---

## 📁 Proje Yapısı

```
ecommerce-analytics/
│
├── dashboard.py              # Ana Streamlit uygulaması (8 sayfa)
│
├── src/
│   ├── preprocess.py         # 20M satır veri ön işleme
│   ├── model.py              # Churn modeli eğitimi (RF, %91.2)
│   ├── clv.py                # CLV modeli eğitimi (GB, R²=0.99)
│   └── cohort.py             # Cohort verisi hazırlama
│
├── data/
│   ├── rfm_segments.csv      # RFM segmentasyon sonuçları
│   ├── churn_model.pkl       # Eğitilmiş churn modeli
│   ├── clv_model.pkl         # Eğitilmiş CLV modeli
│   ├── clv_data.csv          # CLV tahmin sonuçları
│   ├── cohort_retention.csv  # Cohort retention tablosu
│   ├── cohort_counts.csv     # Cohort müşteri sayıları
│   ├── daily_trend.csv       # Günlük trend verisi
│   ├── weekly_trend.csv      # Haftalık trend verisi
│   ├── monthly_trend.csv     # Aylık trend verisi
│   ├── hourly_trend.csv      # Saatlik dağılım
│   ├── dow_trend.csv         # Haftanın günü dağılımı
│   └── event_monthly.csv     # Event tipi trend verisi
│
└── requirements.txt
```

---

## ⚙️ Kurulum

```bash
# 1. Repoyu klonla
git clone https://github.com/cansuyildirimmm/ecommerce-analytics.git
cd ecommerce-analytics

# 2. Sanal ortam oluştur
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux

# 3. Bağımlılıkları yükle
pip install -r requirements.txt

# 4. Ham CSV verilerini data/ klasörüne koy
# Kaggle'dan indir: eCommerce Events History

# 5. Pipeline'ı sırayla çalıştır
python src/preprocess.py
python src/model.py
python src/cohort.py
python src/clv.py

# 6. Dashboard'u başlat
streamlit run dashboard.py
```

---

## 🤖 Model Detayları

### Churn Modeli
- **Algoritma:** Random Forest Classifier
- **Doğruluk:** %91.2
- **Etiket:** Recency > 60 gün → churn
- **Feature'lar:** frequency, monetary, avg_order_value, is_one_time, high_spender, rfm_score_norm
- **Not:** Veri sızıntısını önlemek için recency feature olarak kullanılmadı

### CLV Modeli
- **Algoritma:** Gradient Boosting Regressor
- **R² Skoru:** 0.99 · MAE: $2.78
- **Formül:** avg_order_value × purchase_rate × estimated_lifespan
- **En önemli feature:** monetary (%70)

---

## 📊 Temel Bulgular

- 110.518 müşterinin **%55'i** churn riski taşıyor
- En değerli **%10 müşteri**, toplam gelirin **%61'ini** oluşturuyor
- Ekim 2019 cohort'u en yüksek 1. ay retention'a sahip: **%18.5**
- Şampiyonlar segmentinin ortalama CLV'si **$229** — Kayıp Adayları'nın 45 katı

---

## 👩‍💻 Geliştirici

**Cansu Yıldırım**  
[![GitHub](https://img.shields.io/badge/GitHub-cansuyildirimmm-181717?style=flat&logo=github)](https://github.com/cansuyildirimmm)

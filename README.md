# ⚡ CustomerIQ — E-Commerce Analytics Platform

![Python](https://img.shields.io/badge/Python-3.10+-blue) ![Streamlit](https://img.shields.io/badge/Streamlit-1.x-red) ![Scikit-learn](https://img.shields.io/badge/Scikit--learn-ML-orange) ![Pandas](https://img.shields.io/badge/Pandas-Data-green) ![Plotly](https://img.shields.io/badge/Plotly-Viz-purple)

> 20 milyon satır e-ticaret verisi üzerinde uçtan uca müşteri analitik platformu.

**RFM segmentasyonu · Churn tahmini · Cohort analizi · CLV tahmini · Kampanya simülatörü · Mevsimsellik · Aksiyon penceresi analizi**

---

## 📌 Proje Hakkında

CustomerIQ, gerçek bir e-ticaret veri seti (Kaggle) üzerinde geliştirilen kapsamlı bir müşteri analitik platformudur. Ham veri işlemeden makine öğrenimi modellerine, interaktif dashboard'dan kampanya simülasyonuna kadar tam bir veri bilimi pipeline'ı içermektedir.

- **Veri Seti:** eCommerce Events History — Kozmetik mağazası, Ekim 2019 – Şubat 2020
- **Boyut:** ~20.7 milyon satır · 110.518 benzersiz müşteri

---

## 🚀 Özellikler (10 Sayfa)

### 📊 Genel Bakış
- 6 temel KPI kartı: toplam müşteri, churn riski, toplam gelir, risk altındaki gelir, ortalama müşteri değeri, şampiyon müşteri sayısı
- Segment dağılımı pasta grafiği & RFM dağılım scatter plot
- Segment bazlı churn riski karşılaştırması

### 👥 Segment Analizi
- RFM tabanlı 4 segment: Şampiyonlar, Sadık Müşteriler, Uykudakiler, Kayıp Adayları
- Her segment için harcama, recency ve frequency dağılımları
- Segmente özel aksiyon önerileri

### 📈 Trend Analizi
- Günlük/haftalık/aylık satış ve gelir trendleri
- Saatlik ve haftalık alışveriş yoğunluk haritaları
- Event tipi bazlı trend analizi (view, cart, purchase)

### 🔮 Churn Tahmini
- Random Forest modeli ile **%91.4 doğruluk**, ROC AUC: 0.970
- Müşteri ID bazlı gerçek zamanlı churn riski sorgulama
- **SHAP analizi** — hangi feature'ın tahmini nasıl etkilediği
- En yüksek riskli 20 müşteri listesi

### 🎯 Kampanya Simülatörü *(CLV bazlı)*
- Sadece churn_risk=1 müşterileri hedefler — gerçekçi aksiyon odaklı
- İletişim maliyeti + indirim maliyeti ayrı hesaplanır
- Net kazanç, ROI ve break-even analizi
- %10-%50 indirim senaryo karşılaştırması (çift eksenli grafik)
- Öncelikli hedef müşteriler tablosu (yüksek CLV + churn riskli)

### 🔍 Müşteri Sorgulama
- Müşteri ID ile anlık RFM profili
- Churn riski göstergesi & aksiyon önerisi
- Rastgele müşteri örnekleme

### 🔄 Cohort Analizi
- Aylık cohort bazlı retention ısı haritası
- Retention trendi ve cohort büyüklükleri
- Otomatik iş içgörüleri

### 💰 CLV Analizi
- Gradient Boosting ile müşteri yaşam boyu değeri tahmini (R² = 0.99)
- Segment bazlı ortalama ve toplam CLV
- CLV & Churn riski matrisi (öncelikli aksiyon grubu tespiti)
- En değerli 10 müşteri tablosu

### 🛡️ Model Performansı
- Confusion Matrix, ROC eğrisi (AUC = 0.970), Lift eğrisi, Precision-Recall eğrisi
- SHAP feature etki analizi (global)
- Feature importance karşılaştırması

### 🔬 Gelişmiş Analiz *(Yeni)*
**Aksiyon Penceresi:**
- Recency → churn riski ilişkisi (kaç günde risk eşiği aşılıyor?)
- Erken uyarı (%30), kritik (%50) ve yüksek risk (%70) eşikleri
- Segment bazlı aksiyon penceresi karşılaştırması
- İdeal kampanya zamanı: **45-55. günler** (risk artmadan önce müdahale)

**Mevsimsellik:**
- Gün × Saat gelir ısı haritası
- Aylık gelir trendi & ortalama sipariş değeri
- Gün içi zaman dilimi analizi (sabah/öğle/akşam/gece)
- Ayın haftası bazlı gelir dağılımı

---

## 🛠️ Teknolojiler

| Kategori | Teknoloji |
|---|---|
| Dil | Python 3.10+ |
| Dashboard | Streamlit |
| Görselleştirme | Plotly Express, Plotly Graph Objects |
| Veri İşleme | Pandas, NumPy |
| Makine Öğrenimi | Scikit-learn (Random Forest, Gradient Boosting) |
| Model Açıklanabilirlik | SHAP |
| Model Kaydetme | Joblib |

---

## 📁 Proje Yapısı

```
ecommerce-analytics/
│
├── dashboard.py              # Ana Streamlit uygulaması (10 sayfa)
│
├── src/
│   ├── preprocess.py         # 20M satır veri ön işleme
│   ├── model.py              # Churn modeli eğitimi (RF, %91.4, AUC=0.970)
│   ├── clv.py                # CLV modeli eğitimi (GB, R²=0.99)
│   ├── cohort.py             # Cohort verisi hazırlama
│   └── advanced_analysis.py  # Aksiyon penceresi & mevsimsellik analizi
│
├── data/
│   ├── rfm_segments.csv      # RFM segmentasyon sonuçları
│   ├── churn_model.pkl       # Eğitilmiş churn modeli
│   ├── clv_model.pkl         # Eğitilmiş CLV modeli
│   ├── clv_data.csv          # CLV tahmin sonuçları
│   ├── model_metrics.json    # Model performans metrikleri
│   ├── roc_curve.csv         # ROC eğrisi verisi
│   ├── lift_curve.csv        # Lift eğrisi verisi
│   ├── pr_curve.csv          # Precision-Recall eğrisi
│   ├── shap_mean.csv         # SHAP ortalama değerleri
│   ├── feature_importance.csv
│   ├── cohort_retention.csv
│   ├── cohort_counts.csv
│   ├── action_window.csv         # Aksiyon penceresi analizi
│   ├── recency_threshold.csv     # Recency-churn eşik verisi
│   ├── segment_recency_churn.csv
│   ├── seasonality_heatmap.csv   # Gün×saat gelir ısı haritası
│   ├── monthly_seasonality.csv
│   ├── weekly_pattern.csv
│   ├── timeslot_revenue.csv
│   └── seasonality_summary.json
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
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux

# 3. Bağımlılıkları yükle
pip install -r requirements.txt

# 4. Ham CSV verilerini data/ klasörüne koy
# Kaggle: eCommerce Events History
# Dosyalar: 2019-Oct.csv, 2019-Nov.csv, 2019-Dec.csv, 2020-Jan.csv, 2020-Feb.csv

# 5. Pipeline'ı sırayla çalıştır
python src/preprocess.py
python src/model.py
python src/cohort.py
python src/clv.py
python src/advanced_analysis.py   # Aksiyon penceresi & mevsimsellik

# 6. Dashboard'u başlat
streamlit run dashboard.py
```

---

## 🤖 Model Detayları

### Churn Modeli
| Metrik | Değer |
|---|---|
| Algoritma | Random Forest Classifier |
| Accuracy | %91.4 |
| Precision | 0.931 |
| Recall | 0.913 |
| F1 Score | 0.921 |
| ROC AUC | 0.970 |
| Churn Etiketi | Recency > 60 gün → churn |
| Feature'lar | frequency, monetary, avg_order_value, is_one_time, high_spender, rfm_score_norm |

> **Not:** Veri sızıntısını önlemek için `recency` feature olarak kullanılmadı. En etkili feature: `rfm_score_norm` (SHAP: 0.301)

### CLV Modeli
| Metrik | Değer |
|---|---|
| Algoritma | Gradient Boosting Regressor |
| R² Skoru | 0.990 |
| MAE | $2.78 |
| Formül | avg_order_value × purchase_rate × estimated_lifespan |
| En önemli feature | monetary (%70) |

---

## 📊 Temel Bulgular

- 110.518 müşterinin **%55'i** churn riski taşıyor
- En değerli **%10 müşteri**, toplam gelirin **%61'ini** oluşturuyor
- Ekim 2019 cohort'u en yüksek 1. ay retention'a sahip: **%18.5**
- Şampiyonlar segmentinin ortalama CLV'si **$229** — Kayıp Adayları'nın 45 katı
- Churn riski **60. günde** ani sıçrama yapıyor — ideal kampanya penceresi: **45-55. günler**
- Peak satış günü **Perşembe**, peak saat **11:00**, peak ay **Kasım 2019** (Black Friday etkisi)
- En yoğun alışveriş dilimi **Sabah (06-12)** — toplam gelirin **%34'ü**

---

## 👩‍💻 Geliştirici

**Cansu Yıldırım**          
[GitHub](https://github.com/cansuyildirimmm)

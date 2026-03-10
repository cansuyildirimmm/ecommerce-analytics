"""
advanced_analysis.py
Sayfa 10: Gelişmiş Analiz
- Aksiyon Penceresi: Model kaç gün önceden churn'ü öngörüyor?
- Mevsimsellik: Satışlardaki seasonal pattern'ler
"""

import pandas as pd
import numpy as np
from pathlib import Path

DATA_DIR = Path("data")

def compute_action_window(rfm_path="data/rfm_segments.csv",
                           model_path="data/churn_model.pkl"):
    """
    Recency değerine göre churn öngörü penceresi analizi.
    - Churn label: recency > 60 gün
    - Kaç gün ÖNCE modelin riski artırmaya başladığını gösterir
    """
    import joblib

    rfm = pd.read_csv(rfm_path)
    model = joblib.load(model_path)

    rfm = rfm.copy()
    rfm['avg_order_value'] = rfm['monetary'] / rfm['frequency']
    rfm['is_one_time']     = (rfm['frequency'] == 1).astype(int)
    rfm['high_spender']    = (rfm['monetary'] > rfm['monetary'].quantile(0.75)).astype(int)
    rfm['rfm_score_norm']  = rfm['rfm_score'] / 12

    features = ['frequency', 'monetary', 'avg_order_value',
                'is_one_time', 'high_spender', 'rfm_score_norm']
    rfm['churn_probability'] = model.predict_proba(rfm[features])[:, 1]
    rfm['churn_risk']        = model.predict(rfm[features])

    # Recency bucket'lara böl (10'ar günlük)
    rfm['recency_bucket'] = pd.cut(rfm['recency'],
        bins=[0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 120, 150, 999],
        labels=['0-10','11-20','21-30','31-40','41-50','51-60',
                '61-70','71-80','81-90','91-120','121-150','150+'])

    action_window = rfm.groupby('recency_bucket', observed=True).agg(
        avg_churn_prob=('churn_probability', 'mean'),
        churn_rate=('churn_risk', 'mean'),
        customer_count=('user_id', 'count')
    ).reset_index()
    action_window['avg_churn_prob_pct'] = (action_window['avg_churn_prob'] * 100).round(1)
    action_window['churn_rate_pct']     = (action_window['churn_rate'] * 100).round(1)

    action_window.to_csv(DATA_DIR / "action_window.csv", index=False)
    print(f"✅ action_window.csv kaydedildi ({len(action_window)} satır)")

    # Segment bazlı ortalama recency - churn ilişkisi
    seg_recency = rfm.groupby('segment').agg(
        avg_recency=('recency', 'mean'),
        avg_churn_prob=('churn_probability', 'mean'),
        churn_rate=('churn_risk', 'mean'),
        count=('user_id', 'count')
    ).reset_index().round(2)
    seg_recency.to_csv(DATA_DIR / "segment_recency_churn.csv", index=False)
    print(f"✅ segment_recency_churn.csv kaydedildi")

    # Recency thresholds: hangi recency'den itibaren risk %50'yi aşıyor?
    threshold_df = rfm.groupby('recency')['churn_probability'].mean().reset_index()
    threshold_df.columns = ['recency_day', 'avg_churn_prob']
    threshold_df = threshold_df.sort_values('recency_day')
    threshold_df.to_csv(DATA_DIR / "recency_threshold.csv", index=False)
    print(f"✅ recency_threshold.csv kaydedildi")

    return action_window


def compute_seasonality():
    """
    Ham veriyi okuyup mevsimsellik analizleri üretir.
    5 aylik CSV dosyalarini birlestirerek okur.
    """
    print("📂 Ham veri okunuyor...")

    files = [
        "data/2019-Oct.csv",
        "data/2019-Nov.csv",
        "data/2019-Dec.csv",
        "data/2020-Jan.csv",
        "data/2020-Feb.csv",
    ]

    chunks = []
    for fpath in files:
        print(f"  -> {fpath} okunuyor...")
        for chunk in pd.read_csv(fpath, chunksize=500_000,
                                  parse_dates=['event_time']):
            chunk = chunk[chunk['event_type'] == 'purchase']
            chunks.append(chunk[['event_time', 'price', 'user_id', 'product_id']])
    df = pd.concat(chunks, ignore_index=True)
    print(f"  Toplam {len(df):,} purchase eventi yuklendi")

    df['date']        = df['event_time'].dt.date
    df['week']        = df['event_time'].dt.isocalendar().week.astype(int)
    df['month']       = df['event_time'].dt.to_period('M').astype(str)
    df['hour']        = df['event_time'].dt.hour
    df['dayofweek']   = df['event_time'].dt.day_name()
    df['weekofmonth'] = (df['event_time'].dt.day - 1) // 7 + 1

    # 1. Haftalık mevsimsellik (haftanın günü × saat ısı haritası)
    heatmap = df.groupby(['dayofweek', 'hour'])['price'].sum().reset_index()
    heatmap.columns = ['dayofweek', 'hour', 'revenue']
    heatmap.to_csv(DATA_DIR / "seasonality_heatmap.csv", index=False)
    print("✅ seasonality_heatmap.csv kaydedildi")

    # 2. Aylık mevsimsellik trendi (gelir + sipariş sayısı)
    monthly_season = df.groupby('month').agg(
        revenue=('price', 'sum'),
        orders=('user_id', 'count'),
        avg_order_value=('price', 'mean'),
        unique_customers=('user_id', 'nunique')
    ).reset_index().round(2)
    monthly_season.to_csv(DATA_DIR / "monthly_seasonality.csv", index=False)
    print("✅ monthly_seasonality.csv kaydedildi")

    # 3. Ayın haftası analizi (1. hafta vs 4. hafta farkı)
    weekly_pattern = df.groupby(['month', 'weekofmonth']).agg(
        revenue=('price', 'sum'),
        orders=('user_id', 'count')
    ).reset_index().round(2)
    weekly_pattern.to_csv(DATA_DIR / "weekly_pattern.csv", index=False)
    print("✅ weekly_pattern.csv kaydedildi")

    # 4. Günlük yoğunluk (sabah / öğle / akşam / gece dilimleri)
    def time_slot(h):
        if 6 <= h < 12:   return "Sabah (06-12)"
        elif 12 <= h < 18: return "Öğle (12-18)"
        elif 18 <= h < 24: return "Akşam (18-24)"
        else:              return "Gece (00-06)"

    df['time_slot'] = df['hour'].apply(time_slot)
    slot_data = df.groupby(['month', 'time_slot']).agg(
        revenue=('price', 'sum'),
        orders=('user_id', 'count')
    ).reset_index().round(2)
    slot_data.to_csv(DATA_DIR / "timeslot_revenue.csv", index=False)
    print("✅ timeslot_revenue.csv kaydedildi")

    # 5. Genel özet istatistikler
    peak_day   = df.groupby('dayofweek')['price'].sum().idxmax()
    peak_hour  = df.groupby('hour')['price'].sum().idxmax()
    peak_month = df.groupby('month')['price'].sum().idxmax()
    summary = {
        'peak_day':   peak_day,
        'peak_hour':  int(peak_hour),
        'peak_month': peak_month,
        'total_revenue': round(df['price'].sum(), 2),
        'total_orders':  len(df)
    }
    import json
    with open(DATA_DIR / "seasonality_summary.json", 'w') as f:
        json.dump(summary, f, indent=2)
    print(f"✅ seasonality_summary.json kaydedildi")
    print(f"   Peak gün: {peak_day}, Peak saat: {peak_hour}:00, Peak ay: {peak_month}")

    return summary


if __name__ == "__main__":
    print("=" * 50)
    print("ADIM 1: Aksiyon Penceresi Analizi")
    print("=" * 50)
    compute_action_window()

    print()
    print("=" * 50)
    print("ADIM 2: Mevsimsellik Analizi")
    print("=" * 50)
    compute_seasonality()

    print()
    print("🎉 Tüm dosyalar hazır! Şimdi dashboard'u çalıştırabilirsin.")

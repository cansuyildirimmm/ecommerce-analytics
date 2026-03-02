import pandas as pd

print("Veriler yükleniyor...")
files = [
    '../data/2019-Oct.csv', '../data/2019-Nov.csv',
    '../data/2019-Dec.csv', '../data/2020-Jan.csv', '../data/2020-Feb.csv'
]
df = pd.concat([pd.read_csv(f) for f in files], ignore_index=True)
df['event_time'] = pd.to_datetime(df['event_time'], utc=True)

# Sadece satın almaları al
purchases = df[df['event_type'] == 'purchase'].copy()

# Her müşterinin ilk alışveriş ayı (cohort)
purchases['order_month'] = purchases['event_time'].dt.to_period('M')
first_purchase = purchases.groupby('user_id')['order_month'].min().reset_index()
first_purchase.columns = ['user_id', 'cohort_month']

# Cohort bilgisini ana veriye ekle
purchases = purchases.merge(first_purchase, on='user_id')

# Cohort index hesapla (kaçıncı ayda döndü)
purchases['cohort_index'] = (
    purchases['order_month'].dt.year * 12 + purchases['order_month'].dt.month
) - (
    purchases['cohort_month'].dt.year * 12 + purchases['cohort_month'].dt.month
)

# Cohort tablosu
cohort_data = purchases.groupby(['cohort_month', 'cohort_index'])['user_id'].nunique().reset_index()
cohort_data.columns = ['cohort_month', 'cohort_index', 'user_count']

cohort_pivot = cohort_data.pivot_table(
    index='cohort_month', columns='cohort_index', values='user_count'
)

# Retention oranı (ilk aya göre yüzde)
cohort_size = cohort_pivot[0]
retention = cohort_pivot.divide(cohort_size, axis=0) * 100
retention = retention.round(1)

# Cohort aylarını string'e çevir
retention.index = retention.index.astype(str)
cohort_pivot.index = cohort_pivot.index.astype(str)

retention.to_csv('../data/cohort_retention.csv')
cohort_pivot.to_csv('../data/cohort_counts.csv')

print("✅ Cohort verisi kaydedildi!")
print("\nRetention tablosu önizleme:")
print(retention)
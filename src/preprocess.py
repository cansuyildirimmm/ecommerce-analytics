import pandas as pd

print("Veriler yükleniyor...")
files = [
    '../data/2019-Oct.csv', '../data/2019-Nov.csv',
    '../data/2019-Dec.csv', '../data/2020-Jan.csv', '../data/2020-Feb.csv'
]
df = pd.concat([pd.read_csv(f) for f in files], ignore_index=True)
df['event_time'] = pd.to_datetime(df['event_time'])

purchases = df[df['event_type'] == 'purchase'].copy()

# Günlük trend
print("Günlük trend hesaplanıyor...")
purchases['date'] = purchases['event_time'].dt.date
daily = purchases.groupby('date').agg(
    satis=('event_type','count'),
    gelir=('price','sum')
).reset_index()
daily.to_csv('../data/daily_trend.csv', index=False)

# Haftalık trend
purchases['week'] = purchases['event_time'].dt.to_period('W').astype(str)
weekly = purchases.groupby('week').agg(
    gelir=('price','sum'), satis=('event_type','count')
).reset_index()
weekly.to_csv('../data/weekly_trend.csv', index=False)

# Aylık trend
purchases['month'] = purchases['event_time'].dt.to_period('M').astype(str)
monthly = purchases.groupby('month').agg(
    gelir=('price','sum'), satis=('event_type','count')
).reset_index()
monthly.to_csv('../data/monthly_trend.csv', index=False)

# Saat & gün dağılımı
purchases['hour'] = purchases['event_time'].dt.hour
purchases['dayofweek'] = purchases['event_time'].dt.day_name()
hourly = purchases.groupby('hour').size().reset_index(name='count')
hourly.to_csv('../data/hourly_trend.csv', index=False)
daily_dow = purchases.groupby('dayofweek').size().reset_index(name='count')
daily_dow.to_csv('../data/dow_trend.csv', index=False)

# Event tipi aylık
df['month'] = df['event_time'].dt.to_period('M').astype(str)
event_monthly = df.groupby(['month','event_type']).size().reset_index(name='count')
event_monthly.to_csv('../data/event_monthly.csv', index=False)

print("✅ Tüm trend verileri kaydedildi!")
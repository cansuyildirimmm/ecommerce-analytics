import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
import joblib

print("RFM verisi yukleniyor...")
rfm = pd.read_csv('../data/rfm_segments.csv')

def compute_clv_features(rfm):
    df = rfm.copy()
    df['avg_order_value'] = df['monetary'] / df['frequency']
    df['purchase_rate'] = df['frequency'] / 5
    df['days_active'] = 150 - df['recency']
    df['days_active'] = df['days_active'].clip(lower=1)
    df['estimated_lifespan'] = np.where(
        df['recency'] < 30, 12,
        np.where(df['recency'] < 60, 6,
        np.where(df['recency'] < 90, 3, 1))
    )
    df['clv'] = df['avg_order_value'] * df['purchase_rate'] * df['estimated_lifespan']
    df['clv'] = df['clv'].clip(lower=0)
    return df

df = compute_clv_features(rfm)

print(f"Ortalama CLV: ${df['clv'].mean():.2f}")
print(f"Medyan CLV: ${df['clv'].median():.2f}")
print(f"Max CLV: ${df['clv'].max():.2f}")

features = ['frequency', 'monetary', 'recency', 'avg_order_value',
            'purchase_rate', 'days_active', 'rfm_score']
X = df[features]
y = df['clv']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = GradientBoostingRegressor(n_estimators=100, max_depth=4, random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"\nModel R2 Skoru: {r2:.3f}")
print(f"Ortalama Hata (MAE): ${mae:.2f}")

importance = pd.DataFrame({
    'feature': features,
    'importance': model.feature_importances_
}).sort_values('importance', ascending=False)
print("\nFeature Onem Sirasi:")
print(importance)

df['predicted_clv'] = model.predict(X)
df[['user_id', 'segment', 'monetary', 'frequency', 'recency',
    'rfm_score', 'clv', 'predicted_clv']].to_csv('../data/clv_data.csv', index=False)

joblib.dump(model, '../data/clv_model.pkl')
print("\nCLV modeli ve verisi kaydedildi!")
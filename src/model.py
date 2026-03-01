import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import joblib

def prepare_features(rfm):
    """Model için feature'ları hazırla"""
    # Churn etiketi: recency > 30 gün ise churn (1), değilse aktif (0)
    rfm['churn'] = (rfm['recency'] > 30).astype(int)
    
    print(f"Aktif müşteri (churn=0): {(rfm['churn']==0).sum():,}")
    print(f"Churn müşteri (churn=1): {(rfm['churn']==1).sum():,}")
    print(f"Churn oranı: %{rfm['churn'].mean()*100:.1f}")
    
    return rfm

def train_model(rfm):
    """Churn tahmin modelini eğit"""
    # Feature ve hedef değişkeni ayır
    features = ['frequency', 'monetary']
    X = rfm[features]
    y = rfm['churn']
    
    # Train/test split — %80 eğitim, %20 test
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # Modeli eğit
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Tahmin yap ve değerlendir
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"\nModel Doğruluğu: %{accuracy*100:.1f}")
    print("\nDetaylı Rapor:")
    print(classification_report(y_test, y_pred))
    
    # Feature önem sırası
    feature_importance = pd.DataFrame({
        'feature': features,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    print("\nFeature Önem Sırası:")
    print(feature_importance)
    
    return model, X_test, y_test

def save_model(model):
    """Modeli kaydet"""
    joblib.dump(model, '../data/churn_model.pkl')
    print("\n✅ Model kaydedildi: data/churn_model.pkl")

if __name__ == "__main__":
    # RFM verisini yükle
    rfm = pd.read_csv('../data/rfm_segments.csv')
    
    # Feature hazırla
    rfm = prepare_features(rfm)
    
    # Modeli eğit
    model, X_test, y_test = train_model(rfm)
    
    # Modeli kaydet
    save_model(model)
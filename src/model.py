import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import (classification_report, accuracy_score,
                              confusion_matrix, roc_curve, auc,
                              precision_recall_curve)
import joblib
import json

def prepare_features(rfm):
    rfm['churn'] = (rfm['recency'] > 60).astype(int)
    rfm['avg_order_value'] = rfm['monetary'] / rfm['frequency']
    rfm['is_one_time'] = (rfm['frequency'] == 1).astype(int)
    rfm['high_spender'] = (rfm['monetary'] > rfm['monetary'].quantile(0.75)).astype(int)
    rfm['rfm_score_norm'] = rfm['rfm_score'] / 12

    print(f"Aktif musteri (churn=0): {(rfm['churn']==0).sum():,}")
    print(f"Churn musteri (churn=1): {(rfm['churn']==1).sum():,}")
    print(f"Churn orani: %{rfm['churn'].mean()*100:.1f}")
    return rfm

def train_model(rfm):
    features = ['frequency', 'monetary', 'avg_order_value',
                'is_one_time', 'high_spender', 'rfm_score_norm']
    X = rfm[features]
    y = rfm['churn']

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
    model.fit(X_train, y_train)

    y_pred  = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]
    accuracy = accuracy_score(y_test, y_pred)

    print(f"\nModel Dogrulugu: %{accuracy*100:.1f}")
    print("\nDetayli Rapor:")
    print(classification_report(y_test, y_pred))

    # ── Confusion Matrix ──────────────────────────────────────────────
    cm = confusion_matrix(y_test, y_pred)
    tn, fp, fn, tp = cm.ravel()
    precision = tp / (tp + fp)
    recall    = tp / (tp + fn)
    f1        = 2 * precision * recall / (precision + recall)

    print(f"\nConfusion Matrix:")
    print(f"  TN={tn:,}  FP={fp:,}")
    print(f"  FN={fn:,}  TP={tp:,}")
    print(f"Precision : {precision:.3f}")
    print(f"Recall    : {recall:.3f}")
    print(f"F1        : {f1:.3f}")

    # ── ROC / AUC ────────────────────────────────────────────────────
    fpr, tpr, roc_thresholds = roc_curve(y_test, y_proba)
    roc_auc = auc(fpr, tpr)
    print(f"ROC AUC   : {roc_auc:.3f}")

    # ── MAPE (olasılık bazlı) ─────────────────────────────────────────
    # Binary sınıflandırmada MAPE: tahmin olasılığı ile gerçek etiket arasındaki sapma
    mape = np.mean(np.abs(y_test.values - y_proba)) * 100
    print(f"MAPE      : %{mape:.1f}")

    # ── Lift Curve ───────────────────────────────────────────────────
    lift_df = pd.DataFrame({'y_true': y_test.values, 'y_proba': y_proba})
    lift_df = lift_df.sort_values('y_proba', ascending=False).reset_index(drop=True)
    lift_df['decile'] = pd.qcut(lift_df.index, 10, labels=False)
    lift_data = lift_df.groupby('decile').agg(
        churn_rate=('y_true', 'mean'),
        count=('y_true', 'count')
    ).reset_index()
    baseline = y_test.mean()
    lift_data['lift'] = lift_data['churn_rate'] / baseline
    lift_data['decile_label'] = (lift_data['decile'] + 1) * 10
    print("\nLift Tablosu (ilk 3 decile):")
    print(lift_data[['decile_label', 'churn_rate', 'lift']].head(3))

    # ── Precision-Recall Curve ───────────────────────────────────────
    pr_precision, pr_recall, pr_thresholds = precision_recall_curve(y_test, y_proba)

    # ── SHAP Degerleri ───────────────────────────────────────────────
    try:
        import shap
        print("\nSHAP degerleri hesaplaniyor...")
        explainer   = shap.TreeExplainer(model)
        sample      = X_test.sample(min(1000, len(X_test)), random_state=42)
        shap_values = explainer.shap_values(sample)

        # Binary classification → class 1 (churn)
        if isinstance(shap_values, list):
            sv = shap_values[1]  # class 1
        elif len(shap_values.shape) == 3:
            sv = shap_values[:, :, 1]  # yeni SHAP formatı
        else:
            sv = shap_values

        shap_mean = pd.DataFrame({
            'feature':    features,
            'shap_value': np.abs(sv).mean(axis=0)
        }).sort_values('shap_value', ascending=False)
        print("\nSHAP Feature Etkileri:")
        print(shap_mean)

        # Her musteri icin ham SHAP degerlerini kaydet (ilk 5000)
        shap_sample = X_test.sample(min(5000, len(X_test)), random_state=42)
        sv_sample   = explainer.shap_values(shap_sample)
        if isinstance(sv_sample, list):
            sv_sample_c1 = sv_sample[1]
        elif len(sv_sample.shape) == 3:
            sv_sample_c1 = sv_sample[:, :, 1]
        else:
            sv_sample_c1 = sv_sample

        shap_df = pd.DataFrame(sv_sample_c1, columns=features)
        shap_df['user_index'] = shap_sample.index.values
        shap_df.to_csv('../data/shap_values.csv', index=False)

        shap_mean.to_csv('../data/shap_mean.csv', index=False)
        print("SHAP verileri kaydedildi.")
        shap_ok = True
    except ImportError:
        print("SHAP yuklu degil, pip install shap")
        shap_ok = False

    # ── Feature Importance ───────────────────────────────────────────
    feature_importance = pd.DataFrame({
        'feature':    features,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)
    print("\nFeature Onem Sirasi:")
    print(feature_importance)

    # ── Tum metrikleri kaydet ────────────────────────────────────────
    metrics = {
        'accuracy':  round(accuracy, 4),
        'precision': round(float(precision), 4),
        'recall':    round(float(recall), 4),
        'f1':        round(float(f1), 4),
        'roc_auc':   round(float(roc_auc), 4),
        'mape':      round(float(mape), 2),
        'confusion_matrix': {'tn': int(tn), 'fp': int(fp), 'fn': int(fn), 'tp': int(tp)},
    }
    with open('../data/model_metrics.json', 'w') as f:
        json.dump(metrics, f, indent=2)

    # ROC curve
    pd.DataFrame({'fpr': fpr, 'tpr': tpr}).to_csv('../data/roc_curve.csv', index=False)

    # Lift curve
    lift_data.to_csv('../data/lift_curve.csv', index=False)

    # Precision-Recall curve
    pr_len = min(len(pr_precision), len(pr_recall), len(pr_thresholds) + 1)
    pd.DataFrame({
        'precision': pr_precision[:pr_len],
        'recall':    pr_recall[:pr_len]
    }).to_csv('../data/pr_curve.csv', index=False)

    # Feature importance
    feature_importance.to_csv('../data/feature_importance.csv', index=False)

    print("\nTum metrik dosyalari kaydedildi!")
    return model, X_test, y_test, metrics

def save_model(model):
    joblib.dump(model, '../data/churn_model.pkl')
    print("Model kaydedildi: data/churn_model.pkl")

if __name__ == "__main__":
    rfm = pd.read_csv('../data/rfm_segments.csv')
    rfm = prepare_features(rfm)
    model, X_test, y_test, metrics = train_model(rfm)
    save_model(model)
    print("\nTamamlandi!")

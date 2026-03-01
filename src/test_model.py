import pandas as pd
import joblib

model = joblib.load('../data/churn_model.pkl')
tests = [
    [1,  10,  10.0, 1, 0, 0.25],
    [5,  50,  10.0, 0, 0, 0.42],
    [10, 100, 10.0, 0, 0, 0.58],
    [20, 200, 10.0, 0, 0, 0.67],
    [50, 500, 10.0, 0, 1, 0.83],
]
cols = ['frequency','monetary','avg_order_value','is_one_time','high_spender','rfm_score_norm']
for t in tests:
    df = pd.DataFrame([t], columns=cols)
    prob = model.predict_proba(df)[0][1]
    print(f'Sıklık={t[0]:3d}, Harcama={t[1]:5d} → Churn riski: %{prob*100:.1f}')
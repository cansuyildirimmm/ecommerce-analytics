import pandas as pd

def load_data():
    """Tüm CSV dosyalarını yükle ve birleştir"""
    files = [
        '../data/2019-Oct.csv',
        '../data/2019-Nov.csv',
        '../data/2019-Dec.csv',
        '../data/2020-Jan.csv',
        '../data/2020-Feb.csv'
    ]
    df = pd.concat([pd.read_csv(f) for f in files], ignore_index=True)
    print(f"Toplam satır: {len(df):,}")
    return df

def clean_data(df):
    """Veriyi temizle"""
    df = df.drop(columns=['category_code'], errors='ignore')
    df['brand'] = df['brand'].fillna('Bilinmeyen')
    df = df.dropna(subset=['user_session'])
    df['event_time'] = pd.to_datetime(df['event_time'])
    print(f"Temizleme sonrası satır: {len(df):,}")
    return df

def compute_rfm(df):
    """Her müşteri için RFM feature'larını hesapla"""
    purchases = df[df['event_type'] == 'purchase'].copy()
    reference_date = df['event_time'].max()
    
    rfm = purchases.groupby('user_id').agg(
        recency=('event_time', lambda x: (reference_date - x.max()).days),
        frequency=('event_time', 'count'),
        monetary=('price', 'sum')
    ).reset_index()
    
    print(f"RFM hesaplanan müşteri sayısı: {len(rfm):,}")
    return rfm

def segment_customers(rfm):
    """RFM skorlarına göre müşterileri segmentle"""
    rfm['r_score'] = pd.qcut(rfm['recency'], q=4, labels=[4,3,2,1])
    rfm['f_score'] = pd.qcut(rfm['frequency'].rank(method='first'), q=4, labels=[1,2,3,4])
    rfm['m_score'] = pd.qcut(rfm['monetary'].rank(method='first'), q=4, labels=[1,2,3,4])
    
    rfm['rfm_score'] = (rfm['r_score'].astype(int) + 
                        rfm['f_score'].astype(int) + 
                        rfm['m_score'].astype(int))
    
    def assign_segment(score):
        if score >= 10:
            return 'Şampiyonlar'
        elif score >= 8:
            return 'Sadık Müşteriler'
        elif score >= 6:
            return 'Uykudakiler'
        else:
            return 'Kayıp Adayları'
    
    rfm['segment'] = rfm['rfm_score'].apply(assign_segment)
    
    print("\nSegment dağılımı:")
    print(rfm['segment'].value_counts())
    return rfm

if __name__ == "__main__":
    df = load_data()
    df = clean_data(df)
    rfm = compute_rfm(df)
    rfm = segment_customers(rfm)
    rfm.to_csv('../data/rfm_segments.csv', index=False)
    print("\nRFM verisi kaydedildi: data/rfm_segments.csv")
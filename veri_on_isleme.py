import pandas as pd
from sklearn.preprocessing import LabelEncoder
import numpy as np

def veri_on_isleme(dosya_yolu):
    df = pd.read_csv(dosya_yolu)
    
    le = LabelEncoder()
    kategorik_sutunlar = ['Marka', 'Seri', 'Vites', 'Yakit', 'Kasa', 'Garanti', 'Agir_Hasar']
    
    for col in kategorik_sutunlar:
        df[col] = le.fit_transform(df[col].astype(str))
        
    
    
    parcalar = ["front-hood", "front-left-mudguard", "front-right-mudguard", "front-left-door", 
                "front-right-door", "rear-left-door", "rear-right-door", "rear-left-mudguard", 
                "rear-right-mudguard", "roof"]
    
    for p in parcalar:
        df[p] = 0
        
        # Eğer parça Değişenler içindeyse 3 puan
        df.loc[df['Degisenler'].str.contains(p, na=False), p] = 3
        # Eğer parça Boyalilar içindeyse 2 puan
        df.loc[df['Boyalilar'].str.contains(p, na=False), p] = 2
        # Eğer parça Lokal_Boyalilar içindeyse 1 puan
        df.loc[df['Lokal_Boyalilar'].str.contains(p, na=False), p] = 1

    df = df.drop(['Degisenler', 'Boyalilar', 'Lokal_Boyalilar', 'Model'], axis=1)
    
    return df

if __name__ == "__main__":
    hazir_df = veri_on_isleme(r"C:\Users\RESUL\OneDrive\Masaüstü\araba2\egitim_hazir_veriler.csv")
    hazir_df.to_csv("train_ready_data.csv", index=False)
    print("Veriler XGBoost eğitimi için %100 hazır hale getirildi!")
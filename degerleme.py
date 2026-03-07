import pandas as pd
import xgboost as xgb
import os

dosya_yolu = 'veri_seti.csv'

if not os.path.exists(dosya_yolu):
    print("Hata: veri_seti.csv dosyasi bulunamadi.")
    exit()

df = pd.read_csv(dosya_yolu)
df = df.dropna(subset=['Fiyat', 'Yil', 'Km'])

df_encoded = pd.get_dummies(df, columns=['Marka', 'Model'])

X = df_encoded.drop('Fiyat', axis=1)
y = df_encoded['Fiyat']

model = xgb.XGBRegressor(random_state=42) #
model.fit(X, y)

kullanici_araci = pd.DataFrame({
    'Yil': [2020],
    'Km': [55000],
    'Kaput_Boyali': [1],
    'Agir_Hasar': [0],
    'Marka_BMW': [0],
    'Marka_Fiat': [1],
    'Model_3 Serisi': [0],
    'Model_Egea': [1]
})

kullanici_araci = kullanici_araci.reindex(columns=X.columns, fill_value=0)
tahmini_fiyat = model.predict(kullanici_araci)[0]

print(f"Tahmini Piyasa Fiyati: {tahmini_fiyat:,.2f} TL")
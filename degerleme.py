import json
import os

class AutoWeightEngine:
    def __init__(self, dosya_yolu):
        self.veri_seti = self.veriyi_yukle(dosya_yolu)

    def veriyi_yukle(self, yol):
        if os.path.exists(yol):
            with open(yol, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            return []

    def katsayi_hesapla(self, yas):
        if yas <= 3: 
            return {"boya": 0.07, "degisen": 0.10, "km": 0.04}
        if yas <= 8: 
            return {"boya": 0.04, "degisen": 0.07, "km": 0.06}
        return {"boya": 0.015, "degisen": 0.03, "km": 0.09}

    def fiyat_tahmin(self, yil, km, boya, degisen):
        arac_yasi = 2026 - yil
        benzer_araclar = [a for a in self.veri_seti if a['yil'] == yil]
        
        if not benzer_araclar:
            return None

        ort_fiyat = sum(a['fiyat'] for a in benzer_araclar) / len(benzer_araclar)
        w = self.katsayi_hesapla(arac_yasi)
        
        fiyat_etkisi = (boya * w['boya']) + (degisen * w['degisen'])
        tahmini_deger = ort_fiyat * (1 - fiyat_etkisi)
        
        km_etkisi = (km / 10000) * 0.01 
        tahmini_deger = tahmini_deger * (1 - (km_etkisi * w['km']))

        return round(tahmini_deger, 2)

engine = AutoWeightEngine('veri_setim.json')
sonuc = engine.fiyat_tahmin(2024, 10000, 1, 0)
print(sonuc)
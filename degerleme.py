import json
import os

class AutoWeightEngine:
    def __init__(self, dosya_yolu):
        self.veri_seti = self.veriyi_yukle(dosya_yolu)
        self.Parca_Katsayilari = {
            "tavan": 1.0,
            "sase": 1.0,
            "direk": 0.9,
            "kaput": 0.8,
            "bagaj": 0.5,
            "kapi": 0.4,
            "camurluk": 0.3,
            "tampon": 0.2,
        }

    def veriyi_yukle(self, yol):
        if os.path.exists(yol):
            with open(yol, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            return []

    def katsayi_hesapla(self, yas):
        if yas <= 3: 
            return {"temel_hasar": 0.10, "km": 0.04}
        if yas <= 8: 
            return {"temel_hasar": 0.06, "km": 0.06}
        return {"temel_hasar": 0.02, "km": 0.09}

    def fiyat_etkisi_hesapla(self, boyananlar, degisenler):
        skor=0
        for parca in boyananlar:
            skor += self.Parca_Katsayilari.get(parca, 0) * 1.0
        for parca in degisenler:
            skor += self.Parca_Katsayilari.get(parca, 0) * 1.8
        return skor

    def fiyat_tahmin(self, yil, km, boyananlar, degisenler):
        arac_yasi = 2026 - yil
        benzer_araclar = [a for a in self.veri_seti if a['yil'] == yil]
        
        if not benzer_araclar:
            return None

        ort_fiyat = sum(a['fiyat'] for a in benzer_araclar) / len(benzer_araclar)
        w = self.katsayi_hesapla(arac_yasi)
        
        hasar_skoru = self.fiyat_etkisi_hesapla(boyananlar, degisenler)
        hasar_etkisi = hasar_skoru * w['temel_hasar']
        km_etkisi = (km/10000)* 0.01 * w['km']

        tahmini_deger = ort_fiyat * (1 - hasar_etkisi - km_etkisi)

        return round(tahmini_deger, 2)

engine = AutoWeightEngine('veri_setim.json')

# ÖRNEK SORGULAR
# 2024 Model, Tavan Boyalı (Çok düşmeli)
print("Senaryo 1 (Tavan Boyalı):", engine.fiyat_tahmin(2024, 10000, ["tavan"], []))

# 2024 Model, Tampon Boyalı (Az düşmeli)
print("Senaryo 2 (Tampon Boyalı):", engine.fiyat_tahmin(2024, 10000, ["tampon"], []))
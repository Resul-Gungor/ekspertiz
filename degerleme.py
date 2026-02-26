class ArabaDegerlemeMotoru:
    def __init__(self, veri_seti):
        self.veri_seti = veri_seti

    def dinamik_katsayi_belirle(self, arac_yasi):
        """Senin istediğin ağırlık mevzusunu çözen fonksiyon"""
        if arac_yasi <= 3:
            return {"boya": 0.08, "degisen": 0.12, "km": 0.05}
        elif arac_yasi <= 10:
            return {"boya": 0.03, "degisen": 0.06, "km": 0.08}
        else:
            return {"boya": 0.01, "degisen": 0.02, "km": 0.10}

    def tahmin_et(self, girilen_arac):
        current_year = 2026
        yas = current_year - girilen_arac['yil']
        
        benzerler = [a for a in self.veri_seti if a['yil'] == girilen_arac['yil']]
        if not benzerler:
            return "Yeterli veri yok"
            
        baz_fiyat = sum(a['fiyat'] for a in benzerler) / len(benzerler)
        
        katsayilar = self.dinamik_katsayi_belirle(yas)
        
        boya_indirimi = baz_fiyat * (girilen_arac['boyali_parca'] * katsayilar['boya'])
        degisen_indirimi = baz_fiyat * (girilen_arac['degisen_parca'] * katsayilar['degisen'])
        
        piyasa_ort_km = sum(a['km'] for a in benzerler) / len(benzerler)
        km_farki_oranı = (girilen_arac['km'] - piyasa_ort_km) / piyasa_ort_km
        km_etkisi = baz_fiyat * (km_farki_oranı * katsayilar['km'])

        tahmini_fiyat = baz_fiyat - boya_indirimi - degisen_indirimi - km_etkisi
        
        return {
            "Baz Piyasa Fiyatı": round(baz_fiyat, 2),
            "Tahmini Değer": round(tahmini_fiyat, 2),
            "Uygulanan Katsayılar": katsayilar
        }

piyasa_verisi = [
    {"yil": 2024, "fiyat": 1000000, "km": 10000},
    {"yil": 2024, "fiyat": 980000, "km": 15000},
    {"yil": 2015, "fiyat": 600000, "km": 150000},
    {"yil": 2015, "fiyat": 580000, "km": 170000}
]

motor = ArabaDegerlemeMotoru(piyasa_verisi)

benim_arabam = {"yil": 2024, "km": 12000, "boyali_parca": 1, "degisen_parca": 0}
sonuc = motor.tahmin_et(benim_arabam)
print(f"2024 Araç Tahmini: {sonuc}")
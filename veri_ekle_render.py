from accounts.models import User
from forms.models import T3PersonelAtama

veriler = [
    {"tc": "20404768528", "isim": "Emre", "soyisim": "Verim", "role": "T3 Personel", "koord": "Ulaşım Koordinatörlüğü"},
    {"tc": "69016104232", "isim": "Bahar", "soyisim": "Kılıç", "role": "T3 Personel", "koord": "İdari İşler Koordinatörlüğü"},
    {"tc": "23318519934", "isim": "Gökhan", "soyisim": "Çaylak", "role": "T3 Personel", "koord": "Eğitim Ar-Ge"},
    {"tc": "41683520324", "isim": "Burak", "soyisim": "Altıntaş", "role": "T3 Personel", "koord": "Girişim Koordinatörlüğü"},
    {"tc": "13120019760", "isim": "Ebrar", "soyisim": "Özata", "role": "T3 Personel", "koord": "Mimari Tasarım  Koordinatörlüğü"},
    {"tc": "13532141066", "isim": "Şevval", "soyisim": "Çelik", "role": "T3 Personel", "koord": "TEKNOFEST  Yarışmalar Koordinatörlüğü"},
    {"tc": "10781611746", "isim": "Fatma", "soyisim": "Nur tip", "role": "T3 Personel", "koord": "TEKNOFEST   Fuar Koordinatörlüğü"},
    {"tc": "12955082888", "isim": "Ayşenur", "soyisim": "Yavuz", "role": "T3 Personel", "koord": "Deneyap Koordinatörlüğü"},
    {"tc": "20291303482", "isim": "Havva", "soyisim": "Nur Tekin", "role": "T3 Personel", "koord": "Bilişim Koordinatörlüğü"},
    {"tc": "68443094468", "isim": "Muhammet", "soyisim": "Ali Demir", "role": "T3 Personel", "koord": "Bursiyer Koordinatörülüğü"},
    {"tc": "14268042726", "isim": "Zahide", "soyisim": "Sara Yılmaz", "role": "T3 Personel", "koord": "Kurumsal İletişim  Koordinatörlüğü"},
    {"tc": "60898371170", "isim": "Tuğçe", "soyisim": "Alemdar", "role": "T3 Personel", "koord": "Satış ve Pazarlama  Koordinatörlüğü"},
    {"tc": "17384601662", "isim": "Esma", "soyisim": "Aslan", "role": "T3 Personel", "koord": "Kurumsal Yapılanma Koordinatörlüğü"},
]

koordinatorluk_birimleri = {
    "Ulaşım Koordinatörlüğü": ["T3 Personel", "İl ve Deneyap Sorumlusu"],
    "İdari İşler Koordinatörlüğü": ["T3 Personel", "İl ve Deneyap Sorumlusu"],
    "Eğitim Ar-Ge": ["T3 Personel", "Bilim Sokağı Personel", "İl ve Deneyap Sorumlusu"],
    "Girişim Koordinatörlüğü": ["T3 Personel", "İl ve Deneyap Sorumlusu"],
    "Mimari Tasarım  Koordinatörlüğü": ["T3 Personel", "Vakıf Standı Taşeron Ekibi", "Bilim Sokağı Taşeron Ekibi", "KKTC Arş Proje Yarışması Taşeron Ekibi", "Robolig Yarışması Taşeron Ekibi", "İl ve Deneyap Sorumlusu"],
    "Yarışmalar Koordinatörlüğü": ["T3 Personel", "Yarışmacı Sayısı", "Jüri Sayısı", "İl ve Deneyap Sorumlusu"],
    "Fuar Koordinatörlüğü": ["T3 Personel", "İSG", "İtfaiye", "Branding", "Temizlik", "Sağlıkçılar", "Cleanbox", "İl ve Deneyap Sorumlusu"],
    "Deneyap Koordinatörlüğü": ["T3 Personel", "Deneyap Sorumluları", "İl ve Deneyap Sorumlusu"],
    "Bilişim Koordinatörlüğü": ["T3 Personel", "İl ve Deneyap Sorumlusu"],
    "Bursiyer Koordinatörülüğü": ["T3 Personel", "Busiyer-Gönüllü", "İl ve Deneyap Sorumlusu"],
    "Kurumsal İletişim  Koordinatörlüğü": ["T3 Personel", "PR Ajansı ve Basın", "Sosyal Medya + TF Video Çekim Ekibi(Heysemist)", "T3 Video Çekim Ekibi(ToDo)", "Kreatif Ekip(Arter)", "TRT", "Sunucu/Muhabir/TRT Koordinasyon", "İl ve Deneyap Sorumlusu"],
    "Satış ve Pazarlama  Koordinatörlüğü": ["T3 Personel", "İl ve Deneyap Sorumlusu"],
    "Kurumsal Yapılanma Koordinatörlüğü": ["T3 Personel", "İl ve Deneyap Sorumlusu"]
}

for v in veriler:
    user, created = User.objects.get_or_create(
        tc=v["tc"],
        defaults={
            "isim": v["isim"],
            "soyisim": v["soyisim"],
            "role": v["role"]
        }
    )
    if created:
        user.set_password("tfC12345")
        user.save()

    birimler = koordinatorluk_birimleri.get(v["koord"], ["T3 Personel", "İl ve Deneyap Sorumlusu"])
    for birim in birimler:
        if not T3PersonelAtama.objects.filter(kisi=user, koordinatorluk=v["koord"], birim=birim).exists():
            T3PersonelAtama.objects.create(
                kisi=user,
                koordinatorluk=v["koord"],
                birim=birim
            )

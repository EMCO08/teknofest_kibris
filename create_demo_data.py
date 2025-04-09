import os
import django
import random
from datetime import datetime, timedelta
from django.utils import timezone
from django.core.files.base import ContentFile
from PIL import Image, ImageDraw, ImageFont
import io
import base64

# Django ayarlarını yükle
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'yemek_otomasyonu.settings')
django.setup()

# Modelleri import et
from accounts.models import User
from forms.models import (
    T3PersonelAtama, 
    T3PersonelVeriler, 
    GonulluDurumVeriler, 
    GonulluSorunVeriler, 
    SorumluVeriler
)

def create_demo_image(text, width=800, height=600, color=(255, 255, 255), bg_color=(70, 130, 180)):
    """Demo resim oluştur"""
    image = Image.new('RGB', (width, height), bg_color)
    draw = ImageDraw.Draw(image)
    
    # Basit bir çerçeve çiz
    draw.rectangle([(20, 20), (width-20, height-20)], outline=(255, 255, 255), width=2)
    
    # Metin ekle
    try:
        # Font yüklemeye çalış, yoksa varsayılan font kullan
        font = ImageFont.truetype("arial.ttf", 36)
    except IOError:
        font = ImageFont.load_default()
    
    # Metni ortala
    text_width, text_height = draw.textsize(text, font=font) if hasattr(draw, 'textsize') else (width//2, height//2)
    position = ((width-text_width)//2, (height-text_height)//2)
    
    # Metni çiz
    draw.text(position, text, fill=color, font=font)
    
    # Tarih ve saat ekle
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    draw.text((20, height-40), now, fill=color, font=font)
    
    # Resmi byte olarak kaydet
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='JPEG')
    img_byte_arr.seek(0)
    
    return img_byte_arr

def create_t3personel_data():
    """T3 Personel verileri oluştur"""
    print("T3 Personel verileri oluşturuluyor...")
    
    # T3 Personel rolündeki kullanıcıları bul
    t3_users = User.objects.filter(role='t3personel')
    
    if not t3_users.exists():
        print("T3 Personel rolünde kullanıcı bulunamadı. Yeni kullanıcı oluşturuluyor...")
        # Demo T3 Personel kullanıcısı oluştur
        t3_user = User.objects.create_user(
            tc="12345678901",
            password="demo1234",
            isim="Demo",
            soyisim="T3Personel",
            role="t3personel",
            tel_no="5551234567"
        )
        t3_users = [t3_user]
    
    # Koordinatörlük ve birim seçenekleri
    koordinatorlukler = ["Afet Koordinatörlüğü", "Lojistik Koordinatörlüğü", "Saha Koordinatörlüğü"]
    birimler = {
        "Afet Koordinatörlüğü": ["Afet Yönetim", "Afet Planlama", "Acil Müdahale"],
        "Lojistik Koordinatörlüğü": ["Depo Yönetim", "Sevkiyat", "Tedarik"],
        "Saha Koordinatörlüğü": ["Saha Operasyon", "Gönüllü Yönetim", "İletişim"]
    }
    
    # Her T3 Personel için atama ve veri oluştur
    for user in t3_users:
        # Kullanıcının mevcut atamalarını kontrol et
        existing_atamalar = T3PersonelAtama.objects.filter(kisi=user)
        
        if not existing_atamalar.exists():
            # Rastgele 1-3 atama oluştur
            for _ in range(random.randint(1, 3)):
                koordinatorluk = random.choice(koordinatorlukler)
                birim = random.choice(birimler[koordinatorluk])
                
                # Aynı atama varsa atla
                if T3PersonelAtama.objects.filter(kisi=user, koordinatorluk=koordinatorluk, birim=birim).exists():
                    continue
                
                T3PersonelAtama.objects.create(
                    kisi=user,
                    koordinatorluk=koordinatorluk,
                    birim=birim
                )
                print(f"Atama oluşturuldu: {user.get_full_name()} - {koordinatorluk} - {birim}")
        
        # Kullanıcının atamalarını al
        atamalar = T3PersonelAtama.objects.filter(kisi=user)
        
        # Son 7 gün için veri oluştur
        for i in range(7):
            date = timezone.now().date() - timedelta(days=i)
            
            for atama in atamalar:
                # Aynı gün için aynı atamaya ait veri varsa atla
                if T3PersonelVeriler.objects.filter(
                    kisi=user, 
                    koordinatorluk=atama.koordinatorluk, 
                    birim=atama.birim,
                    submitteddate=date
                ).exists():
                    continue
                
                T3PersonelVeriler.objects.create(
                    kisi=user,
                    koordinatorluk=atama.koordinatorluk,
                    birim=atama.birim,
                    siparis_sayisi=random.randint(10, 500),
                    submitteddate=date,
                    submittedtime=datetime.now().time()
                )
                print(f"T3 Personel verisi oluşturuldu: {user.get_full_name()} - {date}")

def create_gonullu_durum_data():
    """Gönüllü Durum verileri oluştur"""
    print("Gönüllü Durum verileri oluşturuluyor...")
    
    # Gönüllü rolündeki kullanıcıları bul
    gonullu_users = User.objects.filter(role='gonullu')
    
    if not gonullu_users.exists():
        print("Gönüllü rolünde kullanıcı bulunamadı. Yeni kullanıcı oluşturuluyor...")
        # Demo Gönüllü kullanıcısı oluştur
        gonullu_user = User.objects.create_user(
            tc="23456789012",
            password="demo1234",
            isim="Demo",
            soyisim="Gönüllü",
            role="gonullu",
            tel_no="5559876543"
        )
        gonullu_users = [gonullu_user]
    
    # Alan seçenekleri
    alanlar = ["Deprem Bölgesi", "Çadır Kent", "Lojistik Merkez", "Yemek Dağıtım", "Sağlık Çadırı"]
    
    # Açıklama seçenekleri
    aciklamalar = [
        "Durum normal, herhangi bir sorun yok.",
        "Yemek dağıtımı sorunsuz tamamlandı.",
        "Gönüllüler koordineli çalışıyor.",
        "Hava şartları elverişli, çalışmalar devam ediyor.",
        "Malzeme sevkiyatı tamamlandı.",
        "Günlük görevler tamamlandı.",
        "Ekip çalışması başarılı bir şekilde devam ediyor."
    ]
    
    # Son 10 gün için veri oluştur
    for i in range(10):
        date = timezone.now().date() - timedelta(days=i)
        
        for user in gonullu_users:
            # Her gün için 1-3 veri oluştur
            for _ in range(random.randint(1, 3)):
                alan = random.choice(alanlar)
                aciklama = random.choice(aciklamalar)
                saat = datetime.now().replace(
                    hour=random.randint(8, 20),
                    minute=random.randint(0, 59)
                ).time()
                
                # Resim oluştur
                img_content = create_demo_image(f"Durum: {alan}")
                
                durum = GonulluDurumVeriler(
                    kisi=user,
                    gun=date,
                    saat=saat,
                    alan=alan,
                    aciklama=aciklama,
                    submitteddate=date,
                    submittedtime=datetime.now().time()
                )
                
                # Resmi kaydet
                durum.fotograf.save(
                    f"durum_{user.id}_{date}_{random.randint(1000, 9999)}.jpg",
                    ContentFile(img_content.getvalue())
                )
                
                print(f"Gönüllü Durum verisi oluşturuldu: {user.get_full_name()} - {date} - {alan}")

def create_gonullu_sorun_data():
    """Gönüllü Sorun verileri oluştur"""
    print("Gönüllü Sorun verileri oluşturuluyor...")
    
    # Gönüllü rolündeki kullanıcıları bul
    gonullu_users = User.objects.filter(role='gonullu')
    
    if not gonullu_users.exists():
        print("Gönüllü rolünde kullanıcı bulunamadı. Yeni kullanıcı oluşturuluyor...")
        # Demo Gönüllü kullanıcısı oluştur (eğer yukarıda oluşturulmadıysa)
        gonullu_user = User.objects.create_user(
            tc="23456789012",
            password="demo1234",
            isim="Demo",
            soyisim="Gönüllü",
            role="gonullu",
            tel_no="5559876543"
        )
        gonullu_users = [gonullu_user]
    
    # Alan seçenekleri
    alanlar = ["Deprem Bölgesi", "Çadır Kent", "Lojistik Merkez", "Yemek Dağıtım", "Sağlık Çadırı"]
    
    # Sorun açıklamaları
    sorunlar = [
        "Yemek dağıtımında gecikme yaşanıyor.",
        "Malzeme eksikliği var.",
        "Ulaşım sorunu yaşanıyor.",
        "İletişim problemi var.",
        "Koordinasyon eksikliği yaşanıyor.",
        "Hava şartları çalışmaları zorlaştırıyor.",
        "Personel yetersizliği var.",
        "Teknik ekipman arızası var."
    ]
    
    # Son 10 gün için veri oluştur
    for i in range(10):
        date = timezone.now().date() - timedelta(days=i)
        
        # Her gün için rastgele 0-2 sorun oluştur (her gün sorun olmayabilir)
        for _ in range(random.randint(0, 2)):
            user = random.choice(list(gonullu_users))
            alan = random.choice(alanlar)
            aciklama = random.choice(sorunlar)
            saat = datetime.now().replace(
                hour=random.randint(8, 20),
                minute=random.randint(0, 59)
            ).time()
            
            # Resim oluştur
            img_content = create_demo_image(f"Sorun: {alan}", bg_color=(180, 70, 70))
            
            sorun = GonulluSorunVeriler(
                kisi=user,
                gun=date,
                saat=saat,
                alan=alan,
                aciklama=aciklama,
                submitteddate=date,
                submittedtime=datetime.now().time()
            )
            
            # Resmi kaydet
            sorun.fotograf.save(
                f"sorun_{user.id}_{date}_{random.randint(1000, 9999)}.jpg",
                ContentFile(img_content.getvalue())
            )
            
            print(f"Gönüllü Sorun verisi oluşturuldu: {user.get_full_name()} - {date} - {alan}")

def create_sorumlu_data():
    """Sorumlu verileri oluştur"""
    print("Sorumlu verileri oluşturuluyor...")
    
    # Sorumlu rolündeki kullanıcıları bul
    sorumlu_users = User.objects.filter(role='sorumlu')
    
    if not sorumlu_users.exists():
        print("Sorumlu rolünde kullanıcı bulunamadı. Yeni kullanıcı oluşturuluyor...")
        # Demo Sorumlu kullanıcısı oluştur
        sorumlu_user = User.objects.create_user(
            tc="34567890123",
            password="demo1234",
            isim="Demo",
            soyisim="Sorumlu",
            role="sorumlu",
            tel_no="5553456789"
        )
        sorumlu_users = [sorumlu_user]
    
    # Son 14 gün için veri oluştur
    for i in range(14):
        date = timezone.now().date() - timedelta(days=i)
        
        for user in sorumlu_users:
            # Aynı gün için veri varsa atla
            if SorumluVeriler.objects.filter(kisi=user, gun=date).exists():
                continue
            
            SorumluVeriler.objects.create(
                kisi=user,
                gun=date,
                personel_yemek_siparis=random.randint(50, 300),
                taseron_yemek_siparis=random.randint(20, 150),
                submitteddate=date,
                submittedtime=datetime.now().time()
            )
            print(f"Sorumlu verisi oluşturuldu: {user.get_full_name()} - {date}")

def create_izleyici_user():
    """İzleyici kullanıcısı oluştur"""
    if not User.objects.filter(role='izleyici').exists():
        izleyici_user = User.objects.create_user(
            tc="45678901234",
            password="demo1234",
            isim="Demo",
            soyisim="İzleyici",
            role="izleyici",
            tel_no="5554567890"
        )
        print(f"İzleyici kullanıcısı oluşturuldu: {izleyici_user.get_full_name()}")

if __name__ == "__main__":
    print("Demo verileri oluşturuluyor...")
    
    # İzleyici kullanıcısı oluştur (dashboard'u görüntülemek için)
    create_izleyici_user()
    
    # T3 Personel verileri oluştur
    create_t3personel_data()
    
    # Gönüllü Durum verileri oluştur
    create_gonullu_durum_data()
    
    # Gönüllü Sorun verileri oluştur
    create_gonullu_sorun_data()
    
    # Sorumlu verileri oluştur
    create_sorumlu_data()
    
    print("Demo veriler başarıyla oluşturuldu!")
    print("\nKullanıcı Bilgileri:")
    print("T3 Personel: TC: 12345678901, Şifre: demo1234")
    print("Gönüllü: TC: 23456789012, Şifre: demo1234")
    print("Sorumlu: TC: 34567890123, Şifre: demo1234")
    print("İzleyici: TC: 45678901234, Şifre: demo1234") 
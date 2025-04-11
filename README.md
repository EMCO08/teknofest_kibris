# Yemek Otomasyonu Sistemi

Bu proje, belirli rollere sahip kullanıcıların izin verilen formlarda veri girişi yapmalarını sağlayan bir web uygulamasıdır. Uygulama, yetkilendirme mekanizmaları ile kullanıcıların erişim alanlarını sınırlandırır, veri girişini kolaylaştırır ve raporlama imkanı sunar.

## Teknoloji Stack

- **Backend:** Django (Python)
- **Database:** SQLite (Geliştirme), PostgreSQL (Üretim)
- **Frontend:** HTML, CSS, JavaScript, Bootstrap
- **Diğer:** Django REST Framework, Redis, Celery

## Kurulum:

### Gereksinimler

- Python 3.8+
- pip
- virtualenv (opsiyonel)

### Adımlar

1. Projeyi klonlayın:
   ```
   git clone https://github.com/kullanici/yemek-otomasyonu.git
   cd yemek-otomasyonu
   ```

2. Sanal ortam oluşturun ve aktifleştirin:
   ```
   python -m venv venv
   .\venv\Scripts\activate
   ```

3. Bağımlılıkları yükleyin:
   ```
   pip install -r requirements.txt
   pip install python-decouple
   ```

4. Veritabanı migrasyonlarını uygulayın:
   ```
   python manage.py migrate
   ```

5. Süper kullanıcı oluşturun:
   ```
   python manage.py createsuperuser
   ```

6. Geliştirme sunucusunu başlatın:
   ```
   python manage.py runserver
   ```

7. Tarayıcınızda `http://127.0.0.1:8000` adresine gidin.

## Kullanıcı Rolleri ve Erişim Yetkileri

| Rol | Erişim Yetkisi |
|-----|----------------|
| Gönüllü (gonullu) | gonullu-form, gonullu-durum-form, gonullu-sorun-form |
| T3 Personel (t3personel) | t3personel-form |
| Sorumlu (sorumlu) | sorumlu-form |
| İzleyici (izleyici) | Dashboard sayfaları |
| Admin (admin) | Tüm yetkilere sahip |

## Sayfa Akışı

- **Landing Page:** Akışkan ve animasyonlu bir ekran, "Yemek Otomasyonu" yazısı ve "Giriş Yap" butonu.
- **Giriş Sayfası:** TC Kimlik Numarası ile giriş.
- **Form Sayfaları:** Kullanıcı rolüne göre farklı formlar.
- **Dashboard Sayfası:** İzleyici ve Admin kullanıcılar için veri görüntüleme ve raporlama.

## Güvenlik ve Yetkilendirme

- TC Kimlik Numarası ile kimlik doğrulama
- Rol tabanlı erişim kontrolü
- Kullanıcı eylemlerinin loglanması
- Veri doğrulama ve güvenlik kontrolleri

## Lisans

Bu proje [MIT Lisansı](LICENSE) altında lisanslanmıştır. 
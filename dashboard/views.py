from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.db.models import Sum, Count
from django.utils import timezone
import csv
from datetime import datetime, timedelta
from forms.models import (
    T3PersonelVeriler, 
    GonulluDurumVeriler, 
    GonulluSorunVeriler, 
    SorumluVeriler,
    SistemAyarlari,
    T3PersonelAtama
)
from forms.views import role_required
from accounts.views import log_user_action
from accounts.models import User
from django.shortcuts import get_object_or_404
import openpyxl
from openpyxl.utils import get_column_letter
from io import BytesIO
from django.db.models import Sum, F
from django.core.paginator import Paginator
from django.template.defaulttags import register

# Template filtreleri
@register.filter
def get_item(dictionary, key):
    """Dictionary'den değer almak için template filtresi"""
    return dictionary.get(key, 0)

@login_required
@role_required(['izleyici', 'admin'])
def dashboard_home(request):
    """Dashboard ana sayfası"""
    log_user_action(request, 'Dashboard Ana Sayfası Görüntülendi', 'Dashboard Home')

    # Son 7 günlük verileri getir
    son_7_gun = timezone.now().date() - timedelta(days=7)

    t3_veriler_sayisi = T3PersonelVeriler.objects.filter(submitteddate__gte=son_7_gun).count()


    gonullu_durum_sayisi = GonulluDurumVeriler.objects.filter(submitteddate__gte=son_7_gun).count()
    gonullu_sorun_sayisi = GonulluSorunVeriler.objects.filter(submitteddate__gte=son_7_gun).count()
    sorumlu_veriler_sayisi = SorumluVeriler.objects.filter(submitteddate__gte=son_7_gun).count()


    # Toplam sipariş sayıları
    toplam_personel_siparis = SorumluVeriler.objects.filter(submitteddate__gte=son_7_gun).aggregate(Sum('personel_yemek_siparis'))['personel_yemek_siparis__sum'] or 0
    toplam_taseron_siparis = SorumluVeriler.objects.filter(submitteddate__gte=son_7_gun).aggregate(Sum('taseron_yemek_siparis'))['taseron_yemek_siparis__sum'] or 0
    

    toplam_t3_siparis = (
        T3PersonelVeriler.objects
        .filter(submitteddate__gte=son_7_gun)
        .aggregate(toplam=Sum(F('ogle_yemegi') + F('aksam_yemegi') + F('lunchbox')))['toplam'] or 0
    )

    # Koordinatörlük tablosu için veri hazırlama
    # Seçilen gün (varsayılan olarak 1. gün)
    secilen_gun = request.GET.get('gun', '1. Gün')
    
    # Tüm koordinatörlük listesi
    koordinatorlukler = [
        'Selçuk Bey VIP', 'VIP Salon', 'Yönetim Ofisi / Kriz Masası', 'Vakıf Standı Yönetici Odası',
        'Dinamik Alan', 'TSK', 'Gönüllü - Bursiyer', 'Basın', 'TRT Kulis Ana Sahne / Muhabir',
        'Arter / To Do / Kurumsal Ofis / Heysemist', 'Pilot Event', 'T3 Ofis', 
        'Teknofest Robolig Yarışması', 'Teknofest KKTC Araştırma Yarışması', 'Bilim Pavyonu'
    ]
    
    # Tüm günler
    gunler = ['1. Gün', '2. Gün', '3. Gün', '4. Gün']
    
    # Koordinatörlük verilerini hesapla
    koordinatorluk_veri_sayilari = {}
    
    # Her koordinatörlük için seçilen günde kaç veri girildiğini hesapla
    for koordinatorluk in koordinatorlukler:
        # Durum verilerini say
        durum_sayisi = GonulluDurumVeriler.objects.filter(
            alan=koordinatorluk, 
            gun=secilen_gun
        ).count()
        
        # Sorun verilerini say
        sorun_sayisi = GonulluSorunVeriler.objects.filter(
            alan=koordinatorluk, 
            gun=secilen_gun
        ).count()
        
        # Toplam veri sayısı
        toplam_veri = durum_sayisi + sorun_sayisi
        
        koordinatorluk_veri_sayilari[koordinatorluk] = toplam_veri

    # Sistem ayarlarını al
    try:
        veri_guncelleme_son_saat = int(SistemAyarlari.objects.get(anahtar='veri_guncelleme_son_saat').deger)
    except (SistemAyarlari.DoesNotExist, ValueError):
        veri_guncelleme_son_saat = 14  # Varsayılan değer

    try:
        veri_guncelleme_son_dakika = int(SistemAyarlari.objects.get(anahtar='veri_guncelleme_son_dakika').deger)
    except (SistemAyarlari.DoesNotExist, ValueError):
        veri_guncelleme_son_dakika = 0  # Varsayılan değer

    context = {
        't3_veriler_sayisi': t3_veriler_sayisi,
        'gonullu_durum_sayisi': gonullu_durum_sayisi,
        'gonullu_sorun_sayisi': gonullu_sorun_sayisi,
        'sorumlu_veriler_sayisi': sorumlu_veriler_sayisi,
        'toplam_personel_siparis': toplam_personel_siparis,
        'toplam_taseron_siparis': toplam_taseron_siparis,
        'toplam_t3_siparis': toplam_t3_siparis,
        'veri_guncelleme_son_saat': veri_guncelleme_son_saat,
        'veri_guncelleme_son_dakika': veri_guncelleme_son_dakika,
        'secilen_gun': secilen_gun,
        'gunler': gunler,
        'koordinatorlukler': koordinatorlukler,
        'koordinatorluk_veri_sayilari': koordinatorluk_veri_sayilari,
    }

    return render(request, 'dashboard/home.html', context)

@login_required
@role_required(['izleyici', 'admin'])
def t3personel_dashboard(request):
    """T3 personel verileri dashboard"""
    log_user_action(request, 'T3 Personel Dashboard Görüntülendi', 'T3 Personel Dashboard')

    # Filtreleme parametreleri
    baslangic_tarihi = request.GET.get('baslangic_tarihi')
    bitis_tarihi = request.GET.get('bitis_tarihi')
    koordinatorluk = request.GET.get('koordinatorluk')
    birim = request.GET.get('birim')

    # Temel sorgu
    veriler = T3PersonelVeriler.objects.all().order_by('-submitteddate', '-submittedtime')

    # Filtreleri uygula
    if baslangic_tarihi:
        veriler = veriler.filter(submitteddate__gte=baslangic_tarihi)
    if bitis_tarihi:
        veriler = veriler.filter(submitteddate__lte=bitis_tarihi)
    if koordinatorluk:
        veriler = veriler.filter(koordinatorluk__icontains=koordinatorluk)
    if birim:
        veriler = veriler.filter(birim__icontains=birim)

    # CSV indirme
    # Excel indirme

    if 'csv' in request.GET:



        wb = openpyxl.Workbook()

        ws = wb.active

        ws.title = "T3 Personel Verileri"



        # Başlıklar

        headers = ['TC', 'İsim', 'Soyisim', 'Koordinatörlük', 'Birim',

                'Öğle Yemeği', 'Akşam Yemeği', 'Lunchbox', 'Toplam', 'Tarih', 'Saat']

        ws.append(headers)



        # Veriler

        for veri in veriler:

            toplam = veri.ogle_yemegi + veri.aksam_yemegi + veri.lunchbox

            ws.append([

                veri.kisi.tc,

                veri.kisi.isim,

                veri.kisi.soyisim,

                veri.koordinatorluk,

                veri.birim,

                veri.ogle_yemegi,

                veri.aksam_yemegi,

                veri.lunchbox,

                toplam,

                veri.submitteddate.strftime('%Y-%m-%d'),

                str(veri.submittedtime)

            ])



        # Excel dosyasını bellekte oluştur

        output = BytesIO()

        wb.save(output)

        output.seek(0)



        # HTTP yanıtı olarak döndür

        response = HttpResponse(

            output,

            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'

        )

        response['Content-Disposition'] = 'attachment; filename="t3personel_veriler.xlsx"'

        return response

    # Koordinatörlük ve birim listelerini al
    koordinatorlukler = T3PersonelVeriler.objects.values_list('koordinatorluk', flat=True).distinct()
    birimler = T3PersonelVeriler.objects.values_list('birim', flat=True).distinct()

    context = {
        'veriler': veriler,
        'koordinatorlukler': koordinatorlukler,
        'birimler': birimler,
        'filtreler': {
            'baslangic_tarihi': baslangic_tarihi,
            'bitis_tarihi': bitis_tarihi,
            'koordinatorluk': koordinatorluk,
            'birim': birim,
        }
    }

    return render(request, 'dashboard/t3personel.html', context)

@login_required
@role_required(['izleyici', 'admin'])
def gonullu_durum_dashboard(request):
    """Gönüllü durum verileri dashboard"""
    log_user_action(request, 'Gönüllü Durum Dashboard Görüntülendi', 'Gönüllü Durum Dashboard')

    # Filtreleme parametreleri
    baslangic_tarihi = request.GET.get('baslangic_tarihi')
    bitis_tarihi = request.GET.get('bitis_tarihi')
    alan = request.GET.get('alan')

    # Temel sorgu
    veriler = GonulluDurumVeriler.objects.all().order_by('-submitteddate', '-submittedtime')

    # Filtreleri uygula
    if baslangic_tarihi:
        veriler = veriler.filter(submitteddate__gte=baslangic_tarihi)
    if bitis_tarihi:
        veriler = veriler.filter(submitteddate__lte=bitis_tarihi)
    if alan:
        veriler = veriler.filter(alan__icontains=alan)

    # CSV indirme
    if 'csv' in request.GET:
        response = HttpResponse(content_type='text/csv; charset=utf-8-sig')
        response['Content-Disposition'] = 'attachment; filename="gonullu_durum_veriler.csv"'

        writer = csv.writer(response, delimiter=';')
        writer.writerow(['İsim', 'Gün', 'Saat', 'Alan', 'Catering Durumu', 'Catering Ürünleri', 'Fotoğraf', 'Tarih', 'Saat'])
        for veri in veriler:
            writer.writerow([
                veri.kisi.get_full_name(),
                veri.gun,
                veri.saat,
                veri.alan,
                veri.catering_durum,
                ', '.join(veri.catering_urunleri) if veri.catering_urunleri else '',
                'Var' if veri.fotograf else 'Yok',
                veri.submitteddate,
                veri.submittedtime,
            ])

        return response

    # Pagination
    paginator = Paginator(veriler, 50)  # Her sayfada 50 kayıt
    page = request.GET.get('page')
    veriler_paginated = paginator.get_page(page)
    
    # Her veri için fotografları prefetch et
    for veri in veriler_paginated:
        veri.fotograflar_list = veri.fotograflar.all()

    # Alan listesini al
    alanlar = GonulluDurumVeriler.objects.values_list('alan', flat=True).distinct()

    context = {
        'veriler': veriler_paginated,
        'alanlar': alanlar,
        'filtreler': {
            'baslangic_tarihi': baslangic_tarihi,
            'bitis_tarihi': bitis_tarihi,
            'alan': alan,
        }
    }

    return render(request, 'dashboard/gonullu_durum.html', context)

@login_required
@role_required(['izleyici', 'admin'])
def gonullu_sorun_dashboard(request):
    """Gönüllü sorun verileri dashboard"""
    log_user_action(request, 'Gönüllü Sorun Dashboard Görüntülendi', 'Gönüllü Sorun Dashboard')

    # Filtreleme parametreleri
    baslangic_tarihi = request.GET.get('baslangic_tarihi')
    bitis_tarihi = request.GET.get('bitis_tarihi')
    alan = request.GET.get('alan')
    sorun_tipi = request.GET.get('sorun_tipi')
    sorun_seviyesi = request.GET.get('sorun_seviyesi')

    # Temel sorgu
    veriler = GonulluSorunVeriler.objects.all().order_by('-submitteddate', '-submittedtime')

    # Filtreleri uygula
    if baslangic_tarihi:
        veriler = veriler.filter(submitteddate__gte=baslangic_tarihi)
    if bitis_tarihi:
        veriler = veriler.filter(submitteddate__lte=bitis_tarihi)
    if alan:
        veriler = veriler.filter(alan__icontains=alan)
    if sorun_tipi:
        veriler = veriler.filter(sorun_tipi=sorun_tipi)
    if sorun_seviyesi:
        veriler = veriler.filter(sorun_seviyesi=sorun_seviyesi)

    # CSV indirme
    if 'csv' in request.GET:
        response = HttpResponse(content_type='text/csv; charset=utf-8-sig')
        response['Content-Disposition'] = 'attachment; filename="gonullu_sorun_veriler.csv"'

        writer = csv.writer(response, delimiter=';')
        writer.writerow(['TC', 'İsim', 'Soyisim', 'Gün', 'Saat', 'Alan', 'Sorun Tipi', 'Sorun Seviyesi', 'Açıklama', 'Tarih', 'Saat'])

        for veri in veriler:
            writer.writerow([
                veri.kisi.tc,
                veri.kisi.isim,
                veri.kisi.soyisim,
                veri.gun,
                veri.saat,
                veri.alan,
                veri.sorun_tipi,
                veri.sorun_seviyesi,
                veri.aciklama,
                veri.submitteddate.strftime('%Y-%m-%d'),
                veri.submittedtime.strftime('%H:%M:%S')
            ])

        return response
        
    # Pagination
    paginator = Paginator(veriler, 50)  # Her sayfada 50 kayıt
    page = request.GET.get('page')
    veriler_paginated = paginator.get_page(page)
    
    # Her veri için fotografları prefetch et
    for veri in veriler_paginated:
        veri.fotograflar_list = veri.fotograflar.all()

    # Alan listesini al
    alanlar = GonulluSorunVeriler.objects.values_list('alan', flat=True).distinct()
    
    # Sorun tipleri ve seviyeleri için choices'ları al
    sorun_tipleri = [choice[0] for choice in GonulluSorunVeriler.SORUN_TIPI_CHOICES]
    sorun_seviyeleri = [choice[0] for choice in GonulluSorunVeriler.SORUN_SEVIYESI_CHOICES]

    context = {
        'veriler': veriler_paginated,
        'alanlar': alanlar,
        'sorun_tipleri': sorun_tipleri,
        'sorun_seviyeleri': sorun_seviyeleri,
        'filtreler': {
            'baslangic_tarihi': baslangic_tarihi,
            'bitis_tarihi': bitis_tarihi,
            'alan': alan,
            'sorun_tipi': sorun_tipi,
            'sorun_seviyesi': sorun_seviyesi
        }
    }

    return render(request, 'dashboard/gonullu_sorun.html', context)

@login_required
@role_required(['izleyici', 'admin', 'sorumlu'])
def sorumlu_dashboard(request):
    """Sorumlu verileri dashboard"""
    log_user_action(request, 'Sorumlu Dashboard Görüntülendi', 'Sorumlu Dashboard')

    # Filtreleme parametreleri
    baslangic_tarihi = request.GET.get('baslangic_tarihi')
    bitis_tarihi = request.GET.get('bitis_tarihi')

    # Temel sorgu
    veriler = SorumluVeriler.objects.all().order_by('-submitteddate', '-submittedtime')

    # Filtreleri uygula
    if baslangic_tarihi:
        veriler = veriler.filter(submitteddate__gte=baslangic_tarihi)
    if bitis_tarihi:
        veriler = veriler.filter(submitteddate__lte=bitis_tarihi)

    # CSV indirme
    if 'csv' in request.GET:
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="sorumlu_veriler.csv"'

        writer = csv.writer(response)
        writer.writerow(['TC', 'İsim', 'Soyisim', 'Gün', 'Personel Yemek Siparişi', 'Taşeron Yemek Siparişi', 'Tarih', 'Saat'])

        for veri in veriler:
            writer.writerow([
                veri.kisi.tc,
                veri.kisi.isim,
                veri.kisi.soyisim,
                veri.gun,
                veri.personel_yemek_siparis,
                veri.taseron_yemek_siparis,
                veri.submitteddate,
                veri.submittedtime
            ])

        return response

    # Toplam sipariş sayıları
    toplam_personel_siparis = veriler.aggregate(Sum('personel_yemek_siparis'))['personel_yemek_siparis__sum'] or 0
    toplam_taseron_siparis = veriler.aggregate(Sum('taseron_yemek_siparis'))['taseron_yemek_siparis__sum'] or 0

    context = {
        'veriler': veriler,
        'toplam_personel_siparis': toplam_personel_siparis,
        'toplam_taseron_siparis': toplam_taseron_siparis,
    }

    return render(request, 'dashboard/sorumlu.html', context)

@login_required
def sistem_ayarlari_guncelle(request):
    """Sistem ayarlarını güncelleme view'ı"""
    if not (request.user.is_superuser or request.user.is_staff):
        messages.error(request, 'Bu işlemi yapmaya yetkiniz yok.')
        return redirect('dashboard:home')

    if request.method == 'POST':
        veri_guncelleme_son_saat = request.POST.get('veri_guncelleme_son_saat', '14')
        veri_guncelleme_son_dakika = request.POST.get('veri_guncelleme_son_dakika', '0')

        # Değerleri kontrol et
        try:
            saat = int(veri_guncelleme_son_saat)
            dakika = int(veri_guncelleme_son_dakika)

            if not (0 <= saat <= 23 and 0 <= dakika <= 59):
                raise ValueError("Geçersiz saat veya dakika değeri")

            # Saat ayarını kaydet
            SistemAyarlari.objects.update_or_create(
                anahtar='veri_guncelleme_son_saat',
                defaults={'deger': str(saat), 'aciklama': 'T3 personel verilerinin güncellenebileceği son saat'}
            )

            # Dakika ayarını kaydet
            SistemAyarlari.objects.update_or_create(
                anahtar='veri_guncelleme_son_dakika',
                defaults={'deger': str(dakika), 'aciklama': 'T3 personel verilerinin güncellenebileceği son dakika'}
            )

            messages.success(request, 'Sistem ayarları başarıyla güncellendi.')
        except ValueError:
            messages.error(request, 'Geçersiz saat veya dakika değeri girdiniz.')

    return redirect('dashboard:home')

@login_required
@role_required(['admin'])
def t3personel_atama_ekle(request):
    """T3 personel ataması ekleme sayfası"""
    log_user_action(request, 'T3 Personel Atama Ekleme Sayfası Görüntülendi', 'T3 Personel Atama')

    # T3 personel rolüne sahip kullanıcıları getir
    users = User.objects.filter(role='t3personel')

    # Sabit koordinatörlük listesi
    koordinatorlukler = [
        "Bilişim Koordinatörlüğü",
        "Bursiyer Koordinatörlüğü",
        "Deneyap Koordinatörlüğü",
        "Eğitim Ar-Ge",
        "Fuar Koordinatörlüğü",
        "Girişim Koordinatörlüğü",
        "İdari İşler Koordinatörlüğü",
        "Kurumsal İletişim Koordinatörlüğü",
        "Kurumsal Yapılanma Koordinatörlüğü",
        "Mimari Tasarım Koordinatörlüğü",
        "Satış ve Pazarlama Koordinatörlüğü",
        "Operasyon Koordinatörlüğü",
        "Ulaşım Koordinatörlüğü",
        "Yarışmalar Koordinatörlüğü"
    ]

    # Veritabanındaki diğer koordinatörlükleri de ekle
    db_koordinatorlukler = T3PersonelAtama.objects.values_list('koordinatorluk', flat=True).distinct()
    for k in db_koordinatorlukler:
        if k not in koordinatorlukler:
            koordinatorlukler.append(k)

    # Mevcut atamaları getir
    atamalar = T3PersonelAtama.objects.all().order_by('kisi__isim', 'kisi__soyisim', 'koordinatorluk', 'birim')

    if request.method == 'POST':
        # Form verilerini al
        kisi_ids = request.POST.getlist('kisi')
        koordinatorlukler = request.POST.getlist('koordinatorluk')
        birimler = request.POST.getlist('birim')
        coffee_breaks = request.POST.getlist('coffee_break')
        
        # Her bir satır için işlem yap
        basarili_kayit = 0
        hata_kayit = 0

        for i in range(len(kisi_ids)):
            if i < len(koordinatorlukler) and i < len(birimler):
                try:
                    kisi = get_object_or_404(User, id=kisi_ids[i])
                    koordinatorluk = koordinatorlukler[i]
                    birim = birimler[i]
                    coffee_break = True if f'{i}' in coffee_breaks else False

                    # Boş değer kontrolü
                    if not koordinatorluk or not birim:
                        hata_kayit += 1
                        continue

                    # Aynı kayıt var mı kontrolü
                    if T3PersonelAtama.objects.filter(kisi=kisi, koordinatorluk=koordinatorluk, birim=birim).exists():
                        hata_kayit += 1
                        continue

                    # Yeni atama oluştur
                    T3PersonelAtama.objects.create(
                        kisi=kisi,
                        koordinatorluk=koordinatorluk,
                        birim=birim,
                        coffee_break=coffee_break
                    )
                    basarili_kayit += 1
                except Exception as e:
                    hata_kayit += 1
                    print(f"Hata: {str(e)}")

        if basarili_kayit > 0:
            messages.success(request, f'{basarili_kayit} adet T3 personel ataması başarıyla eklendi.')

        if hata_kayit > 0:
            messages.warning(request, f'{hata_kayit} adet atama eklenirken hata oluştu.')

        return redirect('dashboard:t3personel_atama_ekle')

    context = {
        'users': users,
        'koordinatorlukler': koordinatorlukler,
        'atamalar': atamalar,
    }

    return render(request, 'dashboard/t3personel_atama_ekle.html', context)

@login_required
@role_required(['admin'])
def get_koordinatorluk_for_user(request, user_id):
    """Kullanıcının mevcut koordinatörlüğünü getir"""
    try:
        # Kullanıcının en son atamasını bul
        atama = T3PersonelAtama.objects.filter(kisi_id=user_id).order_by('-id').first()

        if atama:
            return JsonResponse({
                'success': True,
                'koordinatorluk': atama.koordinatorluk
            })
        else:
            return JsonResponse({
                'success': True,
                'koordinatorluk': None
            })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })
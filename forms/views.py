from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import time
from .models import (
    T3PersonelAtama, 
    T3PersonelVeriler, 
    GonulluDurumVeriler, 
    GonulluSorunVeriler, 
    SorumluVeriler,
    SistemAyarlari
)
from accounts.views import log_user_action
from django.http import JsonResponse

def role_required(roles):
    """Belirli rollere sahip kullanıcıların erişimini kontrol eden dekoratör"""
    def decorator(view_func):
        @login_required
        def wrapper(request, *args, **kwargs):
            if request.user.role in roles:
                return view_func(request, *args, **kwargs)
            else:
                messages.error(request, 'Bu sayfaya erişim yetkiniz bulunmamaktadır.')
                return redirect('accounts:home')
        return wrapper
    return decorator

@login_required
@role_required(['gonullu'])
def gonullu_form(request):
    """Gönüllü ana form sayfası"""
    log_user_action(request, 'Gönüllü Form Sayfası Görüntülendi', 'Gönüllü Form')
    return render(request, 'forms/gonullu_form.html')

@login_required
@role_required(['gonullu'])
def gonullu_durum_form(request):
    """Gönüllü durum bildirim formu"""
    log_user_action(request, 'Gönüllü Durum Form Sayfası Görüntülendi', 'Gönüllü Durum Form')
    
    if request.method == 'POST':
        gun = request.POST.get('gun')
        saat = request.POST.get('saat')
        alan = request.POST.get('alan')
        aciklama = request.POST.get('aciklama')
        fotograf = request.FILES.get('fotograf')
        
        try:
            GonulluDurumVeriler.objects.create(
                kisi=request.user,
                gun=gun,
                saat=saat,
                alan=alan,
                aciklama=aciklama,
                fotograf=fotograf
            )
            log_user_action(request, 'Gönüllü Durum Formu Gönderildi', 'Gönüllü Durum Form')
            messages.success(request, 'Durum bildiriminiz başarıyla kaydedildi.')
            return redirect('forms:gonullu_form')
        except Exception as e:
            messages.error(request, f'Bir hata oluştu: {str(e)}')
    
    return render(request, 'forms/gonullu_durum_form.html')

@login_required
@role_required(['gonullu'])
def gonullu_sorun_form(request):
    """Gönüllü sorun bildirim formu"""
    log_user_action(request, 'Gönüllü Sorun Form Sayfası Görüntülendi', 'Gönüllü Sorun Form')
    
    if request.method == 'POST':
        gun = request.POST.get('gun')
        saat = request.POST.get('saat')
        alan = request.POST.get('alan')
        aciklama = request.POST.get('aciklama')
        fotograf = request.FILES.get('fotograf')
        
        try:
            GonulluSorunVeriler.objects.create(
                kisi=request.user,
                gun=gun,
                saat=saat,
                alan=alan,
                aciklama=aciklama,
                fotograf=fotograf
            )
            log_user_action(request, 'Gönüllü Sorun Formu Gönderildi', 'Gönüllü Sorun Form')
            messages.success(request, 'Sorun bildiriminiz başarıyla kaydedildi.')
            return redirect('forms:gonullu_form')
        except Exception as e:
            messages.error(request, f'Bir hata oluştu: {str(e)}')
    
    return render(request, 'forms/gonullu_sorun_form.html')

@login_required
@role_required(['t3personel'])
def t3personel_form(request):
    """T3 personel sipariş formu"""
    log_user_action(request, 'T3 Personel Form Sayfası Görüntülendi', 'T3 Personel Form')
    
    user = request.user
    atamalar = T3PersonelAtama.objects.filter(kisi=user)
    bugun = timezone.now().date()
    
    # Türkiye saatini al (+3)
    simdi = timezone.localtime(timezone.now()).time()
    
    # Sistem ayarlarından son saat ve dakikayı al
    try:
        son_saat = int(SistemAyarlari.objects.get(anahtar='veri_guncelleme_son_saat').deger)
        son_dakika = int(SistemAyarlari.objects.get(anahtar='veri_guncelleme_son_dakika').deger)
    except (SistemAyarlari.DoesNotExist, ValueError):
        son_saat = 12
        son_dakika = 0
    
    # Belirlenen saatten önce mi kontrol et
    saat_uygun = simdi < time(son_saat, son_dakika)

    # Güncelleme modu kontrolü
    guncelleme_modu = request.session.get('t3personel_guncelleme_modu', False)
    
    # Daha önce aynı gün veri gönderilmişse onları çek
    bugunku_kayitlar = T3PersonelVeriler.objects.filter(kisi=user, submitteddate=bugun)
    
    # Form gösterim modu (True: form göster, False: tablo göster)
    form_goster = guncelleme_modu or not bugunku_kayitlar.exists()

    if not atamalar.exists():
        messages.warning(request, 'Henüz size atanmış koordinatörlük ve birim bulunmamaktadır.')

    if request.method == 'POST' and not request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        if not saat_uygun:
            messages.error(request, f'Veri girişi için son saat {son_saat:02d}:{son_dakika:02d}\'dır. Şu an veri girişi yapamazsınız.')
            return redirect('forms:t3personel_form')

        # Eğer güncelleme modu aktifse önce eski kayıtları sil
        if guncelleme_modu:
            T3PersonelVeriler.objects.filter(kisi=user, submitteddate=bugun).delete()
            request.session['t3personel_guncelleme_modu'] = False
            
        for atama in atamalar:
            ogle_key = f'ogle_{atama.id}'
            aksam_key = f'aksam_{atama.id}'
            lunchbox_key = f'lunchbox_{atama.id}'
            coffee_key = f'coffee_{atama.id}'
            ogle_sayisi = request.POST.get(ogle_key)
            aksam_sayisi = request.POST.get(aksam_key)
            lunchbox_sayisi = request.POST.get(lunchbox_key)
            coffee_sayisi = request.POST.get(coffee_key)

            if ogle_sayisi and aksam_sayisi and lunchbox_sayisi and coffee_sayisi and ogle_sayisi.isdigit() and aksam_sayisi.isdigit() and lunchbox_sayisi.isdigit() and coffee_sayisi.isdigit():
                T3PersonelVeriler.objects.create(
                    kisi=user,
                    koordinatorluk=atama.koordinatorluk,
                    birim=atama.birim,
                    ogle_yemegi=int(ogle_sayisi),
                    aksam_yemegi=int(aksam_sayisi),
                    lunchbox=int(lunchbox_sayisi),
                    coffee_break=int(coffee_sayisi)
                )

        log_user_action(request, 'T3 Personel Formu Gönderildi', 'T3 Personel Form')
        if guncelleme_modu:
            messages.success(request, 'Sipariş bilgileriniz başarıyla güncellendi.')
        else:
            messages.success(request, 'Sipariş bilgileriniz başarıyla kaydedildi.')
        return redirect('forms:t3personel_form')

    # Form alanları için eski değerleri hazırla
    eski_veriler = {}
    if bugunku_kayitlar.exists() and guncelleme_modu:
        for veri in bugunku_kayitlar:
            atama = T3PersonelAtama.objects.filter(kisi=user, koordinatorluk=veri.koordinatorluk, birim=veri.birim).first()
            if atama:
                eski_veriler[atama.id] = {
                    'ogle': veri.ogle_yemegi,
                    'aksam': veri.aksam_yemegi,
                    'lunchbox': veri.lunchbox,
                    'coffee': veri.coffee_break
                }

    context = {
        'atamalar': atamalar,
        'bugunku_kayitlar': bugunku_kayitlar,
        'saat_uygun': saat_uygun,
        'guncelleme_modu': guncelleme_modu,
        'son_saat': son_saat,
        'son_dakika': son_dakika,
        'form_goster': form_goster,
        'eski_veriler': eski_veriler
    }
    return render(request, 'forms/t3personel_form.html', context)

@login_required
@role_required(['t3personel'])
def t3personel_form_guncelle(request):
    """T3 personel verilerini güncelleme modu"""
    # Türkiye saatini al (+3)
    simdi = timezone.localtime(timezone.now()).time()
    
    # Sistem ayarlarından son saat ve dakikayı al
    try:
        son_saat = int(SistemAyarlari.objects.get(anahtar='veri_guncelleme_son_saat').deger)
        son_dakika = int(SistemAyarlari.objects.get(anahtar='veri_guncelleme_son_dakika').deger)
    except (SistemAyarlari.DoesNotExist, ValueError):
        son_saat = 12
        son_dakika = 0
    
    # Belirlenen saatten önce mi kontrol et
    if simdi >= time(son_saat, son_dakika):
        messages.error(request, f'Veri güncelleme için son saat {son_saat:02d}:{son_dakika:02d}\'dır. Şu an güncelleme yapamazsınız.')
        return redirect('forms:t3personel_form')
    
    # Güncelleme modunu aç
    request.session['t3personel_guncelleme_modu'] = True
    messages.info(request, 'Veri güncelleme modundasınız. Lütfen yeni değerleri girin.')
    return redirect('forms:t3personel_form')

@login_required
@role_required(['sorumlu'])
def sorumlu_form(request):
    """Sorumlu sipariş formu"""
    log_user_action(request, 'Sorumlu Form Sayfası Görüntülendi', 'Sorumlu Form')
    
    if request.method == 'POST':
        gun = request.POST.get('gun')
        personel_yemek_siparis = request.POST.get('personel_yemek_siparis')
        taseron_yemek_siparis = request.POST.get('taseron_yemek_siparis')
        
        try:
            SorumluVeriler.objects.create(
                kisi=request.user,
                gun=gun,
                personel_yemek_siparis=personel_yemek_siparis,
                taseron_yemek_siparis=taseron_yemek_siparis
            )
            log_user_action(request, 'Sorumlu Formu Gönderildi', 'Sorumlu Form')
            messages.success(request, 'Sipariş bilgileriniz başarıyla kaydedildi.')
            return redirect('forms:sorumlu_form')
        except Exception as e:
            messages.error(request, f'Bir hata oluştu: {str(e)}')
    
    return render(request, 'forms/sorumlu_form.html')



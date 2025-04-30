from django.db import models
from django.conf import settings
import os
from django.utils import timezone

# CloudCube storage'ı import et
from .storage import CloudCubeStorage, GonulluDurumStorage, GonulluSorunStorage

class T3PersonelAtama(models.Model):
    kisi = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='atamalar')
    koordinatorluk = models.CharField(max_length=100)
    birim = models.CharField(max_length=100)
    coffee_break = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.kisi.get_full_name()} - {self.koordinatorluk} - {self.birim}"

    class Meta:
        verbose_name = 'T3 Personel Ataması'
        verbose_name_plural = 'T3 Personel Atamaları'
        db_table = 't3personel_atama'
        unique_together = ('kisi', 'koordinatorluk', 'birim')

class T3PersonelVeriler(models.Model):
    kisi = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='t3_veriler')
    koordinatorluk = models.CharField(max_length=100)
    birim = models.CharField(max_length=100)

    ogle_yemegi = models.PositiveIntegerField()
    aksam_yemegi = models.PositiveIntegerField()
    lunchbox = models.PositiveIntegerField(default=0)
    coffee_break = models.PositiveIntegerField(default=0, null=True, blank=True)

    submitteddate = models.DateField(auto_now_add=True)
    submittedtime = models.TimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.kisi.get_full_name()} - {self.koordinatorluk} - {self.birim} - Öğle: {self.ogle_yemegi} - Akşam: {self.aksam_yemegi} - Coffee: {self.coffee_break}"

    class Meta:
        verbose_name = 'T3 Personel Verisi'
        verbose_name_plural = 'T3 Personel Verileri'
        db_table = 't3personel_veriler'


class GonulluDurumVeriler(models.Model):
    kisi = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='gonullu_durum_veriler')
    gun = models.CharField(max_length=50)
    saat = models.TimeField()
    alan = models.CharField(max_length=100)
    catering_durum = models.CharField(max_length=10, choices=[('var', 'Catering Var'), ('yok', 'Catering Yok')], default='yok')
    catering_urunleri = models.JSONField(blank=True, null=True)
    
    # Çoklu fotoğraf desteği için bu alan artık kullanılmayacak, ama geri uyumluluk için tutulacak
    fotograf = models.ImageField(
        upload_to='', 
        blank=True, 
        null=True, 
        storage=GonulluDurumStorage() if hasattr(settings, 'CLOUDCUBE_URL') and settings.CLOUDCUBE_URL else None
    )
    
    submitteddate = models.DateField(auto_now_add=True)
    submittedtime = models.TimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.kisi.get_full_name()} - {self.gun} - {self.saat} - {self.alan}"
    
    def get_fotograf_url(self):
        """CloudCube'dan fotoğrafın URL'sini döndür"""
        if not self.fotograf:
            return None
            
        if hasattr(settings, 'CLOUDCUBE_URL') and settings.CLOUDCUBE_URL and self.fotograf:
            # CloudCube'a erişim URL'sini oluştur
            if 's3.amazonaws.com' in settings.CLOUDCUBE_URL:
                # Eğer URL içinde dosya adı varsa
                if hasattr(self.fotograf, 'name'):
                    file_name = self.fotograf.name
                    if file_name.startswith('/'):
                        file_name = file_name[1:]
                    return f"{settings.CLOUDCUBE_URL.rstrip('/')}/public/gonullu_durum_fotolar/{file_name}"
                # Eğer fotograf.url varsa direkt olarak kullan
                elif hasattr(self.fotograf, 'url'):
                    return self.fotograf.url
        # Django'nun kendi URL mekanizmasını kullan
        try:
            return self.fotograf.url
        except:
            return None

    class Meta:
        verbose_name = 'Gönüllü Durum Verisi'
        verbose_name_plural = 'Gönüllü Durum Verileri'
        db_table = 'gonullu_durum_veriler'

class GonulluDurumFotograf(models.Model):
    """Gönüllü durum bildirimlerine ait fotoğraf modeli"""
    durum = models.ForeignKey(GonulluDurumVeriler, on_delete=models.CASCADE, related_name='fotograflar')
    fotograf = models.ImageField(
        upload_to='', 
        storage=GonulluDurumStorage() if hasattr(settings, 'CLOUDCUBE_URL') and settings.CLOUDCUBE_URL else None
    )
    added_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Fotoğraf - {self.durum}"
    
    def get_fotograf_url(self):
        """CloudCube'dan fotoğrafın URL'sini döndür"""
        if not self.fotograf:
            return None
            
        if hasattr(settings, 'CLOUDCUBE_URL') and settings.CLOUDCUBE_URL and self.fotograf:
            # CloudCube'a erişim URL'sini oluştur
            if 's3.amazonaws.com' in settings.CLOUDCUBE_URL:
                # Eğer URL içinde dosya adı varsa
                if hasattr(self.fotograf, 'name'):
                    file_name = self.fotograf.name
                    if file_name.startswith('/'):
                        file_name = file_name[1:]
                    return f"{settings.CLOUDCUBE_URL.rstrip('/')}/public/gonullu_durum_fotolar/{file_name}"
                # Eğer fotograf.url varsa direkt olarak kullan
                elif hasattr(self.fotograf, 'url'):
                    return self.fotograf.url
        # Django'nun kendi URL mekanizmasını kullan
        try:
            return self.fotograf.url
        except:
            return None
    
    class Meta:
        verbose_name = 'Gönüllü Durum Fotoğrafı'
        verbose_name_plural = 'Gönüllü Durum Fotoğrafları'
        db_table = 'gonullu_durum_fotograflar'

class GonulluSorunVeriler(models.Model):
    SORUN_TIPI_CHOICES = [
        ('Hijyen', 'Hijyen'),
        ('Ürün Kalitesi', 'Ürün Kalitesi'),
        ('İnsan Sağlığı', 'İnsan Sağlığı'),
        ('Hizmet Kalitesi', 'Hizmet Kalitesi'),
    ]
    
    SORUN_SEVIYESI_CHOICES = [
        ('Düşük', 'Düşük'),
        ('Orta', 'Orta'),
        ('Acil', 'Acil'),
    ]

    kisi = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='gonullu_sorun_veriler')
    gun = models.CharField(max_length=50)
    saat = models.TimeField()
    alan = models.CharField(max_length=100)
    sorun_tipi = models.CharField(max_length=50, choices=SORUN_TIPI_CHOICES, default='Hizmet Kalitesi')
    sorun_seviyesi = models.CharField(max_length=20, choices=SORUN_SEVIYESI_CHOICES, default='Düşük')
    aciklama = models.TextField()
    
    # Çoklu fotoğraf desteği için bu alan artık kullanılmayacak, ama geri uyumluluk için tutulacak
    fotograf = models.ImageField(
        upload_to='', 
        blank=True, 
        null=True, 
        storage=GonulluSorunStorage() if hasattr(settings, 'CLOUDCUBE_URL') and settings.CLOUDCUBE_URL else None
    )
    submitteddate = models.DateField(auto_now_add=True)
    submittedtime = models.TimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.kisi.get_full_name()} - {self.gun} - {self.saat} - {self.alan} - {self.sorun_tipi} ({self.sorun_seviyesi})"
    
    def get_fotograf_url(self):
        """CloudCube'dan fotoğrafın URL'sini döndür"""
        if not self.fotograf:
            return None
            
        if hasattr(settings, 'CLOUDCUBE_URL') and settings.CLOUDCUBE_URL and self.fotograf:
            # CloudCube'a erişim URL'sini oluştur
            if 's3.amazonaws.com' in settings.CLOUDCUBE_URL:
                # Eğer URL içinde dosya adı varsa
                if hasattr(self.fotograf, 'name'):
                    file_name = self.fotograf.name
                    if file_name.startswith('/'):
                        file_name = file_name[1:]
                    return f"{settings.CLOUDCUBE_URL.rstrip('/')}/public/gonullu_sorun_fotolar/{file_name}"
                # Eğer fotograf.url varsa direkt olarak kullan
                elif hasattr(self.fotograf, 'url'):
                    return self.fotograf.url
        # Django'nun kendi URL mekanizmasını kullan
        try:
            return self.fotograf.url
        except:
            return None

    class Meta:
        verbose_name = 'Gönüllü Sorun Verisi'
        verbose_name_plural = 'Gönüllü Sorun Verileri'
        db_table = 'gonullu_sorun_veriler'

class GonulluSorunFotograf(models.Model):
    """Gönüllü sorun bildirimlerine ait fotoğraf modeli"""
    sorun = models.ForeignKey(GonulluSorunVeriler, on_delete=models.CASCADE, related_name='fotograflar')
    fotograf = models.ImageField(
        upload_to='', 
        storage=GonulluSorunStorage() if hasattr(settings, 'CLOUDCUBE_URL') and settings.CLOUDCUBE_URL else None
    )
    added_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Fotoğraf - {self.sorun}"
    
    def get_fotograf_url(self):
        """CloudCube'dan fotoğrafın URL'sini döndür"""
        if not self.fotograf:
            return None
            
        if hasattr(settings, 'CLOUDCUBE_URL') and settings.CLOUDCUBE_URL and self.fotograf:
            # CloudCube'a erişim URL'sini oluştur
            if 's3.amazonaws.com' in settings.CLOUDCUBE_URL:
                # Eğer URL içinde dosya adı varsa
                if hasattr(self.fotograf, 'name'):
                    file_name = self.fotograf.name
                    if file_name.startswith('/'):
                        file_name = file_name[1:]
                    return f"{settings.CLOUDCUBE_URL.rstrip('/')}/public/gonullu_sorun_fotolar/{file_name}"
                # Eğer fotograf.url varsa direkt olarak kullan
                elif hasattr(self.fotograf, 'url'):
                    return self.fotograf.url
        # Django'nun kendi URL mekanizmasını kullan
        try:
            return self.fotograf.url
        except:
            return None
    
    class Meta:
        verbose_name = 'Gönüllü Sorun Fotoğrafı'
        verbose_name_plural = 'Gönüllü Sorun Fotoğrafları'
        db_table = 'gonullu_sorun_fotograflar'

class SorumluVeriler(models.Model):
    kisi = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sorumlu_veriler')
    gun = models.DateField()
    personel_yemek_siparis = models.PositiveIntegerField()
    taseron_yemek_siparis = models.PositiveIntegerField()
    submitteddate = models.DateField(auto_now_add=True)
    submittedtime = models.TimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.kisi.get_full_name()} - {self.gun} - Personel: {self.personel_yemek_siparis} - Taşeron: {self.taseron_yemek_siparis}"

    class Meta:
        verbose_name = 'Sorumlu Verisi'
        verbose_name_plural = 'Sorumlu Verileri'
        db_table = 'sorumlu_veriler'

class SistemAyarlari(models.Model):
    """Sistem genelinde kullanılan ayarlar"""
    anahtar = models.CharField(max_length=50, unique=True)
    deger = models.CharField(max_length=255)
    aciklama = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.anahtar}: {self.deger}"

    class Meta:
        verbose_name = "Sistem Ayarı"
        verbose_name_plural = "Sistem Ayarları"
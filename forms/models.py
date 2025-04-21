from django.db import models
from django.conf import settings

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
    gun = models.DateField()
    saat = models.TimeField()
    alan = models.CharField(max_length=100)
    aciklama = models.TextField()
    fotograf = models.ImageField(upload_to='gonullu_durum_fotolar/', blank=True, null=True)
    submitteddate = models.DateField(auto_now_add=True)
    submittedtime = models.TimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.kisi.get_full_name()} - {self.gun} - {self.saat} - {self.alan}"

    class Meta:
        verbose_name = 'Gönüllü Durum Verisi'
        verbose_name_plural = 'Gönüllü Durum Verileri'
        db_table = 'gonullu_durum_veriler'

class GonulluSorunVeriler(models.Model):
    kisi = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='gonullu_sorun_veriler')
    gun = models.DateField()
    saat = models.TimeField()
    alan = models.CharField(max_length=100)
    aciklama = models.TextField()
    fotograf = models.ImageField(upload_to='gonullu_sorun_fotolar/', blank=True, null=True)
    submitteddate = models.DateField(auto_now_add=True)
    submittedtime = models.TimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.kisi.get_full_name()} - {self.gun} - {self.saat} - {self.alan}"

    class Meta:
        verbose_name = 'Gönüllü Sorun Verisi'
        verbose_name_plural = 'Gönüllü Sorun Verileri'
        db_table = 'gonullu_sorun_veriler'

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
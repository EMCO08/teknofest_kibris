from django.contrib import admin
from .models import (
    T3PersonelAtama, 
    T3PersonelVeriler, 
    GonulluDurumVeriler, 
    GonulluSorunVeriler, 
    SorumluVeriler

)

@admin.register(T3PersonelAtama)
class T3PersonelAtamaAdmin(admin.ModelAdmin):
    list_display = ('kisi', 'koordinatorluk', 'birim')
    list_filter = ('koordinatorluk', 'birim')
    search_fields = ('kisi__tc', 'kisi__isim', 'kisi__soyisim', 'koordinatorluk', 'birim')

@admin.register(T3PersonelVeriler)
class T3PersonelVerilerAdmin(admin.ModelAdmin):
    list_display = ('kisi', 'koordinatorluk', 'birim', 'siparis_sayisi', 'submitteddate', 'submittedtime')
    list_filter = ('koordinatorluk', 'birim', 'submitteddate')
    search_fields = ('kisi__tc', 'kisi__isim', 'kisi__soyisim', 'koordinatorluk', 'birim')
    readonly_fields = ('submitteddate', 'submittedtime')

@admin.register(GonulluDurumVeriler)
class GonulluDurumVerilerAdmin(admin.ModelAdmin):
    list_display = ('kisi', 'gun', 'saat', 'alan', 'submitteddate', 'submittedtime')
    list_filter = ('gun', 'alan', 'submitteddate')
    search_fields = ('kisi__tc', 'kisi__isim', 'kisi__soyisim', 'alan', 'aciklama')
    readonly_fields = ('submitteddate', 'submittedtime')

@admin.register(GonulluSorunVeriler)
class GonulluSorunVerilerAdmin(admin.ModelAdmin):
    list_display = ('kisi', 'gun', 'saat', 'alan', 'submitteddate', 'submittedtime')
    list_filter = ('gun', 'alan', 'submitteddate')
    search_fields = ('kisi__tc', 'kisi__isim', 'kisi__soyisim', 'alan', 'aciklama')
    readonly_fields = ('submitteddate', 'submittedtime')

@admin.register(SorumluVeriler)
class SorumluVerilerAdmin(admin.ModelAdmin):
    list_display = ('kisi', 'gun', 'personel_yemek_siparis', 'taseron_yemek_siparis', 'submitteddate', 'submittedtime')
    list_filter = ('gun', 'submitteddate')
    search_fields = ('kisi__tc', 'kisi__isim', 'kisi__soyisim')
    readonly_fields = ('submitteddate', 'submittedtime')
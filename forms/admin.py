from django.contrib import admin
from .models import (
    T3PersonelAtama, 
    T3PersonelVeriler, 
    GonulluDurumVeriler, 
    GonulluSorunVeriler, 
    SorumluVeriler,
    GonulluDurumFotograf,
    GonulluSorunFotograf,
    YeniKelime
)

@admin.register(T3PersonelAtama)
class T3PersonelAtamaAdmin(admin.ModelAdmin):
    list_display = ('kisi', 'koordinatorluk', 'birim', 'coffee_break')
    list_filter = ('koordinatorluk', 'birim', 'coffee_break')
    search_fields = ('kisi__tc', 'kisi__isim', 'kisi__soyisim', 'koordinatorluk', 'birim')

@admin.register(T3PersonelVeriler)
class T3PersonelVerilerAdmin(admin.ModelAdmin):
    list_display = ('kisi', 'koordinatorluk', 'birim', 'ogle_yemegi', 'aksam_yemegi', 'lunchbox', 'coffee_break', 'submitteddate', 'submittedtime')
    list_filter = ('koordinatorluk', 'birim', 'submitteddate')
    search_fields = ('kisi__tc', 'kisi__isim', 'kisi__soyisim', 'koordinatorluk', 'birim')
    readonly_fields = ('submitteddate', 'submittedtime')

class GonulluDurumFotografInline(admin.TabularInline):
    model = GonulluDurumFotograf
    extra = 0
    readonly_fields = ['fotograf_preview']
    
    def fotograf_preview(self, obj):
        if obj.fotograf:
            return obj.get_fotograf_url()
        return "Fotoğraf yok"
    
    fotograf_preview.short_description = "Fotoğraf Önizleme"

class GonulluDurumVerilerAdmin(admin.ModelAdmin):
    list_display = ('kisi', 'gun', 'alan', 'saat', 'catering_durum', 'submitteddate')
    list_filter = ('gun', 'alan', 'catering_durum', 'submitteddate')
    search_fields = ('kisi__first_name', 'kisi__last_name', 'alan')
    readonly_fields = ['fotograf_preview']
    inlines = [GonulluDurumFotografInline]
    
    def fotograf_preview(self, obj):
        # Geriye dönük uyumluluk için eski fotograf alanını da göster
        if obj.fotograf:
            return obj.get_fotograf_url() or "Fotoğraf yok"
        return "Fotoğraf yok"
    
    fotograf_preview.short_description = "Eski Fotoğraf (Geriye Dönük)"

class GonulluSorunFotografInline(admin.TabularInline):
    model = GonulluSorunFotograf
    extra = 0
    readonly_fields = ['fotograf_preview']
    
    def fotograf_preview(self, obj):
        if obj.fotograf:
            return obj.get_fotograf_url()
        return "Fotoğraf yok"
    
    fotograf_preview.short_description = "Fotoğraf Önizleme"

class GonulluSorunVerilerAdmin(admin.ModelAdmin):
    list_display = ('kisi', 'gun', 'alan', 'sorun_tipi', 'sorun_seviyesi', 'submitteddate')
    list_filter = ('gun', 'alan', 'sorun_tipi', 'sorun_seviyesi', 'submitteddate')
    search_fields = ('kisi__first_name', 'kisi__last_name', 'alan', 'aciklama')
    readonly_fields = ['fotograf_preview']
    inlines = [GonulluSorunFotografInline]
    
    def fotograf_preview(self, obj):
        # Geriye dönük uyumluluk için eski fotograf alanını da göster
        if obj.fotograf:
            return obj.get_fotograf_url() or "Fotoğraf yok"
        return "Fotoğraf yok"
    
    fotograf_preview.short_description = "Eski Fotoğraf (Geriye Dönük)"

class SorumluVerilerAdmin(admin.ModelAdmin):
    list_display = ('kisi', 'gun', 'personel_yemek_siparis', 'taseron_yemek_siparis', 'submitteddate')
    list_filter = ('gun', 'submitteddate')
    search_fields = ('kisi__first_name', 'kisi__last_name')

@admin.register(YeniKelime)
class YeniKelimeAdmin(admin.ModelAdmin):
    list_display = ('kullanici', 'kelime', 'anlam', 'ogrenme_tarihi')
    list_filter = ('kullanici', 'ogrenme_tarihi')
    search_fields = ('kullanici__first_name', 'kullanici__last_name', 'kelime', 'anlam')
    readonly_fields = ('ogrenme_tarihi',)
    ordering = ('-ogrenme_tarihi',)

admin.site.register(GonulluDurumVeriler, GonulluDurumVerilerAdmin)
admin.site.register(GonulluSorunVeriler, GonulluSorunVerilerAdmin)
admin.site.register(SorumluVeriler, SorumluVerilerAdmin)
admin.site.register(GonulluDurumFotograf)
admin.site.register(GonulluSorunFotograf)
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User, UserLog

class UserAdmin(BaseUserAdmin):
    list_display = ('tc', 'isim', 'soyisim', 'role', 'is_active', 'is_staff')
    list_filter = ('role', 'is_active', 'is_staff')
    fieldsets = (
        (None, {'fields': ('tc', 'password')}),
        (_('Kişisel Bilgiler'), {'fields': ('isim', 'soyisim', 'tel_no')}),
        (_('İzinler'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'role', 'groups', 'user_permissions')}),
        (_('Önemli Tarihler'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('tc', 'isim', 'soyisim', 'password1', 'password2', 'role', 'is_staff', 'is_active'),
        }),
    )
    search_fields = ('tc', 'isim', 'soyisim')
    ordering = ('tc',)

class UserLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'islem', 'sayfa', 'tarih', 'saat', 'ip')
    list_filter = ('tarih', 'islem', 'sayfa')
    search_fields = ('user__tc', 'user__isim', 'user__soyisim', 'islem', 'sayfa')
    readonly_fields = ('user', 'islem', 'sayfa', 'tarih', 'saat', 'ip', 'tarayici_bilgisi')
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False

admin.site.register(User, UserAdmin)
admin.site.register(UserLog, UserLogAdmin)

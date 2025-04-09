from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone

class UserManager(BaseUserManager):
    def create_user(self, tc, password=None, **extra_fields):
        if not tc:
            raise ValueError('TC Kimlik Numarası gereklidir.')
        user = self.model(tc=tc, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, tc, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')
        return self.create_user(tc, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('gonullu', 'Gönüllü'),
        ('t3personel', 'T3 Personel'),
        ('sorumlu', 'Sorumlu'),
        ('izleyici', 'İzleyici'),
        ('admin', 'Admin'),
    )
    
    tc = models.CharField(max_length=11, unique=True)
    tel_no = models.CharField(max_length=15, blank=True, null=True)
    isim = models.CharField(max_length=50)
    soyisim = models.CharField(max_length=50)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='gonullu')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    submitteddate = models.DateField(auto_now_add=True)
    submittedtime = models.TimeField(auto_now_add=True)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'tc'
    REQUIRED_FIELDS = ['isim', 'soyisim', 'role']
    
    def __str__(self):
        return f"{self.isim} {self.soyisim} ({self.tc})"
    
    def get_full_name(self):
        return f"{self.isim} {self.soyisim}"
    
    def get_short_name(self):
        return self.isim
    
    class Meta:
        verbose_name = 'Kullanıcı'
        verbose_name_plural = 'Kullanıcılar'
        db_table = 'roles'

class UserLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='logs')
    islem = models.CharField(max_length=255)
    sayfa = models.CharField(max_length=255)
    tarih = models.DateField(auto_now_add=True)
    saat = models.TimeField(auto_now_add=True)
    ip = models.GenericIPAddressField()
    tarayici_bilgisi = models.TextField()
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.islem} - {self.tarih} {self.saat}"
    
    class Meta:
        verbose_name = 'Kullanıcı Logu'
        verbose_name_plural = 'Kullanıcı Logları'
        db_table = 'logs'

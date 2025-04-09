from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard_home, name='home'),
    path('t3personel/', views.t3personel_dashboard, name='t3personel'),
    path('gonullu/durum/', views.gonullu_durum_dashboard, name='gonullu_durum'),
    path('gonullu/sorun/', views.gonullu_sorun_dashboard, name='gonullu_sorun'),
    path('sorumlu/', views.sorumlu_dashboard, name='sorumlu'),
    path('sistem-ayarlari-guncelle/', views.sistem_ayarlari_guncelle, name='sistem_ayarlari_guncelle'),
    path('t3personel/atama-ekle/', views.t3personel_atama_ekle, name='t3personel_atama_ekle'),
    path('t3personel/get-koordinatorluk/<int:user_id>/', views.get_koordinatorluk_for_user, name='get_koordinatorluk_for_user'),
] 
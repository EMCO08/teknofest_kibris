from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User, UserLog
from django.views.decorators.csrf import ensure_csrf_cookie

def log_user_action(request, action, page):
    """Kullanıcı eylemlerini loglar"""
    if request.user.is_authenticated:
        UserLog.objects.create(
            user=request.user,
            islem=action,
            sayfa=page,
            ip=request.META.get('REMOTE_ADDR', '0.0.0.0'),
            tarayici_bilgisi=request.META.get('HTTP_USER_AGENT', 'Bilinmiyor')
        )

@ensure_csrf_cookie
def login_view(request):
    """Kullanıcı giriş sayfası"""
    if request.user.is_authenticated:
        return redirect('accounts:home')
    
    if request.method == 'POST':
        tc = request.POST.get('tc')
        password = request.POST.get('password')
        
        user = authenticate(request, tc=tc, password=password)
        
        if user is not None:
            login(request, user)
            log_user_action(request, 'Giriş Yapıldı', 'Login')
            
            # Kullanıcı rolüne göre yönlendirme
            if user.role == 'gonullu':
                return redirect('forms:gonullu_form')
            elif user.role == 't3personel':
                return redirect('forms:t3personel_form')
            elif user.role == 'sorumlu':
                return redirect('forms:sorumlu_form')
            elif user.role == 'izleyici' or user.role == 'admin':
                return redirect('dashboard:home')
            else:
                return redirect('accounts:home')
        else:
            messages.error(request, 'TC Kimlik Numarası veya şifre hatalı!')
    
    return render(request, 'accounts/login.html')

@login_required
def home(request):
    """Ana sayfa"""
    log_user_action(request, 'Ana Sayfa Görüntülendi', 'Home')
    
    # Kullanıcı rolüne göre yönlendirme
    if request.user.role == 'gonullu':
        return redirect('forms:gonullu_form')
    elif request.user.role == 't3personel':
        return redirect('forms:t3personel_form')
    elif request.user.role == 'sorumlu':
        return redirect('forms:sorumlu_form')
    elif request.user.role == 'izleyici' or request.user.role == 'admin':
        return redirect('dashboard:home')
    
    return render(request, 'accounts/home.html')

@login_required
def logout_view(request):
    """Kullanıcı çıkış sayfası"""
    log_user_action(request, 'Çıkış Yapıldı', 'Logout')
    logout(request)
    messages.success(request, 'Başarıyla çıkış yaptınız.')
    return redirect('accounts:login')

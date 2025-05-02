// TC Kimlik Numarası doğrulama
document.addEventListener('DOMContentLoaded', function() {
    var tcInput = document.getElementById('tc');
    if (tcInput) {
        tcInput.addEventListener('input', function(e) {
            this.value = this.value.replace(/[^0-9]/g, '');
            if (this.value.length > 11) {
                this.value = this.value.slice(0, 11);
            }
        });
    }

    // Şifre göster/gizle butonu için click event'i
    var togglePasswordBtn = document.querySelector('.toggle-password');
    if (togglePasswordBtn) {
        togglePasswordBtn.addEventListener('click', togglePasswordVisibility);
    }
});

// Şifre göster/gizle fonksiyonu
function togglePasswordVisibility() {
    try {
        var passwordInput = document.getElementById('password');
        var eyeIcon = document.getElementById('eyeIcon');
        
        if (passwordInput.type === 'password') {
            passwordInput.type = 'text';
            eyeIcon.classList.remove('fa-eye');
            eyeIcon.classList.add('fa-eye-slash');
            console.log('Şifre gösteriliyor'); // Debug için konsola yazdırma
        } else {
            passwordInput.type = 'password';
            eyeIcon.classList.remove('fa-eye-slash');
            eyeIcon.classList.add('fa-eye');
            console.log('Şifre gizleniyor'); // Debug için konsola yazdırma
        }
    } catch (error) {
        console.error('Şifre göster/gizle hatası:', error);
    }
} 
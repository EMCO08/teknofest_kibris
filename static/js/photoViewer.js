/**
 * Fotoğraf Görüntüleyici
 * Gönüllü durum ve sorun sayfaları için fotoğraf görüntüleme işlevleri
 */
document.addEventListener('DOMContentLoaded', function() {
    // Sayfa yüklendiğinde tüm fotoğrafları önbelleğe al
    var photoUrls = [];
    document.querySelectorAll('[data-photo-url]').forEach(function(el) {
        photoUrls.push(el.getAttribute('data-photo-url'));
    });
    
    // Fotoğrafları arka planda yükle
    photoUrls.forEach(function(url) {
        var img = new Image();
        img.src = url;
    });
    
    // Fotoğraf modalı için
    var photoModal = document.getElementById('photoModal');
    var modalPhoto = document.getElementById('modalPhoto');
    var photoLoader = document.getElementById('photoLoader');
    var photoModalLabel = document.getElementById('photoModalLabel');
    var downloadBtn = document.getElementById('downloadBtn');
    var zoomInBtn = document.getElementById('zoomInBtn');
    var zoomOutBtn = document.getElementById('zoomOutBtn');
    var resetZoomBtn = document.getElementById('resetZoomBtn');
    
    var currentScale = 1;
    var minScale = 0.5;
    var maxScale = 3;
    var scaleStep = 0.2;
    
    // Yakınlaştırma fonksiyonu
    function updateZoom() {
        modalPhoto.style.transform = `scale(${currentScale})`;
    }
    
    // Yakınlaştır butonu
    if (zoomInBtn) {
        zoomInBtn.addEventListener('click', function() {
            if (currentScale < maxScale) {
                currentScale += scaleStep;
                updateZoom();
            }
        });
    }
    
    // Uzaklaştır butonu
    if (zoomOutBtn) {
        zoomOutBtn.addEventListener('click', function() {
            if (currentScale > minScale) {
                currentScale -= scaleStep;
                updateZoom();
            }
        });
    }
    
    // Sıfırla butonu
    if (resetZoomBtn) {
        resetZoomBtn.addEventListener('click', function() {
            currentScale = 1;
            updateZoom();
        });
    }
    
    // Fotoğrafa tıklama ile büyütme
    if (modalPhoto) {
        modalPhoto.addEventListener('click', function() {
            if (modalPhoto.classList.contains('zoomed')) {
                modalPhoto.classList.remove('zoomed');
            } else {
                modalPhoto.classList.add('zoomed');
            }
        });
    }
    
    // Fotoğraf butonlarına tıklandığında
    document.querySelectorAll('.show-photo-btn').forEach(function(button) {
        button.addEventListener('click', function() {
            var photoUrl = this.getAttribute('data-photo-url');
            var photoTitle = this.getAttribute('data-photo-title');
            
            // Modal başlığını ayarla
            photoModalLabel.textContent = photoTitle;
            
            // İndirme butonunu ayarla
            downloadBtn.href = photoUrl;
            
            // Yükleme göstergesini göster, fotoğrafı gizle
            photoLoader.style.display = 'flex';
            modalPhoto.style.display = 'none';
            
            // Ölçeği sıfırla
            currentScale = 1;
            modalPhoto.classList.remove('zoomed');
            updateZoom();
            
            // Fotoğrafı yükle
            modalPhoto.src = photoUrl;
            
            // Fotoğraf yüklendiğinde
            modalPhoto.onload = function() {
                // Kısa bir gecikme ekleyerek yanıp sönme etkisini önle
                setTimeout(function() {
                    photoLoader.style.display = 'none';
                    modalPhoto.style.display = 'block';
                }, 300);
            };
        });
    });
    
    // Modal kapandığında
    if (photoModal) {
        photoModal.addEventListener('hidden.bs.modal', function() {
            modalPhoto.src = '';
            currentScale = 1;
            modalPhoto.classList.remove('zoomed');
            updateZoom();
        });
    }
}); 
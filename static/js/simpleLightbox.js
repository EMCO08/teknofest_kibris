// Simple Lightbox
document.addEventListener('DOMContentLoaded', function() {
    console.log('Simple Lightbox yüklendi');
    
    // Gerekli HTML yapısını oluştur ve body sonuna ekle
    const lightboxHTML = `
        <div id="simpleLightbox" class="simple-lightbox">
            <div class="simple-lightbox-content">
                <span class="simple-lightbox-close">&times;</span>
                <div class="simple-lightbox-controls">
                    <button class="zoom-in-btn"><i class="fas fa-search-plus"></i></button>
                    <button class="zoom-out-btn"><i class="fas fa-search-minus"></i></button>
                    <button class="reset-zoom-btn"><i class="fas fa-undo"></i></button>
                    <a href="#" class="download-btn" download><i class="fas fa-download"></i></a>
                </div>
                <div class="simple-lightbox-loader">
                    <div class="spinner"></div>
                </div>
                <img class="simple-lightbox-image" src="" alt="Fotoğraf">
                <div class="simple-lightbox-caption"></div>
            </div>
        </div>
    `;
    
    // CSS stillerini oluştur ve head'e ekle
    const lightboxCSS = `
        .simple-lightbox {
            display: none;
            position: fixed;
            z-index: 9999;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            overflow: auto;
            background-color: rgba(0,0,0,0.9);
        }
        
        .simple-lightbox-content {
            position: relative;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            height: 100%;
            padding: 20px;
        }
        
        .simple-lightbox-close {
            position: absolute;
            top: 10px;
            right: 20px;
            color: #f1f1f1;
            font-size: 30px;
            font-weight: bold;
            cursor: pointer;
            z-index: 1000;
        }
        
        .simple-lightbox-image {
            max-width: 90%;
            max-height: 80vh;
            transition: transform 0.3s ease;
        }
        
        .simple-lightbox-caption {
            color: #f1f1f1;
            padding: 10px 0;
            text-align: center;
            width: 100%;
        }
        
        .simple-lightbox-controls {
            position: absolute;
            bottom: 20px;
            display: flex;
            gap: 10px;
            z-index: 1000;
        }
        
        .simple-lightbox-controls button,
        .simple-lightbox-controls a {
            background-color: rgba(255, 255, 255, 0.2);
            color: white;
            border: none;
            padding: 8px 12px;
            border-radius: 4px;
            cursor: pointer;
        }
        
        .simple-lightbox-controls button:hover,
        .simple-lightbox-controls a:hover {
            background-color: rgba(255, 255, 255, 0.3);
        }
        
        .simple-lightbox-loader {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            z-index: 100;
            display: none;
        }
        
        .simple-lightbox-loader .spinner {
            border: 5px solid #f3f3f3;
            border-top: 5px solid #3498db;
            border-radius: 50%;
            width: 50px;
            height: 50px;
            animation: spin 2s linear infinite;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    `;
    
    // CSS'i head'e ekle
    const style = document.createElement('style');
    style.textContent = lightboxCSS;
    document.head.appendChild(style);
    
    // Lightbox container'ı body'ye ekle
    const lightboxContainer = document.createElement('div');
    lightboxContainer.innerHTML = lightboxHTML;
    document.body.appendChild(lightboxContainer.firstElementChild);
    
    // Değişkenler
    const lightbox = document.getElementById('simpleLightbox');
    const lightboxImage = lightbox.querySelector('.simple-lightbox-image');
    const lightboxCaption = lightbox.querySelector('.simple-lightbox-caption');
    const lightboxClose = lightbox.querySelector('.simple-lightbox-close');
    const lightboxLoader = lightbox.querySelector('.simple-lightbox-loader');
    const zoomInBtn = lightbox.querySelector('.zoom-in-btn');
    const zoomOutBtn = lightbox.querySelector('.zoom-out-btn');
    const resetZoomBtn = lightbox.querySelector('.reset-zoom-btn');
    const downloadBtn = lightbox.querySelector('.download-btn');
    
    let currentScale = 1;
    const minScale = 0.5;
    const maxScale = 3;
    const scaleStep = 0.2;
    
    // Tüm show-photo-btn butonlarına tıklama olayı ekle
    const photoButtons = document.querySelectorAll('.show-photo-btn');
    photoButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            
            const photoUrl = this.getAttribute('data-photo-url');
            const photoTitle = this.getAttribute('data-photo-title');
            
            console.log('Fotoğraf gösterilecek:', photoUrl);
            
            // Başlık ayarla
            lightboxCaption.textContent = photoTitle;
            
            // İndirme butonu ayarla
            downloadBtn.href = photoUrl;
            
            // Yükleme göstergesini göster
            lightboxLoader.style.display = 'block';
            lightboxImage.style.display = 'none';
            
            // Lightbox'ı göster
            lightbox.style.display = 'block';
            
            // Fotoğrafı yükle
            lightboxImage.src = photoUrl;
            
            // Fotoğraf yüklendiğinde
            lightboxImage.onload = function() {
                // Yükleme göstergesini gizle, fotoğrafı göster
                lightboxLoader.style.display = 'none';
                lightboxImage.style.display = 'block';
                
                // Zoom'u sıfırla
                currentScale = 1;
                updateZoom();
            };
        });
    });
    
    // Zoom kontrol fonksiyonu
    function updateZoom() {
        lightboxImage.style.transform = `scale(${currentScale})`;
    }
    
    // Yakınlaştır butonuna tıklama olayı
    zoomInBtn.addEventListener('click', function() {
        if (currentScale < maxScale) {
            currentScale += scaleStep;
            updateZoom();
        }
    });
    
    // Uzaklaştır butonuna tıklama olayı
    zoomOutBtn.addEventListener('click', function() {
        if (currentScale > minScale) {
            currentScale -= scaleStep;
            updateZoom();
        }
    });
    
    // Sıfırla butonuna tıklama olayı
    resetZoomBtn.addEventListener('click', function() {
        currentScale = 1;
        updateZoom();
    });
    
    // Fotoğrafa tıklama ile büyütme
    lightboxImage.addEventListener('click', function() {
        if (currentScale === 1) {
            currentScale = 2;
        } else {
            currentScale = 1;
        }
        updateZoom();
    });
    
    // Kapatma butonuna tıklama olayı
    lightboxClose.addEventListener('click', function() {
        lightbox.style.display = 'none';
        lightboxImage.src = '';
    });
    
    // Dışarıya tıklama ile kapatma
    lightbox.addEventListener('click', function(e) {
        if (e.target === lightbox) {
            lightbox.style.display = 'none';
            lightboxImage.src = '';
        }
    });
    
    // ESC tuşuna basma ile kapatma
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && lightbox.style.display === 'block') {
            lightbox.style.display = 'none';
            lightboxImage.src = '';
        }
    });
}); 
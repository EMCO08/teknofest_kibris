/**
 * Fotoğraf Görüntüleyici
 * Gönüllü durum ve sorun sayfaları için fotoğraf görüntüleme işlevleri
 */
$(document).ready(function() {
    console.log("PhotoViewer.js yüklendi");
    
    // Fotoğraf butonlarına tıklandığında
    $('.show-photo-btn').on('click', function() {
        console.log("Fotoğraf butonuna tıklandı");
        
        var photoUrl = $(this).data('photo-url');
        var photoTitle = $(this).data('photo-title');
        
        // Modal başlığını ayarla
        $('#photoModalLabel').text(photoTitle);
        
        // İndirme butonunu ayarla
        $('#downloadBtn').attr('href', photoUrl);
        
        // Yükleme göstergesini göster, fotoğrafı gizle
        $('#photoLoader').css('display', 'flex');
        $('#modalPhoto').hide();
        
        // Ölçeği sıfırla
        currentScale = 1;
        $('#modalPhoto').removeClass('zoomed');
        updateZoom();
        
        // Fotoğrafı yükle
        $('#modalPhoto').attr('src', photoUrl);
        
        // Fotoğraf yüklendiğinde
        $('#modalPhoto').on('load', function() {
            // Kısa bir gecikme ekleyerek yanıp sönme etkisini önle
            setTimeout(function() {
                $('#photoLoader').hide();
                $('#modalPhoto').show();
            }, 300);
        });
        
        // Modalı aç
        $('#photoModal').modal('show');
    });
    
    // Değişkenler
    var currentScale = 1;
    var minScale = 0.5;
    var maxScale = 3;
    var scaleStep = 0.2;
    
    // Yakınlaştırma fonksiyonu
    function updateZoom() {
        $('#modalPhoto').css('transform', 'scale(' + currentScale + ')');
    }
    
    // Yakınlaştır butonu
    $('#zoomInBtn').on('click', function() {
        console.log("Yakınlaştır butonuna tıklandı");
        if (currentScale < maxScale) {
            currentScale += scaleStep;
            updateZoom();
        }
    });
    
    // Uzaklaştır butonu
    $('#zoomOutBtn').on('click', function() {
        console.log("Uzaklaştır butonuna tıklandı");
        if (currentScale > minScale) {
            currentScale -= scaleStep;
            updateZoom();
        }
    });
    
    // Sıfırla butonu
    $('#resetZoomBtn').on('click', function() {
        console.log("Sıfırla butonuna tıklandı");
        currentScale = 1;
        updateZoom();
    });
    
    // Fotoğrafa tıklama ile büyütme
    $(document).on('click', '#modalPhoto', function() {
        console.log("Fotoğrafa tıklandı");
        if ($(this).hasClass('zoomed')) {
            $(this).removeClass('zoomed');
        } else {
            $(this).addClass('zoomed');
        }
    });
    
    // Modal kapandığında
    $('#photoModal').on('hidden.bs.modal', function() {
        console.log("Modal kapandı");
        $('#modalPhoto').attr('src', '');
        currentScale = 1;
        $('#modalPhoto').removeClass('zoomed');
        updateZoom();
    });
}); 
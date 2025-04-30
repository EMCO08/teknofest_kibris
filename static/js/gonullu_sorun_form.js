document.addEventListener('DOMContentLoaded', function() {
    // Mevcut saati varsayılan olarak ayarla
    const now = new Date();
    const hours = String(now.getHours()).padStart(2, '0');
    const minutes = String(now.getMinutes()).padStart(2, '0');
    document.getElementById('saat').value = `${hours}:${minutes}`;
    
    // Fotoğraf önizleme
    const fileInput = document.getElementById('fotograf');
    const previewContainer = document.getElementById('preview-container');
    const previewContainer2 = document.getElementById('images-preview-container');
    
    fileInput.addEventListener('change', function() {
        // Önizleme konteynerini temizle
        previewContainer2.innerHTML = '';
        
        if (this.files && this.files.length > 0) {
            // Maksimum 5 fotoğraf kontrolü
            const maxFiles = 5;
            const fileCount = Math.min(this.files.length, maxFiles);
            
            if (this.files.length > maxFiles) {
                alert(`En fazla ${maxFiles} fotoğraf yükleyebilirsiniz. İlk ${maxFiles} fotoğraf seçildi.`);
            }
            
            // Seçilen fotoğrafları önizle
            for (let i = 0; i < fileCount; i++) {
                const reader = new FileReader();
                const imgContainer = document.createElement('div');
                imgContainer.className = 'mb-2 d-inline-block mx-1';
                
                const img = document.createElement('img');
                img.className = 'img-fluid img-thumbnail';
                img.style.maxHeight = '150px';
                img.alt = `Fotoğraf ${i+1} Önizleme`;
                
                reader.onload = e => {
                    img.src = e.target.result;
                };
                
                reader.readAsDataURL(this.files[i]);
                imgContainer.appendChild(img);
                previewContainer2.appendChild(imgContainer);
            }
            
            previewContainer.style.display = 'block';
        } else {
            previewContainer.style.display = 'none';
        }
    });
}); 
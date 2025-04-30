document.addEventListener('DOMContentLoaded', function () {
    const now = new Date();
    document.getElementById('saat').value = now.toTimeString().slice(0,5);

    const cateringVar = document.getElementById('catering_var');
    const cateringYok = document.getElementById('catering_yok');
    const cateringContainer = document.getElementById('catering_urunleri_container');
    const cateringInput = document.getElementById('catering_urunleri_input');

    cateringVar.onclick = () => cateringContainer.style.display = 'block';
    cateringYok.onclick = () => cateringContainer.style.display = 'none';

    if (cateringVar.checked) {
        cateringContainer.style.display = 'block';
    }

    const items = document.querySelectorAll('.catering-item');
    items.forEach(item => {
        item.addEventListener('click', () => {
            item.classList.toggle('selected');
            const selected = document.querySelectorAll('.catering-item.selected');
            const values = Array.from(selected).map(i => i.dataset.value);
            cateringInput.value = JSON.stringify(values);
        });
    });

    const fileInput = document.getElementById('fotograf');
    const previewContainer = document.getElementById('preview-container');
    const previewContainer2 = document.getElementById('images-preview-container');

    fileInput.addEventListener('change', function () {
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
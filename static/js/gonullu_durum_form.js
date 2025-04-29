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
    const previewImage = document.getElementById('preview-image');

    fileInput.addEventListener('change', function () {
        if (this.files && this.files[0]) {
            const reader = new FileReader();
            reader.onload = e => {
                previewImage.src = e.target.result;
                previewContainer.style.display = 'block';
            };
            reader.readAsDataURL(this.files[0]);
        } else {
            previewContainer.style.display = 'none';
        }
    });
}); 
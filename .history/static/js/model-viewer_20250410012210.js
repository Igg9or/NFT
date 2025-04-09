document.addEventListener('DOMContentLoaded', function() {
    // Инициализация всех 3D превью
    document.querySelectorAll('.model-preview').forEach(preview => {
        preview.addEventListener('click', function() {
            const modelUrl = this.getAttribute('data-model-url');
            const viewer = document.getElementById('model-viewer');
            viewer.src = modelUrl;
            document.getElementById('model-viewer-container').style.display = 'flex';
        });
    });
    
    // Закрытие просмотрщика
    document.querySelector('.close-viewer').addEventListener('click', function() {
        document.getElementById('model-viewer-container').style.display = 'none';
    });
});
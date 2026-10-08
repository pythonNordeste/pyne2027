const IMAGES_COUNT = 23;

function getImageUrl(index) {
    return `static/img/background/${String(index).padStart(2, '0')}.jpg`;
}

function setBackgroundImage(index) {
    document.querySelector('header.phb-slide-show').style.backgroundImage = `url("${getImageUrl(index)}")`;
}

document.addEventListener('DOMContentLoaded', function() {
    const container = document.querySelector('.phb-photos-carousel');
    if (!container) return;

    // Renderiza duas sequências para loop infinito contínuo (0 a -50%)
    for (let loop = 0; loop < 2; loop++) {
        for (let i = 0; i < IMAGES_COUNT; i++) {
            const img = document.createElement('img');
            img.src = getImageUrl(i);
            img.alt = `Parnaíba - Foto ${i + 1}`;
            img.loading = 'lazy';
            container.appendChild(img);
        }
    }
});
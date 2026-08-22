const IMAGES_COUNT = 23;

function getImageUrl(index) {
    return `static/img/background/${String(index).padStart(2, '0')}.jpg`;
}

function setBackgroundImage(index) {
    document.querySelector('header.phb-slide-show').style.backgroundImage = `url("${getImageUrl(index)}")`;
}

document.addEventListener('DOMContentLoaded', function() {
    let images = Array.from(
        { length: IMAGES_COUNT },
        (_, i) => i
    );

    const container = document.querySelector('.phb-photos-carousel');

    for (let index of images) {
        const img = document.createElement('img');
        img.src = getImageUrl(index);
        container.appendChild(img);
    }
});
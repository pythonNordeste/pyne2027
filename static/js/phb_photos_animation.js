document.addEventListener('DOMContentLoaded', async function() {
    const container = document.querySelector('.phb-photos-carousel');
    if (!container) return;

    const response = await fetch('static/img/background/manifest.json');
    if (!response.ok) return;
    const images = await response.json();
    const pictures = [];
    const loadPicture = function(picture) {
        const source = picture.querySelector('source');
        const img = picture.querySelector('img');
        source.srcset = source.dataset.srcset;
        img.src = img.dataset.src;
    };
    const observer = 'IntersectionObserver' in window
        ? new IntersectionObserver(function(entries) {
            for (const entry of entries) {
                if (!entry.isIntersecting) continue;
                loadPicture(entry.target);
                observer.unobserve(entry.target);
            }
        }, { root: container.parentElement, rootMargin: '0px 800px' })
        : null;

    for (let loop = 0; loop < 2; loop++) {
        for (const [index, image] of images.entries()) {
            const picture = document.createElement('picture');
            const source = document.createElement('source');
            const img = document.createElement('img');
            const displayWidth = Math.round(290 * image.width / image.height);
            picture.style.width = `${displayWidth}px`;
            source.type = 'image/webp';
            source.sizes = `${displayWidth}px`;
            source.dataset.srcset = image.variants.map(function(variant) {
                return `${variant.url} ${variant.width}w`;
            }).join(', ');
            img.dataset.src = image.fallback;
            img.width = image.width;
            img.height = image.height;
            img.alt = `Parnaíba - Foto ${index + 1}`;
            img.decoding = 'async';
            img.loading = observer ? 'eager' : 'lazy';
            picture.append(source, img);
            container.appendChild(picture);
            pictures.push(picture);
            if (!observer) {
                loadPicture(picture);
            }
        }
    }

    if (observer) {
        const galleryObserver = new IntersectionObserver(function(entries) {
            for (const entry of entries) {
                container.classList.toggle('is-visible', entry.isIntersecting);
                if (entry.isIntersecting) {
                    for (const picture of pictures) {
                        if (!picture.querySelector('img').hasAttribute('src')) {
                            observer.observe(picture);
                        }
                    }
                } else {
                    observer.disconnect();
                }
            }
        }, { rootMargin: '400px 0px' });
        galleryObserver.observe(container.parentElement);
    } else {
        container.classList.add('is-visible');
    }
});
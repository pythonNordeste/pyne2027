document.addEventListener('DOMContentLoaded', function() {
    const carousel = document.getElementById('destination-carousel');
    if (!carousel) return;

    const track = carousel.querySelector('.carousel-track');
    const slides = Array.from(carousel.querySelectorAll('.carousel-slide'));
    const dots = Array.from(carousel.querySelectorAll('[data-carousel-dot]'));
    const controls = carousel.querySelector('.carousel-controls');
    const toggle = carousel.querySelector('[data-carousel-toggle]');
    if (!track || slides.length < 2) return;

    const AUTOPLAY_DELAY = 7000;
    const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
    let current = 0;
    let timer = null;
    let isVisible = false;
    let isHovered = false;
    let hasFocus = false;
    // Quem prefere menos movimento começa com a troca automática pausada.
    let isPaused = reducedMotion.matches;

    const setActive = function(index) {
        current = index;
        dots.forEach(function(dot, dotIndex) {
            if (dotIndex === index) dot.setAttribute('aria-current', 'true');
            else dot.removeAttribute('aria-current');
        });
    };

    const goTo = function(index) {
        const target = (index + slides.length) % slides.length;
        track.scrollTo({
            left: slides[target].offsetLeft - track.offsetLeft,
            behavior: reducedMotion.matches ? 'auto' : 'smooth',
        });
        setActive(target);
    };

    const stop = function() {
        clearInterval(timer);
        timer = null;
    };

    const refreshAutoplay = function() {
        const shouldRun = !isPaused && isVisible && !isHovered && !hasFocus && !document.hidden;
        if (shouldRun && !timer) {
            timer = setInterval(function() { goTo(current + 1); }, AUTOPLAY_DELAY);
        } else if (!shouldRun) {
            stop();
        }
    };

    const updateToggle = function() {
        if (!toggle) return;
        toggle.setAttribute('aria-label', isPaused ? 'Retomar troca automática' : 'Pausar troca automática');
        const icon = toggle.querySelector('i');
        icon.classList.toggle('fa-pause', !isPaused);
        icon.classList.toggle('fa-play', isPaused);
    };

    carousel.querySelector('[data-carousel-prev]').addEventListener('click', function() { goTo(current - 1); });
    carousel.querySelector('[data-carousel-next]').addEventListener('click', function() { goTo(current + 1); });
    dots.forEach(function(dot) {
        dot.addEventListener('click', function() { goTo(Number(dot.dataset.carouselDot)); });
    });
    if (toggle) {
        toggle.addEventListener('click', function() {
            isPaused = !isPaused;
            updateToggle();
            refreshAutoplay();
        });
    }

    track.addEventListener('keydown', function(event) {
        if (event.key === 'ArrowRight') goTo(current + 1);
        else if (event.key === 'ArrowLeft') goTo(current - 1);
        else return;
        event.preventDefault();
    });

    // Mantém os indicadores sincronizados quando a pessoa arrasta/rola o carrossel.
    const slideObserver = new IntersectionObserver(function(entries) {
        for (const entry of entries) {
            if (entry.isIntersecting) setActive(slides.indexOf(entry.target));
        }
    }, { root: track, threshold: 0.6 });
    slides.forEach(function(slide) { slideObserver.observe(slide); });

    // Só troca automaticamente enquanto o carrossel está na tela.
    new IntersectionObserver(function(entries) {
        isVisible = entries[0].isIntersecting;
        refreshAutoplay();
    }, { threshold: 0.4 }).observe(carousel);

    carousel.addEventListener('mouseenter', function() { isHovered = true; refreshAutoplay(); });
    carousel.addEventListener('mouseleave', function() { isHovered = false; refreshAutoplay(); });
    carousel.addEventListener('focusin', function() { hasFocus = true; refreshAutoplay(); });
    carousel.addEventListener('focusout', function(event) {
        hasFocus = carousel.contains(event.relatedTarget);
        refreshAutoplay();
    });
    track.addEventListener('pointerdown', function() {
        isPaused = true;
        updateToggle();
        refreshAutoplay();
    });
    document.addEventListener('visibilitychange', refreshAutoplay);

    controls.hidden = false;
    carousel.classList.add('is-enhanced');
    setActive(0);
    updateToggle();
});

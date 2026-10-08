/**
 * Animações interativas do Hero da PyNE 2027
 * - Efeito 3D Tilt suave no emblema ao mover o mouse
 * - Respeito automático a prefers-reduced-motion
 */
document.addEventListener('DOMContentLoaded', () => {
    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (prefersReducedMotion) return;

    const hero = document.getElementById('hero');
    const tiltContainer = document.getElementById('logo-tilt');

    if (!hero || !tiltContainer || !window.matchMedia('(pointer: fine)').matches) {
        return;
    }

    let rafId = null;
    let targetRotateX = 0;
    let targetRotateY = 0;
    let currentRotateX = 0;
    let currentRotateY = 0;

    function updateTilt() {
        // Interpolação suave (lerp)
        currentRotateX += (targetRotateX - currentRotateX) * 0.1;
        currentRotateY += (targetRotateY - currentRotateY) * 0.1;

        tiltContainer.style.transform = `perspective(900px) rotateX(${currentRotateX.toFixed(2)}deg) rotateY(${currentRotateY.toFixed(2)}deg)`;

        if (Math.abs(targetRotateX - currentRotateX) > 0.05 || Math.abs(targetRotateY - currentRotateY) > 0.05) {
            rafId = requestAnimationFrame(updateTilt);
        } else {
            rafId = null;
        }
    }

    hero.addEventListener('mousemove', (e) => {
        const rect = tiltContainer.getBoundingClientRect();
        const centerX = rect.left + rect.width / 2;
        const centerY = rect.top + rect.height / 2;

        const maxAngle = 10;
        const deltaX = (e.clientX - centerX) / (window.innerWidth / 2);
        const deltaY = (e.clientY - centerY) / (window.innerHeight / 2);

        targetRotateY = Math.max(-maxAngle, Math.min(maxAngle, deltaX * maxAngle));
        targetRotateX = Math.max(-maxAngle, Math.min(maxAngle, -deltaY * maxAngle));

        if (!rafId) {
            rafId = requestAnimationFrame(updateTilt);
        }
    });

    hero.addEventListener('mouseleave', () => {
        targetRotateX = 0;
        targetRotateY = 0;
        if (!rafId) {
            rafId = requestAnimationFrame(updateTilt);
        }
    });
});

/**
 * Python Nordeste 2027 (PyNE 2027) - Interatividade da Barra de Navegação (Navbar)
 * Suporte a efeito translúcido no scroll, menu responsivo mobile e acessibilidade ARIA.
 */

document.addEventListener('DOMContentLoaded', () => {
    const navbar = document.getElementById('navbar');
    const toggleBtn = document.getElementById('navbar-toggle');
    const navMenu = document.getElementById('navbar-menu');
    const navLinks = document.querySelectorAll('.nav-link');

    if (!navbar) return;

    // 1. Efeito translúcido / vidro no scroll da página
    const handleScroll = () => {
        if (window.scrollY > 25) {
            navbar.classList.add('navbar-scrolled');
        } else {
            navbar.classList.remove('navbar-scrolled');
        }
    };

    window.addEventListener('scroll', handleScroll, { passive: true });
    handleScroll(); // Checagem inicial caso a página recarregue já rolada

    // 2. Menu hambúrguer para mobile
    if (toggleBtn && navMenu) {
        const toggleMenu = (open) => {
            const isOpen = open !== undefined ? open : !navMenu.classList.contains('navbar-menu-open');
            navMenu.classList.toggle('navbar-menu-open', isOpen);
            toggleBtn.classList.toggle('toggle-active', isOpen);
            toggleBtn.setAttribute('aria-expanded', String(isOpen));

            if (isOpen) {
                document.body.classList.add('nav-locked');
            } else {
                document.body.classList.remove('nav-locked');
            }
        };

        toggleBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            toggleMenu();
        });

        // Fechar ao clicar em qualquer link de navegação
        navLinks.forEach((link) => {
            link.addEventListener('click', () => {
                if (navMenu.classList.contains('navbar-menu-open')) {
                    toggleMenu(false);
                }
            });
        });

        // Fechar ao clicar fora da navbar
        document.addEventListener('click', (e) => {
            if (navMenu.classList.contains('navbar-menu-open') && !navbar.contains(e.target)) {
                toggleMenu(false);
            }
        });

        // Fechar com a tecla ESC para acessibilidade
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && navMenu.classList.contains('navbar-menu-open')) {
                toggleMenu(false);
                toggleBtn.focus();
            }
        });
    }
});

/**
 * Animações e Interatividade do Guará-vermelho da PyNE 2027
 * - Flapping realista de asas (alternância entre guara_up.png e guara_down.png)
 * - Interatividade ao clicar/hover no mascote do Porto das Barcas
 * - Disparo da 'Revoada dos Guarás' (Easter Egg com bando voando pela tela)
 * - Suporte total a acessibilidade e prefers-reduced-motion
 */

(function () {
    'use strict';

    const quotes = [
        "Bem-vindos ao Delta das Américas! 🪶",
        "Pessoas > Tecnologia ❤️",
        "Parnaíba 2027 vai ser inesquecível!",
        "O céu do Piauí fica vermelho ao entardecer!",
        "Nos vemos no Porto das Barcas!",
        "Mais de 10 anos de história da PyNE!",
        "Dunas, tecnologia e comunidade aberta!"
    ];

    document.addEventListener('DOMContentLoaded', () => {
        const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

        const interactiveGuara = document.getElementById('interactive-guara');
        const btnRevoada = document.getElementById('btn-revoada');
        const speechBubble = document.getElementById('guara-speech');
        const speechText = speechBubble ? speechBubble.querySelector('.speech-text') : null;
        const toast = document.getElementById('revoada-toast');
        const overlayContainer = document.getElementById('revoada-canvas-container');

        let isRevoadaActive = false;
        let quoteIndex = 0;

        // Frases dinâmicas ao passar o mouse ou focar
        if (interactiveGuara && speechText) {
            interactiveGuara.addEventListener('mouseenter', () => {
                quoteIndex = (quoteIndex + 1) % quotes.length;
                speechText.textContent = quotes[quoteIndex];
                speechBubble.classList.add('speech-visible');
            });

            interactiveGuara.addEventListener('mouseleave', () => {
                if (!isRevoadaActive) {
                    speechBubble.classList.remove('speech-visible');
                }
            });

            interactiveGuara.addEventListener('focus', () => {
                speechBubble.classList.add('speech-visible');
            });

            interactiveGuara.addEventListener('blur', () => {
                speechBubble.classList.remove('speech-visible');
            });

            // Clique no Guará ativa a Revoada
            interactiveGuara.addEventListener('click', (e) => {
                e.preventDefault();
                triggerRevoada();
            });

            interactiveGuara.addEventListener('keydown', (e) => {
                if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    triggerRevoada();
                }
            });
        }

        if (btnRevoada) {
            btnRevoada.addEventListener('click', (e) => {
                e.preventDefault();
                e.stopPropagation();
                triggerRevoada();
            });
        }

        // Também permite clicar no avatar do Guará no Hero para chamar a Revoada
        const heroGuaraAvatar = document.querySelector('.badge-guara-avatar');
        if (heroGuaraAvatar) {
            heroGuaraAvatar.style.cursor = 'pointer';
            heroGuaraAvatar.title = 'Clique para ver a Revoada dos Guarás!';
            heroGuaraAvatar.addEventListener('click', () => {
                triggerRevoada();
            });
        }

        /**
         * Dispara a Revoada dos Guarás pela tela
         */
        function triggerRevoada() {
            if (isRevoadaActive) return;
            isRevoadaActive = true;

            if (speechText && speechBubble) {
                speechText.textContent = "Olhe para o céu! Revoada no Delta! 🪶✨";
                speechBubble.classList.add('speech-visible');
            }

            // Exibe o toast acolhedor
            if (toast) {
                toast.classList.add('toast-active');
                setTimeout(() => {
                    toast.classList.remove('toast-active');
                }, 4800);
            }

            if (!overlayContainer) {
                isRevoadaActive = false;
                return;
            }

            if (prefersReducedMotion) {
                // Se o usuário preferir menos movimento, apenas mostra o toast
                setTimeout(() => {
                    isRevoadaActive = false;
                }, 1500);
                return;
            }

            overlayContainer.innerHTML = '';
            overlayContainer.classList.add('active');

            // Cria um bando de 8 guarás com trajetórias orgânicas
            const birdCount = 8;
            const screenHeight = window.innerHeight;

            for (let i = 0; i < birdCount; i++) {
                const bird = document.createElement('div');
                bird.className = `revoada-flyer flyer-${i + 1}`;
                
                // Variação de tamanho, velocidade e altura
                const size = 65 + Math.random() * 55; // 65px a 120px
                const startY = 80 + Math.random() * (screenHeight * 0.7);
                const delay = i * 0.22 + Math.random() * 0.15;
                const duration = 5.2 + Math.random() * 2.2;
                const verticalSway = 30 + Math.random() * 60;

                bird.style.width = `${size}px`;
                bird.style.height = `${size * 0.5}px`;
                bird.style.top = `${startY}px`;
                bird.style.animationDuration = `${duration}s`;
                bird.style.animationDelay = `${delay}s`;
                bird.style.setProperty('--sway-amount', `${verticalSway}px`);

                bird.innerHTML = `
                    <div class="guara-flapper">
                        <img src="static/img/guara/guara_up.png" alt="" class="guara-frame frame-up" />
                        <img src="static/img/guara/guara_down.png" alt="" class="guara-frame frame-down" />
                    </div>
                `;

                overlayContainer.appendChild(bird);
            }

            // Adiciona partículas suaves de penas/brilho
            for (let j = 0; j < 12; j++) {
                const feather = document.createElement('div');
                feather.className = 'feather-particle';
                feather.style.left = `${10 + Math.random() * 80}%`;
                feather.style.top = `${20 + Math.random() * 40}%`;
                feather.style.animationDelay = `${0.5 + Math.random() * 1.5}s`;
                feather.style.animationDuration = `${3.5 + Math.random() * 2}s`;
                overlayContainer.appendChild(feather);
            }

            // Limpa após a passagem do bando
            setTimeout(() => {
                overlayContainer.innerHTML = '';
                overlayContainer.classList.remove('active');
                isRevoadaActive = false;
                if (speechBubble) {
                    speechBubble.classList.remove('speech-visible');
                }
            }, 8500);
        }

        /**
         * 3. Guará Acompanhando a Navegação (Navbar Flight Stream & Companion Flutuante)
         */
        const navStream = document.getElementById('nav-guara-stream');
        const streamLine = document.getElementById('stream-line');
        const streamPilot = document.getElementById('stream-guara-pilot');
        const navCompanion = document.getElementById('guara-nav-companion');
        const companionTag = document.getElementById('companion-section-tag');
        const companionText = document.getElementById('companion-text');
        const btnGuaraTop = document.getElementById('btn-guara-top');

        let isScrollingTimeout = null;
        let ticking = false;

        // Mapeamento de mensagens por seção
        const sectionStories = {
            'hero': { tag: 'Boas-vindas', text: 'Sobrevoando Parnaíba 2027! 🪶' },
            'about': { tag: 'Comunidade & Raízes', text: '10+ anos de história nordestina 🌵' },
            'destination': { tag: 'Delta & Porto', text: 'Casarões e o santuário dos Guarás 🏝️' },
            'footer': { tag: 'Comunidade', text: 'Pessoas > Tecnologia ❤️' }
        };

        const updateFlightProgress = () => {
            const scrollY = window.scrollY || window.pageYOffset;
            const docHeight = document.documentElement.scrollHeight - window.innerHeight;
            const progress = docHeight > 0 ? Math.min(Math.max(scrollY / docHeight, 0), 1) : 0;
            const percentage = progress * 100;

            // 1. Atualiza a barra de voo na navbar
            if (streamLine && streamPilot) {
                streamLine.style.width = `${percentage}%`;
                // Deixa 2% de margem no início e no fim para o ícone não sumir
                const pilotPos = Math.min(Math.max(percentage, 1), 99);
                streamPilot.style.left = `${pilotPos}%`;

                // Durante o scroll ativo, as asas batem. Ao parar, entra em planeio (glide)
                streamPilot.classList.remove('is-gliding');
                clearTimeout(isScrollingTimeout);
                isScrollingTimeout = setTimeout(() => {
                    streamPilot.classList.add('is-gliding');
                }, 180);
            }

            // 2. Controla a visibilidade do Guardião Flutuante (Companion)
            if (navCompanion) {
                if (scrollY > 280) {
                    navCompanion.classList.add('companion-active');
                } else {
                    navCompanion.classList.remove('companion-active');
                }
            }

            ticking = false;
        };

        window.addEventListener('scroll', () => {
            if (!ticking) {
                window.requestAnimationFrame(updateFlightProgress);
                ticking = true;
            }
        }, { passive: true });

        updateFlightProgress();

        // 3. Rastreamento inteligente da seção atual com IntersectionObserver
        const sectionsToTrack = document.querySelectorAll('section[id], footer[id]');
        if ('IntersectionObserver' in window && sectionsToTrack.length > 0) {
            const observer = new IntersectionObserver((entries) => {
                entries.forEach((entry) => {
                    if (entry.isIntersecting) {
                        const id = entry.target.id;
                        const info = sectionStories[id];
                        if (info && companionTag && companionText) {
                            companionTag.textContent = info.tag;
                            companionText.textContent = info.text;
                        }
                    }
                });
            }, {
                rootMargin: '-30% 0px -40% 0px',
                threshold: 0.1
            });

            sectionsToTrack.forEach((sec) => observer.observe(sec));
        }

        // 4. Interação ao clicar no Guará Piloto da Navbar
        if (streamPilot) {
            streamPilot.addEventListener('click', (e) => {
                e.stopPropagation();
                // Pequena pirueta no ar
                streamPilot.style.transform = 'translate(-50%, -10px) rotate(-360deg) scale(1.3)';
                setTimeout(() => {
                    streamPilot.style.transform = '';
                }, 600);
            });
        }

        // 5. Interação com o botão flutuante Voltar ao Topo
        if (btnGuaraTop && navCompanion) {
            btnGuaraTop.addEventListener('click', (e) => {
                e.preventDefault();
                btnGuaraTop.classList.add('companion-soaring');

                window.scrollTo({
                    top: 0,
                    behavior: 'smooth'
                });

                setTimeout(() => {
                    btnGuaraTop.classList.remove('companion-soaring');
                }, 1300);
            });
        }
    });
})();

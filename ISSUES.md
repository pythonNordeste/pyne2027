# 📌 Quadro de Issues & Roadmap — Python Nordeste 2027

Quadro oficial de acompanhamento do desenvolvimento do site da **Python Nordeste 2027 (Parnaíba/PI)**.

---

## 🟢 Concluído (Done)

- [x] **#01 — Setup do Ambiente & Ferramentas**
  - Configuração do projeto com Python 3.14 + `uv` + Hatchling.
  - Estrutura de dependências de desenvolvimento (`ruff`, `pytest`, `livereload`).
- [x] **#02 — Servidor Local com LiveReload**
  - Implementação do comando `uv run main start` com abertura automática de navegador e recarregamento em tempo real.
  - Contribuição e correção de resiliência no repositório fork do `python-livereload`.
- [x] **#03 — Modularização Dinâmica (YAML + Jinja2)**
  - Criação do [variables.yaml](variables.yaml) para controle completo de textos, datas, local e links sem alterar código.
- [x] **#04 — Identidade Visual Oficial PyNE 2027**
  - Extração do brasão do mapa do Piauí/Nordeste (`static/img/pyne_emblem.png`).
  - Vetorização do fundo de curvas de nível (`static/img/contour_lines.svg`).
  - Aplicação da paleta *Rosa Dunas* (`#E47A9F`), *Rosa Destaque* (`#D4638A`), *Areia/Off-white* (`#F9F4E8`) e *Café Escuro* (`#2B1B22`).
- [x] **#05 — Padronização de Ícones com Font Awesome 6**
  - Integração do CDN do Font Awesome 6 e substituição de emojis soltos por ícones semânticos (`<i class="fa-solid ..."></i>`, `<i class="fa-brands ..."></i>`).
- [x] **#06 — Link do Repositório GitHub no Rodapé**
  - Adicionado botão estilo badge no rodapé e pílula no Hero com link direto para o repositório da comunidade.
- [x] **#07 — Animações Visuais Modernas (GPU-Accelerated)**
  - Efeito *Dunas Vivas* com deslocamento orgânico do fundo topográfico.
  - Flutuação suave do brasão oficial (`floatEmblem`).
  - Interação 3D tilt no emblema ao mover o cursor (`static/js/hero_animations.js`).
  - Entrada escalonada dos elementos (*Staggered Reveal*).
  - Pulso no pin de localização e brilho reflexivo no número "2027".
  - Carrossel infinito cinematográfico com máscara de gradiente nas fotos de Parnaíba.
- [x] **#08 — Favicon com Fundo e Alto Contraste**
  - Geração do favicon em formato squircle com fundo sólido Rosa Dunas, além de `static/img/apple-touch-icon.png` e `favicon.ico`.
- [x] **#09 — Copywriting Comunitário ("Pessoas > Tecnologia")**
  - Ajuste da mensagem principal com o lema histórico da comunidade Python.
- [x] **#10 — Esteira de CI/CD (GitHub Actions)**
  - Criação do workflow `.github/workflows/ci-dev.yml` para validação de PRs e deploy de staging no GitHub Pages.
  - Criação do workflow `.github/workflows/ci-main.yml` para produção.
  - Suíte de testes automatizados em `tests/test_site.py`.
- [x] **#11 — Blindagem de Staging contra Motores de Busca**
  - Injeção automática de `<meta name="robots" content="noindex, nofollow">`.
  - Geração automática de `dist/robots.txt` com `Disallow: /`.
  - Desativação do Google Analytics em ambiente de staging.
  - Criação de `dist/.nojekyll` para compatibilidade com o GitHub Pages.

---

## 🟡 Próximas Prioridades (To Do / In Progress)

- [ ] **#12 — Barra de Navegação (Navbar Fixa e Responsiva)**
  - Adicionar menu superior com logotipo, links com rolagem suave para as seções (*Início*, *Sobre*, *Destino*, *CDC*) e ícones sociais.
  - Menu hambúrguer / gaveta mobile para celulares.
- [ ] **#13 — Seção "Sobre a Python Nordeste"**
  - Criar bloco de conteúdo destacando a história itinerante de mais de 10 anos do evento, o acolhimento da comunidade e a chegada inédita a Parnaíba/PI.
- [ ] **#14 — Página Dedicada do Código de Conduta (`/cdc.html`)**
  - Implementar template `pages/cdc.j2` com o texto integral e acessível do Código de Conduta da APyB para navegação interna rápida.
- [ ] **#15 — Easter Egg no DevTools Console**
  - Injetar no console do navegador a mensagem comunitária estilizada da edição 2027 com as bandeiras da diversidade e o lema *Pessoas > Tecnologia*.
- [ ] **#16 — Expansão do Rodapé em 3 Colunas**
  - Estruturar o footer com: (1) Links rápidos de navegação, (2) Créditos comunitários (GruPy/comunidade local e designers), (3) Contato oficial.

---

## 📋 Backlog de Fases Futuras (Roadmap do Evento)

- [ ] **#17 — Módulo de Voluntárias(os) & Organização**
  - Suporte modular no `variables.yaml` para cadastrar membros da equipe com foto, nome, bio e links sociais, renderizados em grid dinâmico.
- [ ] **#18 — Seção de Captação de Patrocínio & Media Kit**
  - Bloco para empresas com botões de download do Media Kit (pt-br / en) ativável condicionalmente conforme a fase de captação.
- [ ] **#19 — Grade de Patrocinadoras por Cotas**
  - Estrutura pronta para exibir marcas apoiadoras organizadas por cotas (*Diamante, Ouro, Prata, Bronze, Apoio*).
- [ ] **#20 — Seção do Local do Evento (Venue & Mapa)**
  - Bloco com informações sobre o centro de convenções/universidade em Parnaíba, dicas de hospedagem e mapa interativo integrado.
- [ ] **#21 — Página de Palestrantes e Agenda (`/speakers.html`)**
  - Grid de palestrantes confirmados, keynotes e grade de horários integrada ao Pretalx ou lista estática.
- [ ] **#22 — Modal de Boas-Vindas Comunitário**
  - Popup acolhedor na primeira visita (com persistência em `localStorage`) destacando o Código de Conduta e as novidades.
- [ ] **#23 — Auditoria de Acessibilidade (a11y) & SEO Final**
  - Verificação de contraste de cores nos níveis WCAG AA/AAA, tags ARIA e pontuação 100 no Lighthouse.

# 📌 Quadro de Issues & Roadmap — Python Nordeste 2027

Quadro oficial de acompanhamento do desenvolvimento do site da **Python Nordeste 2027 (Parnaíba/PI)**.

---

## 🏷️ Taxonomia de Labels Oficiais

Para organizar as contribuições da comunidade no GitHub, utilizamos a seguinte convenção de etiquetas:

| Categoria | Label | Cor | Descrição |
| :--- | :--- | :--- | :--- |
| **Tipo** | `type: feat` | `#0E8A16` | Nova funcionalidade ou componente visual |
| | `type: enhancement` | `#1D76DB` | Melhoria em funcionalidade existente |
| | `type: bug` | `#D93F0B` | Correção de comportamento inesperado ou erro |
| | `type: docs` | `#0075CA` | Atualização de textos, README ou documentação |
| | `type: chore` | `#7057FF` | Tarefas técnicas, CI/CD ou dependências |
| | `type: a11y` | `#FBCA04` | Acessibilidade (WCAG, leitores de tela, contraste) |
| **Escopo** | `scope: ui/ux` | `#BFDADC` | Interface, CSS, animações e responsividade |
| | `scope: content` | `#D4C5F9` | Textos, copies e informações do evento |
| | `scope: community` | `#F9D0C4` | Código de conduta, voluntários e inclusão |
| | `scope: sponsor` | `#FEF2C0` | Patrocínio, cotas e media kit |
| | `scope: schedule` | `#C2E0C6` | Programação, palestras e palestrantes |
| **Onboarding** | `good first issue` | `#7057FF` | Ideal para pessoas iniciando no código aberto |
| | `help wanted` | `#008672` | Tarefa aberta aguardando contribuição |

---

## 🟢 Entregas Realizadas (Done)

- [x] **Setup do Ambiente & Ferramentas**
  - Configuração do projeto com Python 3.14 + `uv` + Hatchling.
  - Estrutura de dependências de desenvolvimento (`ruff`, `pytest`, `livereload`).
- [x] **Servidor Local com LiveReload**
  - Implementação do comando `uv run main start` com abertura automática de navegador e recarregamento em tempo real.
  - Contribuição e correção de resiliência no repositório fork do `python-livereload`.
- [x] **Modularização Dinâmica (YAML + Jinja2)**
  - Criação do [variables.yaml](variables.yaml) para controle completo de textos, datas, local e links sem alterar código.
- [x] **Identidade Visual Oficial PyNE 2027**
  - Extração do brasão do mapa do Piauí/Nordeste (`static/img/pyne_emblem.png`).
  - Vetorização do fundo de curvas de nível (`static/img/contour_lines.svg`).
  - Aplicação da paleta *Rosa Dunas* (`#E47A9F`), *Rosa Destaque* (`#D4638A`), *Areia/Off-white* (`#F9F4E8`) e *Café Escuro* (`#2B1B22`).
- [x] **Padronização de Ícones com Font Awesome 6**
  - Integração do CDN do Font Awesome 6 e substituição de emojis soltos por ícones semânticos (`<i class="fa-solid ..."></i>`, `<i class="fa-brands ..."></i>`).
- [x] **Link do Repositório GitHub no Rodapé**
  - Adicionado botão estilo badge no rodapé e pílula no Hero com link direto para o repositório da comunidade.
- [x] **Animações Visuais Modernas (GPU-Accelerated)**
  - Efeito *Dunas Vivas* com deslocamento orgânico do fundo topográfico.
  - Flutuação suave do brasão oficial (`floatEmblem`).
  - Interação 3D tilt no emblema ao mover o cursor (`static/js/hero_animations.js`).
  - Entrada escalonada dos elementos (*Staggered Reveal*).
  - Pulso no pin de localização e brilho reflexivo no número "2027".
  - Carrossel infinito cinematográfico com máscara de gradiente nas fotos de Parnaíba.
- [x] **Favicon com Fundo e Alto Contraste**
  - Geração do favicon em formato squircle com fundo sólido Rosa Dunas, além de `static/img/apple-touch-icon.png` e `favicon.ico`.
- [x] **Copywriting Comunitário ("Pessoas > Tecnologia")**
  - Ajuste da mensagem principal com o lema histórico da comunidade Python.
- [x] **Esteira de CI/CD (GitHub Actions)**
  - Criação do workflow `.github/workflows/ci-dev.yml` para validação de PRs e deploy de staging no GitHub Pages.
  - Criação do workflow `.github/workflows/ci-main.yml` para produção.
  - Suíte de testes automatizados em `tests/test_site.py`.
- [x] **Blindagem de Staging contra Motores de Busca**
  - Injeção automática de `<meta name="robots" content="noindex, nofollow">`.
  - Geração automática de `dist/robots.txt` com `Disallow: /`.
  - Desativação do Google Analytics em ambiente de staging.
  - Criação de `dist/.nojekyll` para compatibilidade com o GitHub Pages.

---

## 🟡 Próximas Prioridades (To Do / In Progress)

### #01 — Barra de Navegação (Navbar Fixa e Responsiva)
- **Tipo:** `type: feat`
- **Labels:** `scope: ui/ux`, `good first issue`
- **Milestone:** `v0.2.0 - Navegação & Identidade`
- **Esforço:** `Médio`
- **Descrição:** Adicionar barra de navegação no topo com logo, links de rolagem suave para as seções da página (*Início*, *Sobre*, *Destino*, *CDC*) e atalhos para as redes sociais.
- **Critérios de Aceite:**
  - [ ] Navbar fixa no topo com efeito vidro/blur translúcido ao rolar a página.
  - [ ] Links âncora funcionando com rolagem suave (`scroll-behavior: smooth`).
  - [ ] Ícones sociais do GitHub, Instagram, LinkedIn e YouTube à direita.
  - [ ] Menu hambúrguer responsivo para celulares (< 768px).

---

### #02 — Seção "Sobre a Python Nordeste"
- **Tipo:** `type: feat`
- **Labels:** `scope: content`, `good first issue`
- **Milestone:** `v0.2.0 - Navegação & Identidade`
- **Esforço:** `Pequeno`
- **Descrição:** Criar um bloco institucional contextualizando a história itinerante de mais de 10 anos do evento, o compromisso com diversidade e inclusão, e a celebração da chegada inédita ao litoral do Piauí.
- **Critérios de Aceite:**
  - [ ] Texto e títulos configuráveis via `variables.yaml`.
  - [ ] Layout harmonizado com a paleta oficial (fundo Areia/Off-white e tipografia *Outfit*).
  - [ ] Destaques em números ou marcos da comunidade (anos de história, edições passadas).

---

### #03 — Página Dedicada do Código de Conduta (`/cdc.html`)
- **Tipo:** `type: feat`
- **Labels:** `scope: community`, `type: docs`, `good first issue`
- **Milestone:** `v0.2.0 - Navegação & Identidade`
- **Esforço:** `Pequeno`
- **Descrição:** Implementar uma página dedicada (`pages/cdc.j2`) com o texto completo do Código de Conduta da APyB e canais de contato da comissão de resposta a incidentes.
- **Critérios de Aceite:**
  - [ ] Página acessível diretamente pela rota `/cdc.html`.
  - [ ] Texto integral com formatação limpa e legível.
  - [ ] Informações claras sobre como reportar incidentes de forma segura.

---

### #04 — Easter Egg no DevTools Console
- **Tipo:** `type: chore`
- **Labels:** `scope: community`, `good first issue`
- **Milestone:** `v0.2.0 - Navegação & Identidade`
- **Esforço:** `Pequeno`
- **Descrição:** Injetar no console do navegador uma mensagem acolhedora com arte em texto da edição 2027, bandeiras da diversidade e o lema comunitário *Pessoas > Tecnologia*.
- **Critérios de Aceite:**
  - [ ] Mensagem estilizável com CSS no `console.log`.
  - [ ] Execução leve no carregamento da página sem impactar performance.

---

### #05 — Rodapé Modular e Configurável (Multi-colunas)
- **Tipo:** `type: enhancement`
- **Labels:** `scope: ui/ux`, `type: feat`
- **Milestone:** `v0.2.0 - Navegação & Identidade`
- **Esforço:** `Médio`
- **Descrição:** Estruturar o rodapé de forma totalmente genérica e parametrizável via `variables.yaml`, suportando colunas opcionais (links rápidos, créditos de realização e canais de contato).
- **Critérios de Aceite:**
  - [ ] Colunas opcionais: se uma seção não estiver preenchida no YAML, ela não é renderizada.
  - [ ] Preservação do link oficial do repositório no GitHub com ícone Font Awesome.
  - [ ] Layout responsivo em colunas no desktop e empilhado no celular.

---

## 📋 Backlog de Fases Futuras (Roadmap do Evento)

### #06 — Módulo de Voluntárias(os) & Organização
- **Tipo:** `type: feat`
- **Labels:** `scope: community`, `type: enhancement`
- **Milestone:** `v0.3.0 - Envolvimento Comunitário`
- **Esforço:** `Médio`
- **Descrição:** Suporte modular no `variables.yaml` para listar voluntárias e voluntários da organização com foto, nome, bio e links sociais, renderizados em grid dinâmico.

---

### #07 — Seção de Captação de Patrocínio & Media Kit
- **Tipo:** `type: feat`
- **Labels:** `scope: sponsor`, `type: feat`
- **Milestone:** `v0.4.0 - Captação de Recursos`
- **Esforço:** `Médio`
- **Descrição:** Bloco de chamada para empresas parceiras com botões de download do Media Kit (pt-br / en) ativável condicionalmente conforme a fase de captação.

---

### #08 — Grade de Patrocinadoras por Cotas
- **Tipo:** `type: feat`
- **Labels:** `scope: sponsor`, `type: feat`
- **Milestone:** `v0.4.0 - Captação de Recursos`
- **Esforço:** `Médio`
- **Descrição:** Estrutura pronta para exibir marcas apoiadoras organizadas por cotas (*Diamante, Ouro, Prata, Bronze, Apoio*), ativadas dinamicamente via YAML.

---

### #09 — Seção do Local do Evento (Venue & Informações de Parnaíba)
- **Tipo:** `type: feat`
- **Labels:** `scope: content`, `scope: ui/ux`
- **Milestone:** `v0.5.0 - Experiência do Participante`
- **Esforço:** `Médio`
- **Descrição:** Bloco com detalhes do espaço em Parnaíba, dicas de deslocamento, hospedagem na região e mapa interativo integrado.

---

### #10 — Página de Palestrantes e Agenda (`/speakers.html`)
- **Tipo:** `type: feat`
- **Labels:** `scope: schedule`, `type: feat`
- **Milestone:** `v0.6.0 - Grade de Programação`
- **Esforço:** `Grande`
- **Descrição:** Grid de palestrantes confirmados, keynotes e grade de horários integrada ao Pretalx ou lista estática.

---

### #11 — Modal de Boas-Vindas Comunitário
- **Tipo:** `type: feat`
- **Labels:** `scope: community`, `scope: ui/ux`
- **Milestone:** `v0.5.0 - Experiência do Participante`
- **Esforço:** `Pequeno`
- **Descrição:** Popup acolhedor na primeira visita (com persistência em `localStorage`) destacando o Código de Conduta e avisos importantes.

---

### #12 — Auditoria de Acessibilidade (a11y) & SEO Final
- **Tipo:** `type: a11y`
- **Labels:** `type: a11y`, `scope: ui/ux`
- **Milestone:** `v1.0.0 - Release Oficial`
- **Esforço:** `Médio`
- **Descrição:** Verificação de contraste de cores nos níveis WCAG AA/AAA, tags ARIA semânticas, navegação por teclado e pontuação 100 no Lighthouse.

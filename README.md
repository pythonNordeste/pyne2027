# Python Nordeste 2027

Site oficial da **Python Nordeste 2027** que acontecerá em Parnaíba, Piauí.

---

## 🚀 Pré-requisitos

O projeto utiliza o **[uv](https://docs.astral.sh/uv/)** para gerenciamento de dependências e ambiente Python:

- Instale o `uv` (se ainda não tiver):
  ```bash
  # Linux/macOS
  curl -LsSf https://astral.sh/uv/install.sh | sh

  # Windows (PowerShell)
  powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
  ```

---

## 🛠️ Como rodar o projeto localmente

1. **Clone o repositório e acesse a pasta:**
   ```bash
   git clone https://github.com/pythonnordeste/pyne2027.git
   cd pyne2027
   ```

2. **Instale as dependências:**
   ```bash
   uv sync --extra dev
   ```

3. **Inicie o servidor local:**
   ```bash
   uv run main start
   ```

4. **Acesse no navegador:**
   Abra [http://localhost:8000](http://localhost:8000).

---

## 📁 Onde editar o conteúdo

- **`variables.yaml`**: Textos, links e informações gerais do evento.
- **`pages/`**: Páginas do site em formato Jinja2 (`.j2`).
- **`templates/`**: Estrutura e layout base compartilhado (`base.j2`).
- **`static/`**: Arquivos estáticos (CSS, JavaScript e imagens).
- **`dist/`**: Pasta gerada automaticamente com o site compilado (não versione esta pasta).

---

## 💻 Comandos úteis

| Comando | Descrição |
| --- | --- |
| `uv run main start` | Compila o site e inicia o servidor local em `http://localhost:8000` |
| `uv run main render` | Apenas compila as páginas e estáticos para a pasta `dist/` |
| `uv run pytest` | Executa os testes automatizados de integridade do site |
| `uv run ruff check` | Analisa e valida a qualidade do código Python |
| `uv run ruff format` | Formata o código Python automaticamente |

---

## 🤝 Como contribuir

Damos as boas-vindas a todas as pessoas! Se esta é a sua primeira experiência no mundo do código aberto ou na comunidade, sua participação é muito importante. Não é necessário ter experiência avançada para contribuir.

### 💡 Por onde começar?
- **Não precisa ser código complexo**:
  - Correção de textos, erros de digitação ou links em `variables.yaml` e `pages/`.
  - Melhorias de design, espaçamentos ou responsividade para celular em `static/css/`.
  - Sugestões de melhoria no próprio `README.md`.
- **Encontre uma tarefa**: Acesse a aba **[Issues](https://github.com/pythonnordeste/pyne2027/issues)** e procure por tarefas com a etiqueta `good first issue` (ótima para quem está começando).
- **Tem uma ideia ou achou um problema?**: Abra uma nova Issue descrevendo o que você encontrou ou gostaria de ver no site.
- **Travou ou tem dúvidas?**: Pergunte na própria Issue. Estamos aqui para ajudar você a fazer sua contribuição!

### 📋 Passo a passo técnico

1. **Crie uma branch** para sua alteração a partir da branch `dev`:
   ```bash
   git checkout dev
   git pull origin dev
   git checkout -b minha-contribuicao
   ```

2. **Faça suas alterações** e visualize localmente com `uv run main start`.

3. **Valide a formatação e os testes locais:**
   ```bash
   uv run ruff check
   uv run pytest
   ```

4. **Faça o commit e envie sua branch:**
   ```bash
   git add .
   git commit -m "feat: descreva brevemente sua alteração"
   git push origin minha-contribuicao
   ```

5. **Abra um Pull Request (PR)** apontando para a branch `dev`. A CI do GitHub executará as validações automaticamente em seu PR!

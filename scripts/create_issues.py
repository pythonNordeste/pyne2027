#!/usr/bin/env python3
"""
Script de automação para criar Labels e Issues no GitHub.
Pode ser executado localmente (com GITHUB_TOKEN) ou via GitHub Actions (workflow_dispatch).
"""

import json
import os
import shutil
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

REPO = os.environ.get("GITHUB_REPOSITORY", "pythonNordeste/pyne2027")
TOKEN = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")

if not TOKEN and shutil.which("gh"):
    try:
        proc = subprocess.run(
            ["gh", "auth", "token"], capture_output=True, text=True, check=True
        )
        TOKEN = proc.stdout.strip()
    except subprocess.CalledProcessError, FileNotFoundError, OSError:
        TOKEN = None

if not TOKEN:
    print("❌ Erro: GITHUB_TOKEN ou GH_TOKEN não encontrado nas variáveis de ambiente.")
    print("💡 Para executar localmente, defina: export GITHUB_TOKEN='seu_token'")
    print(
        "💡 Ou execute via GitHub Actions na aba 'Actions > Sincronizar Issues e Labels > Run workflow'."
    )
    sys.exit(1)

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/vnd.github+json",
    "User-Agent": "pyne2027-issues-syncer",
    "X-GitHub-Api-Version": "2022-11-28",
}


def api_request(endpoint: str, method: str = "GET", data: dict | None = None):
    url = f"https://api.github.com/{endpoint.lstrip('/')}"
    body = json.dumps(data).encode("utf-8") if data else None
    req = urllib.request.Request(url, data=body, headers=HEADERS, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            content = resp.read().decode("utf-8")
            return json.loads(content) if content else {}
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        return {"error": e.code, "message": error_body}


def sync_labels():
    print(f"📦 Sincronizando labels em {REPO}...")
    labels_file = Path(__file__).parent.parent / ".github" / "labels.json"
    if not labels_file.exists():
        print("⚠️ Arquivo .github/labels.json não encontrado.")
        return

    labels = json.loads(labels_file.read_text(encoding="utf-8"))

    # Buscar labels existentes
    existing = api_request(f"repos/{REPO}/labels?per_page=100")
    if isinstance(existing, dict) and "error" in existing:
        print(f"❌ Erro ao listar labels: {existing.get('message')}")
        if existing.get("error") == 404:
            print(
                "💡 Dica: Erro 404 indica que o token atual não tem acesso ao repositório."
            )
            print(
                "   Se estiver usando gh CLI, reautentique com: gh auth login -w -s repo"
            )
            print(
                "   Ou defina GITHUB_TOKEN com um Personal Access Token (Classic) com escopo 'repo'."
            )
        return

    existing_names = {l["name"].lower(): l["name"] for l in existing}

    for label in labels:
        name = label["name"]
        color = label["color"].lstrip("#")
        desc = label.get("description", "")

        if name.lower() in existing_names:
            real_name = existing_names[name.lower()]
            endpoint = f"repos/{REPO}/labels/{urllib.parse.quote(real_name)}"
            api_request(
                endpoint, method="PATCH", data={"color": color, "description": desc}
            )
            print(f"  🔄 Label atualizada: {name}")
        else:
            endpoint = f"repos/{REPO}/labels"
            api_request(
                endpoint,
                method="POST",
                data={"name": name, "color": color, "description": desc},
            )
            print(f"  ✨ Label criada: {name}")


ISSUES = [
    {
        "title": "feat: barra de navegação superior fixa e responsiva",
        "labels": ["type: feat", "scope: ui/ux", "good first issue"],
        "body": """### 💡 Descrição da Funcionalidade
Implementar barra de navegação no topo com logo, links de rolagem suave para as seções da página (*Início*, *Sobre*, *Destino*, *CDC*) e atalhos para as redes sociais.

### 🎯 Critérios de Aceite
- [ ] Navbar fixa no topo com efeito vidro/blur translúcido ao rolar a página.
- [ ] Links âncora funcionando com rolagem suave (`scroll-behavior: smooth`).
- [ ] Ícones sociais do GitHub, Instagram, LinkedIn e YouTube à direita.
- [ ] Menu hambúrguer responsivo para celulares (< 768px).

### 🏷️ Informações Adicionais
- **Milestone:** v0.2.0 - Navegação & Identidade
- **Esforço estimado:** Médio
""",
    },
    {
        "title": "feat: seção 'Sobre a Python Nordeste' contando história e valores",
        "labels": ["type: feat", "scope: content", "good first issue"],
        "body": """### 💡 Descrição da Funcionalidade
Criar um bloco institucional contextualizando a história itinerante de mais de 10 anos do evento, o compromisso com diversidade e inclusão, e a celebração da chegada inédita ao litoral do Piauí.

### 🎯 Critérios de Aceite
- [ ] Texto e títulos configuráveis via `variables.yaml`.
- [ ] Layout harmonizado com a paleta oficial (fundo Areia/Off-white e tipografia *Outfit*).
- [ ] Destaques em números ou marcos da comunidade (anos de história, edições passadas).

### 🏷️ Informações Adicionais
- **Milestone:** v0.2.0 - Navegação & Identidade
- **Esforço estimado:** Pequeno
""",
    },
    {
        "title": "feat: página dedicada do Código de Conduta (/cdc.html)",
        "labels": ["type: feat", "scope: community", "type: docs", "good first issue"],
        "body": """### 💡 Descrição da Funcionalidade
Implementar uma página dedicada (`pages/cdc.j2`) com o texto completo do Código de Conduta da APyB e canais de contato da comissão de resposta a incidentes.

### 🎯 Critérios de Aceite
- [ ] Página acessível diretamente pela rota `/cdc.html`.
- [ ] Texto integral com formatação limpa e legível.
- [ ] Informações claras sobre como reportar incidentes de forma segura.

### 🏷️ Informações Adicionais
- **Milestone:** v0.2.0 - Navegação & Identidade
- **Esforço estimado:** Pequeno
""",
    },
    {
        "title": "chore: easter egg comunitário no console do DevTools",
        "labels": ["type: chore", "scope: community", "good first issue"],
        "body": """### 💡 Descrição da Funcionalidade
Injetar no console do navegador uma mensagem acolhedora com arte em texto da edição 2027, bandeiras da diversidade e o lema comunitário *Pessoas > Tecnologia*.

### 🎯 Critérios de Aceite
- [ ] Mensagem estilizável com CSS no `console.log`.
- [ ] Execução leve no carregamento da página sem impactar performance.

### 🏷️ Informações Adicionais
- **Milestone:** v0.2.0 - Navegação & Identidade
- **Esforço estimado:** Pequeno
""",
    },
    {
        "title": "feat: rodapé modular e configurável em multi-colunas via variables.yaml",
        "labels": ["type: feat", "type: enhancement", "scope: ui/ux"],
        "body": """### 💡 Descrição da Funcionalidade
Estruturar o rodapé de forma totalmente genérica e parametrizável via `variables.yaml`, suportando colunas opcionais (links rápidos, créditos de realização e canais de contato).

### 🎯 Critérios de Aceite
- [ ] Colunas opcionais: se uma seção não estiver preenchida no YAML, ela não é renderizada.
- [ ] Preservação do link oficial do repositório no GitHub com ícone Font Awesome.
- [ ] Layout responsivo em colunas no desktop e empilhado no celular.

### 🏷️ Informações Adicionais
- **Milestone:** v0.2.0 - Navegação & Identidade
- **Esforço estimado:** Médio
""",
    },
    {
        "title": "feat: módulo de voluntárias(os) e equipe organizadora",
        "labels": ["type: feat", "type: enhancement", "scope: community"],
        "body": """### 💡 Descrição da Funcionalidade
Suporte modular no `variables.yaml` para listar voluntárias e voluntários da organização com foto, nome, bio e links sociais, renderizados em grid dinâmico.

### 🎯 Critérios de Aceite
- [ ] Lista em YAML ou JSON com fallback para fotos padrão.
- [ ] Grid responsivo com cards e links sociais.

### 🏷️ Informações Adicionais
- **Milestone:** v0.3.0 - Envolvimento Comunitário
- **Esforço estimado:** Médio
""",
    },
    {
        "title": "feat: seção de captação de patrocínio com download de Media Kit",
        "labels": ["type: feat", "scope: sponsor"],
        "body": """### 💡 Descrição da Funcionalidade
Bloco de chamada para empresas parceiras com botões de download do Media Kit (pt-br / en) ativável condicionalmente conforme a fase de captação.

### 🎯 Critérios de Aceite
- [ ] Download do Media Kit em PDF condicional.
- [ ] E-mail de contato para propostas e cotas.

### 🏷️ Informações Adicionais
- **Milestone:** v0.4.0 - Captação de Recursos
- **Esforço estimado:** Médio
""",
    },
    {
        "title": "feat: grade de patrocinadoras organizadas por cotas",
        "labels": ["type: feat", "scope: sponsor"],
        "body": """### 💡 Descrição da Funcionalidade
Estrutura pronta para exibir marcas apoiadoras organizadas por cotas (*Diamante, Ouro, Prata, Bronze, Apoio*), ativadas dinamicamente via YAML.

### 🎯 Critérios de Aceite
- [ ] Logos organizadas por nível de patrocínio com links externos.
- [ ] Espaço dedicado para parceiros institucionais e apoios locais.

### 🏷️ Informações Adicionais
- **Milestone:** v0.4.0 - Captação de Recursos
- **Esforço estimado:** Médio
""",
    },
    {
        "title": "feat: seção do local do evento (venue) e mapa interativo",
        "labels": ["type: feat", "scope: content", "scope: ui/ux"],
        "body": """### 💡 Descrição da Funcionalidade
Bloco com detalhes do espaço em Parnaíba, dicas de deslocamento, hospedagem na região e mapa interativo integrado.

### 🎯 Critérios de Aceite
- [ ] Informações de endereço e pontos de referência.
- [ ] Mapa integrado ou link direto para Google Maps / OpenStreetMap.
- [ ] Dicas de transporte e aeroportos próximos (PHB, THE, FOR).

### 🏷️ Informações Adicionais
- **Milestone:** v0.5.0 - Experiência do Participante
- **Esforço estimado:** Médio
""",
    },
    {
        "title": "feat: página de palestrantes e agenda (/speakers.html)",
        "labels": ["type: feat", "scope: schedule"],
        "body": """### 💡 Descrição da Funcionalidade
Grid de palestrantes confirmados, keynotes e grade de horários integrada ao Pretalx ou lista estática.

### 🎯 Critérios de Aceite
- [ ] Página `/speakers.html` ou `/agenda.html`.
- [ ] Visualização por dia e por trilha.
- [ ] Destaque para palestrantes convidadas(os).

### 🏷️ Informações Adicionais
- **Milestone:** v0.6.0 - Grade de Programação
- **Esforço estimado:** Grande
""",
    },
    {
        "title": "feat: modal de boas-vindas comunitário no primeiro acesso",
        "labels": ["type: feat", "scope: community", "scope: ui/ux"],
        "body": """### 💡 Descrição da Funcionalidade
Popup acolhedor na primeira visita (com persistência em `localStorage`) destacando o Código de Conduta e avisos importantes.

### 🎯 Critérios de Aceite
- [ ] Exibição apenas na primeira visita via `localStorage`.
- [ ] Opção fácil de fechar (botão X ou clique fora).
- [ ] Respeito a acessibilidade de teclado (ESC fecha o modal).

### 🏷️ Informações Adicionais
- **Milestone:** v0.5.0 - Experiência do Participante
- **Esforço estimado:** Pequeno
""",
    },
    {
        "title": "a11y: auditoria de acessibilidade, contraste e pontuação 100 no Lighthouse",
        "labels": ["type: a11y", "scope: ui/ux"],
        "body": """### 💡 Descrição da Funcionalidade
Verificação de contraste de cores nos níveis WCAG AA/AAA, tags ARIA semânticas, navegação por teclado e pontuação 100 no Lighthouse.

### 🎯 Critérios de Aceite
- [ ] Contraste verificado para textos e fundos.
- [ ] Navegação 100% acessível por teclado (foco visível).
- [ ] Alt tags descritivas em todas as imagens.
- [ ] Pontuação mínima de 95+ em Acessibilidade e Boas Práticas no Google Lighthouse.

### 🏷️ Informações Adicionais
- **Milestone:** v1.0.0 - Release Oficial
- **Esforço estimado:** Médio
""",
    },
]


def sync_issues():
    print(f"\n📋 Verificando issues existentes em {REPO}...")
    existing = api_request(f"repos/{REPO}/issues?state=all&per_page=100")
    if isinstance(existing, dict) and "error" in existing:
        print(f"❌ Erro ao listar issues: {existing.get('message')}")
        if existing.get("error") == 404:
            print(
                "💡 Dica: Erro 404 indica que o token atual não tem acesso ao repositório."
            )
            print(
                "   Se estiver usando gh CLI, reautentique com: gh auth login -w -s repo"
            )
            print(
                "   Ou defina GITHUB_TOKEN com um Personal Access Token (Classic) com escopo 'repo'."
            )
        return

    existing_titles = {
        i["title"].strip().lower() for i in existing if "pull_request" not in i
    }

    for issue in ISSUES:
        title = issue["title"]
        if title.strip().lower() in existing_titles:
            print(f"  ⏭️ Já existe: {title}")
            continue

        data = {
            "title": title,
            "body": issue["body"],
            "labels": issue["labels"],
        }
        res = api_request(f"repos/{REPO}/issues", method="POST", data=data)
        if isinstance(res, dict) and "error" in res:
            print(f"  ❌ Erro ao criar '{title}': {res.get('message')}")
        else:
            issue_num = res.get("number", "?")
            print(f"  ✅ Criada #{issue_num}: {title}")


if __name__ == "__main__":
    sync_labels()
    sync_issues()
    print("\n🎉 Processo concluído com sucesso!")

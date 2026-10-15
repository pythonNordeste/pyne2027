from pathlib import Path

from main import load_settings, output_folder, render, settings_file


def test_variables_yaml_exists_and_valid():
    assert settings_file.exists(), "O arquivo variables.yaml não foi encontrado."
    settings = load_settings()
    assert isinstance(settings, dict), (
        "variables.yaml deve ser um dicionário YAML válido."
    )
    assert "event" in settings, "A chave 'event' deve existir em variables.yaml."
    assert "theme" in settings, "A chave 'theme' deve existir em variables.yaml."
    assert settings["event"].get("name"), "O evento deve ter um nome definido."
    assert settings["event"].get("edition"), "O evento deve ter uma edição definida."


def test_referenced_theme_assets_exist():
    settings = load_settings()
    theme = settings.get("theme", {})

    for key in ["logo", "logo_horizontal", "favicon", "preview_image"]:
        asset_path = theme.get(key)
        if asset_path:
            assert Path(asset_path).exists(), (
                f"O arquivo de tema '{key}' apontado para '{asset_path}' não existe."
            )


def test_render_generates_dist_and_index_html():
    render()
    assert output_folder.exists(), "A pasta dist/ não foi gerada."
    index_html = output_folder / "index.html"
    assert index_html.exists(), "O arquivo dist/index.html não foi gerado."

    content = index_html.read_text(encoding="utf-8")
    assert "<!DOCTYPE html>" in content
    assert '<footer id="footer">' in content
    assert "fa-brands fa-github" in content
    assert "Pessoas > Tecnologia" in content


def test_staging_environment_blocks_search_engines():
    render()
    robots_file = output_folder / "robots.txt"
    assert robots_file.exists(), "O arquivo dist/robots.txt deve ser gerado."
    assert "Disallow: /" in robots_file.read_text(), (
        "Em staging, o robots.txt deve bloquear todos os robôs de busca."
    )

    index_html = (output_folder / "index.html").read_text(encoding="utf-8")
    assert 'content="noindex, nofollow' in index_html, (
        "Em staging, a meta tag robots deve ser 'noindex, nofollow'."
    )
    assert 'name="googlebot" content="noindex, nofollow' in index_html, (
        "Em staging, a meta tag googlebot deve ser 'noindex, nofollow'."
    )
    assert "googletagmanager.com/gtag/js" not in index_html, (
        "Em staging, o Google Analytics não deve ser injetado."
    )
    assert (output_folder / "favicon.ico").exists(), (
        "O arquivo dist/favicon.ico deve ser copiado."
    )
    assert (output_folder / ".nojekyll").exists(), (
        "O arquivo dist/.nojekyll deve ser gerado para o GitHub Pages."
    )


def test_navbar_rendered_and_responsive():
    render()
    index_html = (output_folder / "index.html").read_text(encoding="utf-8")
    assert '<nav class="navbar" id="navbar"' in index_html, (
        "A navbar deve existir no DOM."
    )
    assert 'id="navbar-toggle"' in index_html, (
        "O botão de menu hambúrguer deve existir."
    )
    assert 'href="index.html#about"' in index_html, (
        "Link para a seção Sobre deve estar na navbar."
    )
    assert 'href="cdc.html"' in index_html, (
        "Link para o Código de Conduta deve estar na navbar."
    )
    assert "static/js/navbar.js" in index_html, "O script navbar.js deve ser importado."


def test_about_section_rendered():
    render()
    index_html = (output_folder / "index.html").read_text(encoding="utf-8")
    assert '<section id="about"' in index_html, "A seção #about deve ser renderizada."
    assert "Sobre a Python Nordeste" in index_html, (
        "O título da seção Sobre deve estar presente."
    )
    assert "Anos de História" in index_html, (
        "Card de estatística de anos de história deve existir."
    )
    assert "Estados Nordestinos" in index_html, (
        "Card de estados nordestinos deve existir."
    )


def test_cdc_page_rendered():
    render()
    cdc_html = output_folder / "cdc.html"
    assert cdc_html.exists(), "A página dist/cdc.html deve ser gerada automaticamente."
    content = cdc_html.read_text(encoding="utf-8")
    assert "Código de Conduta" in content, (
        "Título do Código de Conduta deve estar presente."
    )
    assert "conduta@pythonnordeste.org" in content, (
        "E-mail de denúncia do CDC deve estar presente."
    )
    assert "Voltar à Página Inicial" in content, (
        "Link de retorno para a página inicial deve existir."
    )
    assert '<nav class="navbar" id="navbar"' in content, (
        "A navbar deve estar presente na página do CDC."
    )


def test_artwork_assets_exist():
    expected_assets = [
        "static/img/brand/logo.svg",
        "static/img/brand/monograma.svg",
        "static/img/brand/nordeste.svg",
        "static/img/brand/pattern_contour.svg",
        "static/img/casinhas/casinha_amarela.svg",
        "static/img/casinhas/casinha_azul.svg",
        "static/img/casinhas/casinha_coral.svg",
        "static/img/guara/guara.png",
        "static/img/guara/guara_up.png",
        "static/img/guara/guara_down.png",
        "static/js/guara_animation.js",
    ]
    for asset in expected_assets:
        assert Path(asset).exists(), f"Arquivo de arte visual não encontrado: {asset}"


def test_destination_and_casinhas_rendered():
    render()
    index_html = (output_folder / "index.html").read_text(encoding="utf-8")
    assert '<section id="destination"' in index_html, "Seção #destination deve existir."
    assert "casinhas-stage-card" in index_html, (
        "Card das casinhas deve ser renderizado."
    )
    assert "Porto das Barcas" in index_html, "Porto das Barcas deve ser mencionado."
    assert "casinha_amarela.svg" in index_html, "Casinha amarela deve estar no DOM."
    assert "casinha_azul.svg" in index_html, "Casinha azul deve estar no DOM."
    assert "casinha_coral.svg" in index_html, "Casinha coral deve estar no DOM."
    assert "guara.png" in index_html, "Guará deve estar no DOM."


def test_guara_animation_and_revoada_rendered():
    render()
    index_html = (output_folder / "index.html").read_text(encoding="utf-8")
    assert "hero-guara-flock" in index_html, (
        "Bando de guarás no Hero deve estar no DOM."
    )
    assert "interactive-guara" in index_html, (
        "Mascote interativo do Guará deve estar presente."
    )
    assert "guara_up.png" in index_html, (
        "Frame de asa para cima do Guará deve estar no DOM."
    )
    assert "guara_down.png" in index_html, (
        "Frame de asa para baixo do Guará deve estar no DOM."
    )
    assert "revoada-canvas-container" in index_html, (
        "Container da Revoada deve estar no DOM."
    )
    assert "revoada-toast" in index_html, "Toast da Revoada deve estar no DOM."
    assert "static/js/guara_animation.js" in index_html, (
        "Script guara_animation.js deve ser importado."
    )


def test_hero_identity_rendered():
    render()
    index_html = (output_folder / "index.html").read_text(encoding="utf-8")
    assert "hero-contour-right" in index_html, (
        "Elemento hero-contour-right deve estar presente no Hero."
    )
    assert "hero_contour_right.svg" in index_html, (
        "Curvas topográficas oficiais hero_contour_right.svg devem ser importadas no Hero."
    )
    assert "hero-logo-horizontal" in index_html, (
        "Logo horizontal oficial deve estar no Hero."
    )
    assert "static/img/brand/logo.svg" in index_html, (
        "Arquivo logo.svg deve estar no src do hero-logo."
    )


def test_guara_navigation_companion_rendered():
    render()
    index_html = (output_folder / "index.html").read_text(encoding="utf-8")
    assert "nav-guara-stream" in index_html, (
        "Linha de navegação com o Guará deve estar na navbar."
    )
    assert "stream-guara-pilot" in index_html, (
        "Guará piloto na navbar deve estar presente no DOM."
    )
    assert "guara-nav-companion" in index_html, (
        "Guará companheiro de navegação flutuante deve estar no DOM."
    )
    assert "btn-guara-top" in index_html, (
        "Botão de voar ao topo do Guará deve estar presente."
    )

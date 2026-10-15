from pathlib import Path

import pytest

import main
from main import (
    load_destination_slides,
    load_settings,
    output_folder,
    render,
    settings_file,
)


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
        if asset_path and not asset_path.startswith("http"):
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


@pytest.fixture
def render_with(monkeypatch):
    """Renderiza o site sobrescrevendo chaves do variables.yaml, sem alterar o arquivo."""

    def _render(**overrides):
        settings = {**load_settings(), **overrides}
        monkeypatch.setattr(main, "load_settings", lambda: settings)
        render()
        return settings

    yield _render
    monkeypatch.undo()
    render()


def test_render_generates_github_pages_files():
    render()
    assert (output_folder / "robots.txt").exists(), (
        "O arquivo dist/robots.txt deve ser gerado."
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


@pytest.mark.skip(
    reason="Seção de casinhas do Porto das Barcas comentada no template para manter o Destino da main"
)
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


@pytest.mark.parametrize(
    "overrides",
    [
        {"environment": "staging", "allow_indexing": True},
        {"environment": "production", "allow_indexing": False},
    ],
    ids=["staging", "production-sem-indexacao"],
)
def test_indexing_disabled_blocks_search_engines(render_with, overrides):
    render_with(**overrides)

    assert "Disallow: /" in (output_folder / "robots.txt").read_text(), (
        "Sem indexação, o robots.txt deve bloquear todos os robôs de busca."
    )
    assert not (output_folder / "sitemap.xml").exists(), (
        "Sem indexação, o sitemap.xml não deve ser gerado."
    )

    index_html = (output_folder / "index.html").read_text(encoding="utf-8")
    assert 'name="robots" content="noindex, nofollow' in index_html, (
        "Sem indexação, a meta tag robots deve ser 'noindex, nofollow'."
    )
    assert 'name="googlebot" content="noindex, nofollow' in index_html, (
        "Sem indexação, a meta tag googlebot deve ser 'noindex, nofollow'."
    )
    assert 'rel="canonical"' not in index_html
    assert "googletagmanager.com/gtag/js" not in index_html, (
        "Sem indexação, o Google Analytics não deve ser injetado."
    )


def test_production_allows_search_engines(render_with):
    settings = render_with(environment="production", allow_indexing=True)
    site_url = settings["event"]["url"].rstrip("/")

    robots = (output_folder / "robots.txt").read_text()
    assert "Disallow: /" not in robots, (
        "Em produção, o robots.txt não deve bloquear os robôs de busca."
    )
    assert "Allow: /" in robots
    assert f"Sitemap: {site_url}/sitemap.xml" in robots

    sitemap = output_folder / "sitemap.xml"
    assert sitemap.exists(), "Em produção, o dist/sitemap.xml deve ser gerado."
    assert f"<loc>{site_url}/</loc>" in sitemap.read_text()

    index_html = (output_folder / "index.html").read_text(encoding="utf-8")
    assert 'name="robots" content="index, follow"' in index_html
    assert 'name="googlebot" content="index, follow' in index_html
    assert f'rel="canonical" href="{site_url}/"' in index_html
    if settings.get("google_tag"):
        assert f"gtag/js?id={settings['google_tag']}" in index_html, (
            "Em produção, o Google Analytics deve ser injetado."
        )


def test_social_preview_uses_absolute_image_url():
    settings = load_settings()
    render()
    site_url = settings["event"]["url"].rstrip("/")
    preview_image = settings["theme"]["preview_image"]
    expected = (
        preview_image
        if preview_image.startswith("http")
        else f"{site_url}/{preview_image.lstrip('/')}"
    )

    index_html = (output_folder / "index.html").read_text(encoding="utf-8")
    assert f'property="og:image" content="{expected}"' in index_html, (
        "A og:image deve ser uma URL absoluta para os previews em redes sociais."
    )
    assert f'name="twitter:image" content="{expected}"' in index_html
    assert 'property="og:title"' in index_html
    assert 'name="twitter:card" content="summary_large_image"' in index_html


def test_meta_description_used_in_search_and_social_tags():
    settings = load_settings()
    meta_description = settings["event"].get("meta_description")
    if not meta_description:
        pytest.skip("event.meta_description não definido em variables.yaml.")

    assert len(meta_description) <= 160, (
        "event.meta_description deve ter até 160 caracteres para não ser cortada no Google."
    )

    render()
    index_html = (output_folder / "index.html").read_text(encoding="utf-8")
    for tag in (
        f'name="description" content="{meta_description}"',
        f'property="og:description" content="{meta_description}"',
        f'name="twitter:description" content="{meta_description}"',
    ):
        assert tag in index_html, f"Meta tag ausente ou divergente: {tag}"


def test_event_date_and_venue_rendered_in_hero():
    settings = load_settings()
    event = settings["event"]
    location = event["location"]
    render()
    index_html = (output_folder / "index.html").read_text(encoding="utf-8")

    assert (
        f'<time datetime="{event["start_date"]}/{event["end_date"]}">{event["date"]}</time>'
        in index_html
    )
    assert (
        f"{location['venue']}, em {location['city']}, {location['state_code']}"
        in index_html
    )


def test_destination_slides_reference_existing_photos():
    settings = load_settings()
    slides = load_destination_slides(settings)
    assert slides, "destination.highlights deve ter ao menos uma atração."

    for slide in slides:
        assert slide.get("title") and slide.get("description") and slide.get("alt")
        assert slide["image"].endswith(".jpg")
        assert Path(slide["image"]).exists()


def test_destination_carousel_rendered_with_captions():
    slides = load_destination_slides(load_settings())
    render()
    index_html = (output_folder / "index.html").read_text(encoding="utf-8")

    assert index_html.count('class="carousel-slide"') == len(slides)
    assert index_html.count("data-carousel-dot=") == len(slides)
    for slide in slides:
        assert f'<h3 class="slide-title">{slide["title"]}</h3>' in index_html
        assert f'<img src="{slide["image"]}"' in index_html


def test_destination_slide_with_unknown_photo_fails():
    settings = {"destination": {"highlights": [{"photo": "99", "title": "X"}]}}
    with pytest.raises(ValueError, match="99"):
        load_destination_slides(settings)


def test_venue_section_with_map_and_photo_placeholder(render_with):
    settings = load_settings()
    location = {**settings["event"]["location"], "photo": ""}
    render_with(event={**settings["event"], "location": location})
    index_html = (output_folder / "index.html").read_text(encoding="utf-8")

    assert '<section id="venue"' in index_html
    assert "maps.google.com/maps?q=" in index_html
    assert "output=embed" in index_html
    assert "Foto do local em breve" in index_html


def test_venue_section_shows_photo_when_configured(render_with):
    settings = load_settings()
    photo = settings["theme"]["logo"]
    location = {**settings["event"]["location"], "photo": photo, "photo_alt": "Campus"}
    render_with(event={**settings["event"], "location": location})
    index_html = (output_folder / "index.html").read_text(encoding="utf-8")

    assert f'<img src="{photo}" alt="Campus"' in index_html
    assert "Foto do local em breve" not in index_html

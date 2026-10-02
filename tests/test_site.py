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

    for key in ["logo", "favicon", "preview_image"]:
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

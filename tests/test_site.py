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

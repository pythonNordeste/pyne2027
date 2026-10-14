import functools
import http.server
import random
import shutil
from datetime import UTC, datetime
from pathlib import Path
from xml.sax.saxutils import escape

from jinja2 import Environment, FileSystemLoader
from typer import Typer
from yaml import safe_load

settings_file = Path(__file__).parent / "variables.yaml"
pages_folder = Path(__file__).parent / "pages"
templates_folder = Path(__file__).parent / "templates"
static_folder = Path(__file__).parent / "static"
output_folder = Path(__file__).parent / "dist"


cli = Typer(no_args_is_help=True)
environment = Environment(loader=FileSystemLoader(searchpath=pages_folder.parent))
environment.filters["shuffle"] = lambda seq: random.sample(list(seq), k=len(seq))


def load_settings() -> dict:
    if settings_file.exists():
        return safe_load(settings_file.read_text()) or {}
    return {}


def write_sitemap(site_url: str) -> None:
    """Gera dist/sitemap.xml com as páginas renderizadas (referenciado no robots.txt)."""
    lastmod = datetime.now(UTC).date().isoformat()
    entries = []
    for page in sorted(output_folder.glob("*.html")):
        path = "/" if page.name == "index.html" else f"/{page.name}"
        priority = "1.0" if path == "/" else "0.8"
        entries.append(
            "  <url>\n"
            f"    <loc>{escape(site_url + path)}</loc>\n"
            f"    <lastmod>{lastmod}</lastmod>\n"
            "    <changefreq>weekly</changefreq>\n"
            f"    <priority>{priority}</priority>\n"
            "  </url>"
        )
    (output_folder / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(entries)
        + "\n</urlset>\n"
    )


@cli.command()
def render():
    """Gera os arquivos HTML estáticos na pasta dist."""
    settings = load_settings()

    if output_folder.exists():
        shutil.rmtree(output_folder)

    output_folder.mkdir(exist_ok=True)
    static_folder.copy(output_folder / static_folder.name)

    root_favicon = Path(__file__).parent / "favicon.ico"
    if root_favicon.exists():
        shutil.copy(root_favicon, output_folder / "favicon.ico")

    for file in pages_folder.glob("*.j2"):
        template_path = file.relative_to(pages_folder.parent).as_posix()
        template = environment.get_template(template_path)
        rendered_content = template.render(settings)
        output_file = output_folder / file.with_suffix(".html").name
        output_file.write_text(rendered_content)

    # Geração automática de robots.txt com base no ambiente (staging vs production)
    is_staging = settings.get("environment") == "staging" or not settings.get(
        "allow_indexing", True
    )
    robots_file = output_folder / "robots.txt"
    if is_staging:
        robots_file.write_text("User-agent: *\nDisallow: /\n")
    else:
        site_url = settings.get("event", {}).get("url", "").rstrip("/")
        # CSS, JS e imagens liberados explicitamente: o Googlebot precisa deles
        # para renderizar a página e avaliá-la corretamente (mobile-first).
        robots_lines = [
            "User-agent: *",
            "Allow: /",
            "",
            "User-agent: Googlebot",
            "Allow: /",
            "Allow: /static/",
            "",
            "User-agent: Googlebot-Image",
            "Allow: /static/img/",
            "",
        ]
        if site_url:
            robots_lines.append(f"Sitemap: {site_url}/sitemap.xml")
            write_sitemap(site_url)
        robots_file.write_text("\n".join(robots_lines) + "\n")

    # Arquivo .nojekyll para o GitHub Pages servir arquivos estáticos diretamente
    (output_folder / ".nojekyll").touch()


@cli.command()
def start(port: int = 8000, host: str = "127.0.0.1"):
    """Inicia o servidor web local com Live Reload em tempo real."""
    render()

    try:
        from livereload import Server

        server = Server()
        # Monitora dados, templates, páginas e estáticos
        server.watch(str(settings_file), render)
        server.watch(str(pages_folder / "*.j2"), render)
        server.watch(str(templates_folder / "*.j2"), render)
        server.watch(str(static_folder), render)

        print(
            f"🔥 Servidor com Live Reload rodando em http://{host}:{port}/ (Ctrl+C para encerrar)"
        )
        server.serve(root=str(output_folder), host=host, port=port, open_url=True)
    except ImportError:
        handler = functools.partial(
            http.server.SimpleHTTPRequestHandler, directory=str(output_folder)
        )
        server = http.server.ThreadingHTTPServer((host, port), handler)
        print(
            f"Servidor rodando em http://{host}:{port}/ (pressione Ctrl+C para encerrar)"
        )
        print(
            "💡 Dica: instale as dependências de dev ('uv sync --extra dev') para ativar o Live Reload automático."
        )
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\nServidor encerrado.")
            server.server_close()


if __name__ == "__main__":
    cli()

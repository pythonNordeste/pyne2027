import functools
import http.server
import random
import shutil
from pathlib import Path

from jinja2 import Environment, FileSystemLoader
from typer import Typer
from yaml import safe_load

settings_file = Path(__file__).parent / 'variables.yaml'
pages_folder = Path(__file__).parent / 'pages'
static_folder = Path(__file__).parent / 'static'
output_folder = Path(__file__).parent / 'dist'


cli = Typer(no_args_is_help=True)
settings = safe_load(settings_file.read_text())
environment = Environment(
    loader=FileSystemLoader(
        searchpath=pages_folder.parent
    )
)
environment.filters['shuffle'] = lambda seq: random.sample(list(seq), k=len(seq))


@cli.command()
def render():
    """Gera os arquivos HTML estáticos na pasta dist."""
    if output_folder.exists():
        shutil.rmtree(output_folder)

    output_folder.mkdir(exist_ok=True)
    static_folder.copy(output_folder / static_folder.name)
    
    for file in pages_folder.glob('*.j2'):
        template_path = file.relative_to(pages_folder.parent).as_posix()
        template = environment.get_template(template_path)
        rendered_content = template.render(settings)
        output_file = output_folder / file.with_suffix('.html').name
        output_file.write_text(rendered_content)


@cli.command()
def start(port: int = 8000, host: str = "127.0.0.1"):
    """Renderiza os templates e inicia um servidor web local."""
    render()
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(output_folder))
    server = http.server.ThreadingHTTPServer((host, port), handler)
    print(f"Servidor rodando em http://{host}:{port}/ (pressione Ctrl+C para encerrar)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor encerrado.")
        server.server_close()


if __name__ == "__main__":
    cli()

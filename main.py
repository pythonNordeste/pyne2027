from typer import Typer
from jinja2 import Environment, FileSystemLoader
from yaml import safe_load
from pathlib import Path

import random
import shutil


settings_file = Path(__file__).parent / 'variables.yaml'
pages_folder = Path(__file__).parent / 'pages'
static_folder = Path(__file__).parent / 'static'
output_folder = Path(__file__).parent / 'dist'


cli = Typer()
settings = safe_load(settings_file.read_text())
environment = Environment(
    loader=FileSystemLoader(
        searchpath=pages_folder.parent
    )
)
environment.filters['shuffle'] = lambda seq: random.sample(list(seq), k=len(seq))


@cli.command()
def render():
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


if __name__ == "__main__":
    cli()

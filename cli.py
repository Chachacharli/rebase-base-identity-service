import subprocess

import typer

app = typer.Typer()

@app.command()
def run() -> None:
    """Levanta el servidor con fastapi en modo desarrollo."""
    subprocess.run(["fastapi", "dev", "app/main.py"])


"""Console script for cities_of_eternal_spring_in_europe."""
import cities_of_eternal_spring_in_europe

import typer
from rich.console import Console

app = typer.Typer()
console = Console()


@app.command()
def main():
    """Console script for cities_of_eternal_spring_in_europe."""
    console.print("Replace this message by putting your code into "
               "cities_of_eternal_spring_in_europe.cli.main")
    console.print("See Typer documentation at https://typer.tiangolo.com/")
    


if __name__ == "__main__":
    app()

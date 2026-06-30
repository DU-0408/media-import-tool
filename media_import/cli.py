"""
Interactive command-line interface for collecting import options.
"""

from rich.console import Console
from rich.panel import Panel
from rich.prompt import IntPrompt, Prompt

from .config import (
    ImportConfig,
    ImportType,
    MediaType,
    SourceType,
)

console = Console()


def run_cli() -> ImportConfig:
    console.print()

    console.print(
        Panel.fit(
            "[bold cyan]🎬 Media Import Tool[/bold cyan]",
            border_style="cyan",
        )
    )

    console.print()

    source_choice = IntPrompt.ask(
        "[bold]Select Source[/bold]\n"
        "1. Local File\n"
        "2. Download URL",
        choices=["1", "2"],
    )

    source_type = (
        SourceType.LOCAL
        if source_choice == 1
        else SourceType.URL
    )

    console.print()

    media_choice = IntPrompt.ask(
        "[bold]Select Media Type[/bold]\n"
        "1. Movie\n"
        "2. TV Show",
        choices=["1", "2"],
    )

    media_type = (
        MediaType.MOVIE
        if media_choice == 1
        else MediaType.TV_SHOW
    )

    if media_type == MediaType.MOVIE:
        import_type = ImportType.MOVIE
        season = None

    else:
        console.print()

        import_choice = IntPrompt.ask(
            "[bold]Select Import Type[/bold]\n"
            "1. Single Episode\n"
            "2. Full Season",
            choices=["1", "2"],
        )

        import_type = (
            ImportType.SINGLE_EPISODE
            if import_choice == 1
            else ImportType.FULL_SEASON
        )

        season = IntPrompt.ask(
            "Season Number",
            default=1,
            choices=[str(i) for i in range(1, 100)]
        )

    console.print()

    source = Prompt.ask("Local file path or download URL")

    title = Prompt.ask("Title", default="").strip() or None

    year = None

    while True:
        year_text = Prompt.ask("Year", default="").strip()

        if not year_text:
            break

        if year_text.isdigit():
            year = int(year_text)
            break

        console.print("[red]Please enter a valid year.[/red]")

    return ImportConfig(
        source_type=source_type,
        media_type=media_type,
        import_type=import_type,
        source=source,
        title=title,
        year=year,
        season=season,
    )

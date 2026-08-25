"""
Interactive command-line interface for collecting import options using questionary.
"""

from rich.console import Console
from rich.panel import Panel
import questionary
import sys

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

    source_choice = questionary.select(
        "Select Source:",
        choices=[
            "Local File",
            "Download URL",
            "Exit"
        ]
    ).ask()

    if source_choice == "Exit" or source_choice is None:
        console.print("\n[yellow]Exiting Media Import Tool.[/yellow]")
        sys.exit(0)

    source_type = SourceType.LOCAL if source_choice == "Local File" else SourceType.URL

    media_choice = questionary.select(
        "Select Media Type:",
        choices=[
            "Movie",
            "TV Show",
            "Special"
        ]
    ).ask()
    
    if media_choice is None:
        sys.exit(0)

    if media_choice == "Movie":
        media_type = MediaType.MOVIE
        import_type = ImportType.MOVIE
        season = None
    elif media_choice == "Special":
        media_type = MediaType.SPECIAL
        import_type = ImportType.SPECIAL
        season = None
    else:
        media_type = MediaType.TV_SHOW
        import_choice = questionary.select(
            "Select Import Type:",
            choices=[
                "Single Episode",
                "Full Season"
            ]
        ).ask()
        
        if import_choice is None:
            sys.exit(0)

        import_type = ImportType.SINGLE_EPISODE if import_choice == "Single Episode" else ImportType.FULL_SEASON

        season_str = questionary.text(
            "Season Number:",
            default="1",
            validate=lambda text: text.isdigit() and int(text) > 0 or "Please enter a valid positive number"
        ).ask()
        
        if season_str is None:
            sys.exit(0)
            
        season = int(season_str)
        
    is_marvel = questionary.confirm(
        "Is this part of the Marvel Universe?",
        default=False
    ).ask()

    source = questionary.text("Local file path or download URL:").ask()
    if source is None:
        sys.exit(0)

    title = questionary.text("Title (optional):").ask()
    if title is None:
        sys.exit(0)
    title = title.strip() or None

    year_str = questionary.text(
        "Year (optional):",
        validate=lambda text: True if not text.strip() else (text.isdigit() or "Please enter a valid year")
    ).ask()
    
    if year_str is None:
        sys.exit(0)
        
    year = int(year_str) if year_str.strip() else None

    return ImportConfig(
        source_type=source_type,
        media_type=media_type,
        import_type=import_type,
        source=source.strip(),
        title=title,
        year=year,
        season=season,
        is_marvel=is_marvel,
    )

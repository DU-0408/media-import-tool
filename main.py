#!/usr/bin/env python3

import os
import sys
import tempfile
import shutil
from pathlib import Path
from rich.console import Console

from media_import.cli import run_cli
from media_import.config import SourceType, MediaType, ImportConfig
from media_import.constants import (
    MOVIES_DIR,
    TV_SHOWS_DIR,
    SPECIALS_DIR,
    MARVEL_MOVIES_DIR,
    MARVEL_SHOWS_DIR,
    MARVEL_SPECIALS_DIR,
    OWNER,
    GROUP,
    DIR_PERMS,
    FILE_PERMS
)
from media_import.downloader import download_file
from media_import.extractor import extract_archive
from media_import.renamer import rename_media
from media_import.permissions import set_permissions
from media_import.mover import move_media
from media_import.jellyfin import refresh_library

console = Console()

def main():
    if os.geteuid() != 0:
        console.print("[red][bold]Error:[/bold] This tool must be run as root (using sudo) to set correct file permissions and access the destination directories.[/red]")
        sys.exit(1)

    try:
        config = run_cli()
    except KeyboardInterrupt:
        console.print("\n[yellow]Import cancelled by user.[/yellow]")
        sys.exit(0)

    def get_destination_dir(cfg: ImportConfig) -> Path:
        if cfg.is_marvel:
            if cfg.media_type == MediaType.MOVIE:
                return Path(MARVEL_MOVIES_DIR)
            elif cfg.media_type == MediaType.SPECIAL:
                return Path(MARVEL_SPECIALS_DIR)
            else:
                return Path(MARVEL_SHOWS_DIR)
        else:
            if cfg.media_type == MediaType.MOVIE:
                return Path(MOVIES_DIR)
            elif cfg.media_type == MediaType.SPECIAL:
                return Path(SPECIALS_DIR)
            else:
                return Path(TV_SHOWS_DIR)

    # Pre-flight check: see if the destination folder already exists
    import questionary
    final_dest_dir = get_destination_dir(config)
    title_str = config.title or "Unknown"
    year_str = f" ({config.year})" if config.year else ""
    expected_path = final_dest_dir / f"{title_str}{year_str}"
    
    if expected_path.exists():
        console.print(f"\n[yellow]Warning: The destination '{expected_path}' already exists.[/yellow]")
        overwrite = questionary.confirm("Do you want to update/overwrite the existing files?").ask()
        if not overwrite:
            console.print("[yellow]Import cancelled by user.[/yellow]")
            sys.exit(0)

    console.print()
    console.print("[bold cyan]Starting Import Process...[/bold cyan]")
    
    # Create a temporary working directory
    base_temp_dir = Path(tempfile.mkdtemp(prefix="media_import_"))
    
    try:
        # Step 1: Download or locate source file
        if config.source_type == SourceType.URL:
            target_path = download_file(config.source, base_temp_dir)
        else:
            target_path = Path(config.source).resolve()
            if not target_path.exists():
                console.print(f"[red]Local file not found: {target_path}[/red]")
                sys.exit(1)

        # Step 2: Extract if it's a TV show archive (ZIP/RAR)
        from media_import.extractor import is_supported_archive
        if config.media_type == MediaType.TV_SHOW and is_supported_archive(target_path):
            target_path = extract_archive(target_path, base_temp_dir)

        # Step 3: Rename and structure
        structured_dir = rename_media(target_path, config, base_temp_dir)

        # Step 4: Set permissions
        set_permissions(structured_dir, OWNER, GROUP, DIR_PERMS, FILE_PERMS)

        # Step 5: Move to final destination
        final_dest = move_media(structured_dir, final_dest_dir)

        # Step 6: Notify Jellyfin
        refresh_library()

        console.print(f"\n[bold green]🎉 Import completed successfully![/bold green]")
        console.print(f"Media is now available at: [cyan]{final_dest}[/cyan]")
        
    except Exception as e:
        console.print(f"\n[bold red]An error occurred during import:[/bold red] {e}")
        sys.exit(1)
        
    finally:
        # Cleanup temporary directory
        if base_temp_dir.exists():
            shutil.rmtree(base_temp_dir, ignore_errors=True)

if __name__ == "__main__":
    main()

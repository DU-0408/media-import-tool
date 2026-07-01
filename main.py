#!/usr/bin/env python3

import os
import sys
import tempfile
import shutil
from pathlib import Path
from rich.console import Console

from media_import.cli import run_cli
from media_import.config import SourceType, MediaType
from media_import.constants import (
    MOVIES_DIR,
    TV_SHOWS_DIR,
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

        # Step 2: Extract if it's a TV show ZIP
        if config.media_type == MediaType.TV_SHOW and target_path.suffix.lower() == '.zip':
            target_path = extract_archive(target_path, base_temp_dir)

        # Step 3: Rename and structure
        structured_dir = rename_media(target_path, config, base_temp_dir)

        # Step 4: Set permissions
        set_permissions(structured_dir, OWNER, GROUP, DIR_PERMS, FILE_PERMS)

        # Step 5: Move to final destination
        final_dest_dir = Path(MOVIES_DIR) if config.media_type == MediaType.MOVIE else Path(TV_SHOWS_DIR)
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

"""
Handles extracting ZIP and RAR files for TV shows.
"""
import zipfile
import rarfile
from pathlib import Path
from rich.console import Console

console = Console()

def is_supported_archive(path: Path) -> bool:
    """Checks if the file is a supported archive type (ZIP or RAR)."""
    return zipfile.is_zipfile(path) or rarfile.is_rarfile(path)

def extract_archive(archive_path: Path, dest_dir: Path) -> Path:
    """
    Extracts a ZIP or RAR archive to the destination directory.
    Returns the path to the directory containing the extracted files.
    """
    console.print(f"[cyan]Extracting {archive_path.name}...[/cyan]")
    
    extract_path = dest_dir / f"{archive_path.stem}_extracted"
    extract_path.mkdir(parents=True, exist_ok=True)
    
    if zipfile.is_zipfile(archive_path):
        with zipfile.ZipFile(archive_path, 'r') as zip_ref:
            zip_ref.extractall(extract_path)
    elif rarfile.is_rarfile(archive_path):
        with rarfile.RarFile(archive_path, 'r') as rar_ref:
            rar_ref.extractall(extract_path)
    else:
        raise ValueError(f"Unsupported archive format for {archive_path}")
        
    console.print(f"[green]Extracted to {extract_path}[/green]")
    return extract_path

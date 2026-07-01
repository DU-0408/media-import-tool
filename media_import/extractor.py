"""
Handles extracting ZIP files for TV shows.
"""
import zipfile
from pathlib import Path
from rich.console import Console

console = Console()

def extract_archive(archive_path: Path, dest_dir: Path) -> Path:
    """
    Extracts a ZIP archive to the destination directory.
    Returns the path to the directory containing the extracted files.
    """
    console.print(f"[cyan]Extracting {archive_path.name}...[/cyan]")
    
    extract_path = dest_dir / archive_path.stem
    extract_path.mkdir(parents=True, exist_ok=True)
    
    with zipfile.ZipFile(archive_path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)
        
    console.print(f"[green]Extracted to {extract_path}[/green]")
    return extract_path

"""
Handles moving the processed files to the final media directories.
"""
import shutil
from pathlib import Path
from rich.console import Console

console = Console()

def move_media(source_path: Path, dest_dir: Path) -> Path:
    """
    Moves a file or directory to the destination directory.
    If a directory with the same name exists, it attempts to merge contents.
    Returns the final destination path.
    """
    console.print(f"[cyan]Moving {source_path.name} to {dest_dir}...[/cyan]")
    
    dest_dir.mkdir(parents=True, exist_ok=True)
    final_dest = dest_dir / source_path.name
    
    # If it's a directory and it already exists, merge it
    if source_path.is_dir() and final_dest.exists():
        for item in source_path.iterdir():
            shutil.move(str(item), str(final_dest / item.name))
        source_path.rmdir()
    else:
        # Move directly
        # If moving a single file that exists, it will overwrite
        shutil.move(str(source_path), str(final_dest))
        
    console.print(f"[green]Successfully moved to {final_dest}[/green]")
    return final_dest

"""
Handles downloading files from URLs with a progress bar.
"""
import os
import requests
from pathlib import Path
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn, DownloadColumn, TimeRemainingColumn, TransferSpeedColumn, TimeElapsedColumn

def download_file(url: str, dest_dir: Path) -> Path:
    """
    Downloads a file from a URL to the destination directory.
    Returns the path to the downloaded file.
    """
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        
        # Try to get filename from Content-Disposition header
        filename = None
        if "Content-Disposition" in r.headers:
            cd = r.headers["Content-Disposition"]
            if "filename=" in cd:
                filename = cd.split("filename=")[1].strip('"\'')
        
        # Fallback to URL path
        if not filename:
            filename = url.split("/")[-1]
            if not filename or "?" in filename:
                filename = "downloaded_file"
        
        dest_path = dest_dir / filename
        
        total_size = int(r.headers.get("content-length", 0))
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            DownloadColumn(),
            TransferSpeedColumn(),
            TimeElapsedColumn(),
            TimeRemainingColumn(),
        ) as progress:
            task = progress.add_task(f"[cyan]Downloading {filename}...", total=total_size)
            
            with open(dest_path, "wb") as f:
                # Use a larger chunk size (1MB) to smooth out the speed/time estimation
                for chunk in r.iter_content(chunk_size=1024 * 1024):
                    if chunk:
                        f.write(chunk)
                        progress.update(task, advance=len(chunk))
                        
    return dest_path

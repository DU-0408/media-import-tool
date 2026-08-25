"""
Handles renaming files to Jellyfin standards.
"""
import os
import re
from pathlib import Path
from rich.console import Console
from .config import ImportConfig, MediaType, ImportType

console = Console()

VIDEO_EXTENSIONS = {'.mkv', '.mp4', '.avi', '.webm'}

def get_video_files(directory: Path) -> list[Path]:
    """Recursively get all video files in a directory."""
    video_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            path = Path(root) / file
            if path.suffix.lower() in VIDEO_EXTENSIONS:
                video_files.append(path)
    return sorted(video_files)

def extract_episode_number(filename: str) -> int | None:
    """Attempts to extract an episode number from a filename."""
    # Match S01E05 or E05
    match = re.search(r'[sS]\d+[eE](\d+)|[eE](\d+)', filename)
    if match:
        return int(match.group(1) or match.group(2))
    
    # Match plain numbers like 05 or 5
    match = re.search(r'(\d+)', filename)
    if match:
        return int(match.group(1))
    
    return None

def rename_media(source_path: Path, config: ImportConfig, base_temp_dir: Path) -> Path:
    """
    Renames and structures media according to Jellyfin standards in a temporary directory.
    Returns the path to the root folder that should be moved to the final destination.
    """
    console.print("[cyan]Structuring and renaming files...[/cyan]")
    
    # Format base names
    year_str = f" ({config.year})" if config.year else ""
    title_str = f"{config.title}{year_str}"
    
    if config.media_type in (MediaType.MOVIE, MediaType.SPECIAL):
        # Structure: Title (Year)/Title (Year).ext
        movie_dir = base_temp_dir / title_str
        movie_dir.mkdir(parents=True, exist_ok=True)
        
        # Determine source file (if zip, find the largest video file)
        if source_path.is_dir():
            videos = get_video_files(source_path)
            if not videos:
                raise ValueError("No video files found in the extracted archive.")
            # Assuming the largest video file is the movie/special
            target_file = max(videos, key=lambda p: p.stat().st_size)
        else:
            target_file = source_path
            
        ext = target_file.suffix if target_file.suffix else '.mkv'
        new_file_path = movie_dir / f"{title_str}{ext}"
        
        os.rename(target_file, new_file_path)
        return movie_dir
        
    elif config.media_type == MediaType.TV_SHOW:
        # Structure: Show Title (Year)/Season X/Show Title (Year) S0X E0Y.ext
        season_num = config.season if config.season else 1
        season_str = f"Season {season_num:02d}" if season_num >= 1 else f"Season {season_num}"
        
        show_dir = base_temp_dir / title_str
        season_dir = show_dir / season_str
        season_dir.mkdir(parents=True, exist_ok=True)
        
        if config.import_type == ImportType.SINGLE_EPISODE:
            target_file = source_path
            ep_num = extract_episode_number(target_file.name) or 1
            ext = target_file.suffix if target_file.suffix else '.mkv'
            new_file_path = season_dir / f"{title_str} S{season_num:02d}E{ep_num:02d}{ext}"
            os.rename(target_file, new_file_path)
            
        elif config.import_type == ImportType.FULL_SEASON:
            if not source_path.is_dir():
                raise ValueError("Source path for full season must be a directory (extracted zip).")
                
            videos = get_video_files(source_path)
            if not videos:
                raise ValueError("No video files found in the extracted archive.")
                
            for idx, video_path in enumerate(videos):
                # Try to extract episode number, fallback to sequential order
                ep_num = extract_episode_number(video_path.stem)
                if ep_num is None:
                    ep_num = idx + 1
                    
                ext = video_path.suffix
                new_file_path = season_dir / f"{title_str} S{season_num:02d}E{ep_num:02d}{ext}"
                os.rename(video_path, new_file_path)
                
        return show_dir

    raise ValueError(f"Unsupported media type: {config.media_type}")

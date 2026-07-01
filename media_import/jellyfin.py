"""
Handles communication with the Jellyfin API.
"""
import requests
from rich.console import Console
from .constants import JELLYFIN_URL, JELLYFIN_API_KEY

console = Console()

def refresh_library():
    """
    Triggers a library scan in Jellyfin via the API.
    """
    if not JELLYFIN_URL or not JELLYFIN_API_KEY:
        console.print("[yellow]Jellyfin URL or API Key not configured. Skipping library refresh.[/yellow]")
        return

    url = f"{JELLYFIN_URL.rstrip('/')}/Library/Refresh"
    headers = {
        "X-Emby-Token": JELLYFIN_API_KEY
    }
    
    console.print("[cyan]Triggering Jellyfin library scan...[/cyan]")
    try:
        response = requests.post(url, headers=headers)
        response.raise_for_status()
        console.print("[green]Jellyfin library scan initiated successfully.[/green]")
    except requests.exceptions.RequestException as e:
        console.print(f"[red]Failed to trigger Jellyfin library scan: {e}[/red]")

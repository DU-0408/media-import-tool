"""
Handles setting permissions for Jellyfin media.
"""
import os
import pwd
import grp
from pathlib import Path
from rich.console import Console

console = Console()

def set_permissions(path: Path, owner: str, group: str, dir_perms: int, file_perms: int):
    """
    Recursively sets ownership and permissions for directories and files.
    """
    console.print(f"[cyan]Setting permissions for {path}...[/cyan]")
    
    try:
        uid = pwd.getpwnam(owner).pw_uid
        gid = grp.getgrnam(group).gr_gid
    except KeyError as e:
        console.print(f"[red]Error finding user or group: {e}[/red]")
        console.print("[yellow]Ensure you are running with sufficient privileges (sudo) and the user/group exists.[/yellow]")
        return

    # Set for the root path first
    os.chown(path, uid, gid)
    if path.is_dir():
        os.chmod(path, dir_perms)
    else:
        os.chmod(path, file_perms)

    if path.is_dir():
        for root, dirs, files in os.walk(path):
            for d in dirs:
                dir_path = os.path.join(root, d)
                os.chown(dir_path, uid, gid)
                os.chmod(dir_path, dir_perms)
            for f in files:
                file_path = os.path.join(root, f)
                os.chown(file_path, uid, gid)
                os.chmod(file_path, file_perms)
                
    console.print("[green]Permissions set successfully.[/green]")

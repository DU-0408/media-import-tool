# 🎬 Media Import Tool

A robust, interactive command-line utility to automate the process of importing movies and TV shows into a Jellyfin homelab media library. 

## Features

- **Interactive UI:** A smooth, arrow-key driven CLI built with `rich` and `questionary`.
- **Multi-Source Support:** Import media directly from a local file path or a direct download URL (featuring a live progress bar).
- **Automated Extraction:** Automatically detects and extracts `.zip` archives into a safe temporary workspace before processing.
- **Smart Renaming & Structuring:** Renames media files and structures them to adhere strictly to Jellyfin conventions (e.g., `Movie Title (Year)/Movie Title (Year).mkv` or `Show Title (Year)/Season X/Show Title (Year) SXXEYY.mkv`).
- **Overwrite Protection:** Detects if a movie or TV show folder already exists and asks for your confirmation before safely updating or overwriting files.
- **Homelab Permissions:** Automatically applies strict permission structures (`chmod 775/664`) and sets group ownership (`fadmin:mediausers`) to ensure Nextcloud/Jellyfin compatibility.
- **Global Access & Auto-Updater:** The tool installs itself globally as `import-media`, allowing you to run it from any directory. It also includes an `import-media update` command to automatically pull the latest code and sync dependencies.
- **Jellyfin Auto-Refresh:** Automatically pings your Jellyfin server via API when an import finishes to trigger a library scan instantly.

## Installation

Clone the repository to your server and run the installation script:

```bash
git clone https://github.com/DU-0408/media-import-tool.git
cd media-import-tool
bash install.sh
```

During installation, a `.env` file will be generated from `.env.example`. Open the newly created `.env` file and add your Jellyfin API Key so the script can auto-refresh your library:
```bash
nano .env
```

## Usage

Because the tool manages root-level `/mnt` directories and configures permissions, it requires `sudo` privileges. The installation script generates a global wrapper that handles this for you.

Simply type the following from anywhere in your terminal:
```bash
import-media
```
And follow the interactive prompts!

### Updating
If you ever want to update the tool with the latest changes from GitHub, simply run:
```bash
import-media update
```
The script will automatically fetch the latest code and install any new dependencies.

## Supported Media Types
- **Movies**: Single `.mp4`, `.mkv`, etc.
- **TV Shows**: Accepts ZIP archives containing episodes. (Note: Currently optimized to process one season at a time).

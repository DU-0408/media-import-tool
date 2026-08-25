"""
Constants for the Media Import Tool.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file in the project root
ENV_PATH = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=ENV_PATH)

# Destination Directories
MOVIES_DIR = "/mnt/s1/Movies"
TV_SHOWS_DIR = "/mnt/s1/Web_Shows"
SPECIALS_DIR = "/mnt/s1/Specials"

MARVEL_MOVIES_DIR = "/mnt/s1/Marvel/Movies"
MARVEL_SHOWS_DIR = "/mnt/s1/Marvel/Shows"
MARVEL_SPECIALS_DIR = "/mnt/s1/Marvel/Specials"

# Permissions
OWNER = "fadmin"
GROUP = "mediausers"
DIR_PERMS = 0o775
FILE_PERMS = 0o664

# Jellyfin API
JELLYFIN_URL = os.getenv("JELLYFIN_URL", "http://localhost:8096")
JELLYFIN_API_KEY = os.getenv("JELLYFIN_API_KEY", "")

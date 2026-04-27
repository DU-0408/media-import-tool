#!/home/fadmin/media_env/bin/python

import os
import re
import sys
import shutil
import requests
import zipfile
import tarfile
import subprocess
import uuid
from tqdm import tqdm

# --------------------------
# CONFIG
# --------------------------

MOVIE_ROOT = "/path/to/Movies"
SHOW_ROOT = "/path/to/Web_Shows"

USER = "username"
GROUP = "group-username"

JELLYFIN_SERVICE = "jellyfin"

# --------------------------
# GLOBAL OVERRIDES
# --------------------------

OVERRIDE_NAME = None
OVERRIDE_YEAR = None
OVERRIDE_SEASON = None
FORCE_SHOW = False

# --------------------------
# HELPERS
# --------------------------

def sanitize(name):
    return re.sub(r"[._\-]+", " ", name).strip()


def detect_year(name):
    match = re.search(r"(19|20)\d{2}", name)
    return match.group(0) if match else None


def is_show(filename):
    return bool(re.search(r"[Ss]\d{1,2}[Ee]\d{1,2}", filename))


# --------------------------
# DOWNLOAD WITH PROGRESS
# --------------------------

def download_file(url):
    local_filename = f"download_{uuid.uuid4().hex[:8]}.bin"

    print(f"\n📥 Downloading → {local_filename}")

    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        total = int(r.headers.get('content-length', 0))

        with open(local_filename, "wb") as f, tqdm(
            total=total,
            unit='B',
            unit_scale=True,
            desc=local_filename
        ) as bar:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    bar.update(len(chunk))

    return local_filename


# --------------------------
# EXTRACT ARCHIVES
# --------------------------

def extract_archive(file):
    print(f"\n📦 Extracting → {file}")

    extract_dir = "temp_extract"

    if os.path.exists(extract_dir):
        shutil.rmtree(extract_dir)

    os.makedirs(extract_dir)

    if zipfile.is_zipfile(file):
        with zipfile.ZipFile(file, "r") as zip_ref:
            zip_ref.extractall(extract_dir)

    elif tarfile.is_tarfile(file):
        with tarfile.open(file, "r:*") as tar:
            tar.extractall(extract_dir)

    elif file.endswith(".rar"):
        subprocess.run(["unrar", "x", file, extract_dir], check=True)

    else:
        print("❌ Unsupported archive format.")
        sys.exit(1)

    os.remove(file)
    return extract_dir


# --------------------------
# MOVIE PROCESSING
# --------------------------

def process_movie(file):
    basename = os.path.basename(file)

    year = OVERRIDE_YEAR if OVERRIDE_YEAR else detect_year(basename)

    name = re.sub(r"\.\w+$", "", basename)
    name = OVERRIDE_NAME if OVERRIDE_NAME else sanitize(name.replace(year, "") if year else name)

    title = f"{name} ({year})" if year else name
    dest_dir = os.path.join(MOVIE_ROOT, title)

    os.makedirs(dest_dir, exist_ok=True)

    new_path = os.path.join(dest_dir, f"{title}{os.path.splitext(file)[1]}")
    shutil.move(file, new_path)

    print(f"🎬 Movie → {new_path}")
    return dest_dir


# --------------------------
# SHOW PROCESSING
# --------------------------

def process_show(file):
    basename = os.path.basename(file)

    season_ep = re.search(r"[Ss](\d{1,2})[Ee](\d{1,2})", basename)

    if not season_ep and not OVERRIDE_SEASON:
        return None

    season = OVERRIDE_SEASON if OVERRIDE_SEASON else season_ep.group(1).zfill(2)
    episode = season_ep.group(2).zfill(2) if season_ep else "01"

    show_name = re.sub(r"[Ss]\d{1,2}[Ee]\d{1,2}.*", "", basename)
    show_name = OVERRIDE_NAME if OVERRIDE_NAME else sanitize(show_name)

    year = OVERRIDE_YEAR if OVERRIDE_YEAR else detect_year(basename)

    show_dir = os.path.join(SHOW_ROOT, show_name)
    season_dir = os.path.join(show_dir, f"Season {season}")

    os.makedirs(season_dir, exist_ok=True)

    ext = os.path.splitext(file)[1]

    if year:
        new_name = f"{show_name} ({year}) S{season}E{episode}{ext}"
    else:
        new_name = f"{show_name} S{season}E{episode}{ext}"

    new_path = os.path.join(season_dir, new_name)
    shutil.move(file, new_path)

    print(f"📺 Episode → {new_path}")
    return show_dir


# --------------------------
# DIRECTORY PROCESSING
# --------------------------

def process_directory(path):
    affected = set()

    for root, _, files in os.walk(path):
        for f in files:
            full_path = os.path.join(root, f)

            if FORCE_SHOW or is_show(f):
                result = process_show(full_path)
            else:
                result = process_movie(full_path)

            if result:
                affected.add(result)

    shutil.rmtree(path)
    return affected


# --------------------------
# PERMISSIONS
# --------------------------

def fix_permissions(path):
    subprocess.run(["chown", "-R", f"{USER}:{GROUP}", path])
    subprocess.run(["chmod", "-R", "770", path])


# --------------------------
# JELLYFIN REFRESH
# --------------------------

def restart_jellyfin():
    print("\n🔄 Refreshing Jellyfin...")
    subprocess.run(["systemctl", "restart", JELLYFIN_SERVICE])


# --------------------------
# MAIN CLI
# --------------------------

def main():
    print("\n🎬 MEDIA IMPORT TOOL\n")

    # INTERACTIVE INPUTS
    input_path = input("👉 Paste URL or drag file here: ").strip()

    manual_name = input("👉 Enter title (leave blank for auto): ").strip()
    manual_year = input("👉 Enter year (leave blank for auto): ").strip()

    is_show_manual = input("👉 Is this a show? (y/n, leave blank for auto): ").strip().lower()

    manual_season = None
    if is_show_manual == "y":
        manual_season = input("👉 Enter season number: ").strip().zfill(2)

    # SET GLOBAL OVERRIDES
    global OVERRIDE_NAME, OVERRIDE_YEAR, OVERRIDE_SEASON, FORCE_SHOW

    OVERRIDE_NAME = manual_name if manual_name else None
    OVERRIDE_YEAR = manual_year if manual_year else None
    OVERRIDE_SEASON = manual_season
    FORCE_SHOW = True if is_show_manual == "y" else False

    # URL or local
    if input_path.startswith("http"):
        file = download_file(input_path)
    else:
        if not os.path.exists(input_path):
            print("❌ File not found")
            sys.exit(1)
        file = input_path

    # Archive or direct file
    if any(file.endswith(ext) for ext in [".zip", ".tar", ".tar.gz", ".tgz", ".rar"]):
        extracted = extract_archive(file)
        paths = process_directory(extracted)

        for p in paths:
            fix_permissions(p)

    else:
        if FORCE_SHOW or is_show(file):
            path = process_show(file)
        else:
            path = process_movie(file)

        if path:
            fix_permissions(path)

    restart_jellyfin()
    print("\n✅ Import completed successfully!\n")


if __name__ == "__main__":
    main()

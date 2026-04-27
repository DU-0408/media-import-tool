# 🎬 Media Import Tool

A CLI tool to automate media ingestion for Jellyfin.

---

## 🚀 Features

- Download media from URL
- Supports archives (zip, tar)
- Automatic extraction
- Smart renaming (Movies & TV Shows)
- Season & episode detection
- Manual override support
- Jellyfin-ready structure
- Automatic permission handling

---

## ⚙️ Installation

```bash
git clone https://github.com/DU-0408/media-import-tool.git
cd media-import-tool
pip install -r requirements.txt
```
---

## ▶️ Usage

python media-import.py

## Interactive Flow

```
👉 Paste URL or file path  
👉 Enter title (optional)  
👉 Enter year (optional)  
👉 Is this a show? (y/n)  
👉 Enter season (if show)  
```

## 📂 Output Structure

```
Movies/  
  Movie Name (Year)/Movie Name (Year).mkv  

Web_Shows/  
  Show Name/  
    Season 01/  
      Show Name (Year) S01E01.mkv  
```

## 🧠 Tech Stack

* Python
* requests
* tqdm
* subprocess

## 📌 Future Improvements

* Metadata fetching (TMDB)
* GUI version
* Background downloads
* File type auto-detection


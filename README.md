<div align="center">

# 🎧 DeeMusic

**FastAPI Gateway & Music Engine powered by Deezer, YouTube Music, and LRCLIB**

[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

*An all-in-one music processing suite for metadata retrieval, dynamic audio streaming, high-quality downloading, and synchronized lyrics.*

---

</div>

## 📌 Overview

**DeeMusic** is a hybrid music engine designed to bridge metadata retrieval and audio streaming seamlessness:

> *This API allows you to retrieve information—such as artists, playlists, radio stations, tracks, and albums—from Deezer and then use the YT Music API for streaming and downloading. It also includes functionality to fetch lyrics from the lrclib API.*

Additionally, the project features a **CustomTkinter GUI Desktop Application** with a real-time **Animated Canvas Gradient** that dynamically adapts to the color scheme of any playing track's cover art.

---

## ✨ Key Features

- **📂 Comprehensive Deezer Proxy:** Full proxy coverage across 15 Deezer API resources (Albums, Artists, Charts, Playlists, Tracks, Podcasts, Genres, etc.).
- **⚡ YT Music Streaming Engine:** Real-time stream URL extraction via `ytmusicapi` and `yt-dlp` for full-track VLC playback (bypassing 30s previews).
- **📥 320kbps MP3 Downloader:** High-quality audio downloader complete with automatic ID3 tag embedding (Title, Artist, Album, and Cover Art).
- **🎤 Synchronized Lyrics:** Instant lyric retrieval powered by the LRCLIB API.
- **🎨 Dynamic Gradient GUI:** CustomTkinter desktop interface featuring smooth color interpolation algorithms (Lerp) for animated background canvas visuals.

---

## 🛠️ Architecture & Tech Stack

- **Backend:** FastAPI, Uvicorn, Requests
- **Audio Engine:** `ytmusicapi`, `yt-dlp`, `python-vlc`
- **Metadata Tags:** `mutagen`
- **Frontend GUI:** `customtkinter`, `Pillow (PIL)`

---

## 🚀 Quick Start

### 1. Installation

Clone the repository and install the dependencies:

```bash
git clone [https://github.com/YOUR_USERNAME/deemusic.git](https://github.com/YOUR_USERNAME/deemusic.git)
cd deemusic

pip install -r requirements.txt

<div align="center">

# 🎧 DeeMusic API

<table align="center" border="0" style="border: none; background: transparent;">
  <tr style="border: none; background: transparent;">
    <td align="center" valign="middle" style="border: none; padding: 0 12px;">
      <a href="javascript:void(0)"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/7/75/Deezer_logo%2C_2023.svg/3840px-Deezer_logo%2C_2023.svg.png" height="32" alt="Deezer" /></a>
    </td>
    <td align="center" valign="middle" style="border: none; padding: 0 6px; font-size: 18px; font-weight: bold;">
      ✖
    </td>
    <td align="center" valign="middle" style="border: none; padding: 0 12px;">
      <a href="javascript:void(0)"><img src="https://upload.wikimedia.org/wikipedia/commons/1/1c/YouTube_Music_2024.svg" height="36" alt="YouTube Music" /></a>
    </td>
    <td align="center" valign="middle" style="border: none; padding: 0 6px; font-size: 18px; font-weight: bold;">
      ✖
    </td>
    <td align="center" valign="middle" style="border: none; padding: 0 12px;">
      <a href="javascript:void(0)"><img src="https://lrclib.net/assets/lrclib-370c57eb.png" height="42" alt="LRCLIB" /></a>
    </td>
  </tr>
</table>

**FastAPI Gateway & Music Engine powered by Deezer, YouTube Music, and LRCLIB**

[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

*An all-in-one music processing suite for metadata retrieval, dynamic audio streaming, high-quality downloading, and synchronized lyrics.*

---

</div>

> ⚠️ **Notice / Work in Progress:**  
> This project is currently under active development. Some features may be unstable, updated frequently, or produce unexpected bugs/errors. Feel free to open an issue if you encounter any problems!

---

## 📌 Overview

**DeeMusic API** is a hybrid music engine designed to bridge metadata retrieval and audio streaming seamlessly:

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

## 🛠️ Integrated Platforms & Tech Stack

| Platform / Tool | Role in DeeMusic |
| :---: | :--- |
| <a href="javascript:void(0)"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/7/75/Deezer_logo%2C_2023.svg/3840px-Deezer_logo%2C_2023.svg.png" width="110" /></a> | **Metadata Provider** (Search, Track Info, Albums, Playlists) |
| <a href="javascript:void(0)"><img src="https://upload.wikimedia.org/wikipedia/commons/1/1c/YouTube_Music_2024.svg" width="130" /></a> | **Audio Engine** (Direct Audio Streaming & MP3 Download) |
| <a href="javascript:void(0)"><img src="https://lrclib.net/assets/lrclib-370c57eb.png" width="80" /></a> | **Lyrics Engine** (Plain & Synced Lrc Lyrics) |
| **FastAPI / Python** | **Core Backend Gateway & GUI Engine** |

---

## 🚀 Quick Start

### 1. Installation

Clone the repository and install the dependencies:

```bash
git clone [https://github.com/kien9998800/DeeMusic-API.git](https://github.com/kien9998800/DeeMusic-API.git)
cd DeeMusic-API

pip install -r requirements.txt

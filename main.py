import os
import re
import tempfile
import requests
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse
from ytmusicapi import YTMusic
import yt_dlp
from mutagen.id3 import ID3, APIC, TIT2, TPE1, TALB, ID3NoHeaderError

# Tắt OpenAPI Schema và toàn bộ trang Docs UI
app = FastAPI(
    docs_url=None,
    redoc_url=None,
    openapi_url=None
)

DEEZER_BASE = "https://api.deezer.com"
LRCLIB_URL = "https://lrclib.net/api"
ytmusic = YTMusic()


def fetch_deezer(endpoint: str, params: dict = None):
    """Hàm proxy gửi request tới Deezer API"""
    try:
        res = requests.get(f"{DEEZER_BASE}/{endpoint}", params=params, timeout=10)
        if res.status_code != 200:
            raise HTTPException(status_code=res.status_code, detail="Lỗi phản hồi từ Deezer API")
        return res.json()
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Không thể kết nối Deezer API: {str(e)}")


def clean_filename(name: str) -> str:
    return re.sub(r'[\\/*?:"<>|]', "", name)


def embed_id3_metadata(mp3_path: str, title: str, artist: str, album: str, cover_url: str):
    try:
        try:
            audio = ID3(mp3_path)
        except ID3NoHeaderError:
            audio = ID3()

        audio.delete(mp3_path)
        audio = ID3()
        audio.add(TIT2(encoding=3, text=title))
        audio.add(TPE1(encoding=3, text=artist))
        if album:
            audio.add(TALB(encoding=3, text=album))

        if cover_url:
            headers = {'User-Agent': 'Mozilla/5.0'}
            img_res = requests.get(cover_url, headers=headers, timeout=15)
            if img_res.status_code == 200:
                mime_type = 'image/png' if cover_url.lower().endswith('.png') else 'image/jpeg'
                audio.add(APIC(encoding=3, mime=mime_type, type=3, desc='Cover', data=img_res.content))

        audio.save(mp3_path, v2_version=3)
    except Exception as e:
        print(f"[!] Lỗi nhúng ID3 Tag: {e}")


# =====================================================================
# 15 ENDPOINTS DEEZER PROXY
# =====================================================================

# 1. ALBUM
@app.get("/album/{album_id}")
def get_album(album_id: str):
    return fetch_deezer(f"album/{album_id}")


@app.get("/album/{album_id}/tracks")
def get_album_tracks(album_id: str):
    return fetch_deezer(f"album/{album_id}/tracks")


# 2. ARTIST
@app.get("/artist/{artist_id}")
def get_artist(artist_id: str):
    return fetch_deezer(f"artist/{artist_id}")


@app.get("/artist/{artist_id}/top")
def get_artist_top(artist_id: str, limit: int = 10):
    return fetch_deezer(f"artist/{artist_id}/top", params={"limit": limit})


# 3. CHART
@app.get("/chart")
def get_chart():
    return fetch_deezer("chart")


@app.get("/chart/{genre_id}")
def get_chart_by_genre(genre_id: str):
    return fetch_deezer(f"chart/{genre_id}")


# 4. EDITORIAL
@app.get("/editorial")
def get_editorial():
    return fetch_deezer("editorial")


# 5. EPISODE
@app.get("/episode/{episode_id}")
def get_episode(episode_id: str):
    return fetch_deezer(f"episode/{episode_id}")


# 6. GENRE
@app.get("/genre")
def get_genres():
    return fetch_deezer("genre")


@app.get("/genre/{genre_id}")
def get_genre_detail(genre_id: str):
    return fetch_deezer(f"genre/{genre_id}")


# 7. INFOS
@app.get("/infos")
def get_infos():
    return fetch_deezer("infos")


# 8. OEMBED
@app.get("/oembed")
def get_oembed(url: str = Query(...)):
    return fetch_deezer("oembed", params={"url": url})


# 9. OPTIONS
@app.get("/options")
def get_options():
    return fetch_deezer("options")


# 10. PLAYLIST
@app.get("/playlist/{playlist_id}")
def get_playlist(playlist_id: str):
    return fetch_deezer(f"playlist/{playlist_id}")


# 11. PODCAST
@app.get("/podcast/{podcast_id}")
def get_podcast(podcast_id: str):
    return fetch_deezer(f"podcast/{podcast_id}")


# 12. RADIO
@app.get("/radio")
def get_radios():
    return fetch_deezer("radio")


@app.get("/radio/genres")
def get_radio_genres():
    return fetch_deezer("radio/genres")


# 13. SEARCH
@app.get("/search")
def search_deezer(q: str = Query(...), limit: int = 20):
    return fetch_deezer("search", params={"q": q, "limit": limit})


# 14. TRACK
@app.get("/track/{track_id}")
def get_track(track_id: str):
    return fetch_deezer(f"track/{track_id}")


# 15. USER
@app.get("/user/{user_id}")
def get_user(user_id: str):
    return fetch_deezer(f"user/{user_id}")


# =====================================================================
# MEDIA ENGINE ENDPOINTS (STREAMING / DOWNLOAD / LYRICS)
# =====================================================================

@app.get("/stream/{track_id}")
def stream_audio(track_id: str):
    """Lấy Direct Streaming URL từ YouTube Music cho VLC Player phát full bài"""
    try:
        track_data = fetch_deezer(f"track/{track_id}")
        title = track_data.get("title")
        artist_name = track_data.get("artist", {}).get("name", "")

        search_query = f"{title} {artist_name}"
        search_results = ytmusic.search(search_query, filter="songs", limit=1)
        if not search_results or "videoId" not in search_results[0]:
            raise HTTPException(status_code=404, detail="Không tìm thấy bài hát trên YTMusic")

        yt_video_id = search_results[0]["videoId"]
        yt_url = f"https://music.youtube.com/watch?v={yt_video_id}"

        ydl_opts = {
            'format': 'bestaudio/best',
            'quiet': True,
            'no_warnings': True,
            'extractor_args': {'youtube': {'player_client': ['android', 'ios']}}
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(yt_url, download=False)
            stream_url = info.get('url')

        if not stream_url:
            raise HTTPException(status_code=500, detail="Không thể lấy URL stream")

        return {"stream_url": stream_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/lyrics")
def get_lyrics(title: str, artist: str):
    """Lấy lời bài hát từ LRCLIB API"""
    try:
        res = requests.get(f"{LRCLIB_URL}/get", params={"track_name": title, "artist_name": artist}, timeout=10)
        if res.status_code == 200:
            data = res.json()
            lyrics = data.get("syncedLyrics") or data.get("plainLyrics")
            return {"lyrics": lyrics or "Không tìm thấy lời bài hát."}

        search_res = requests.get(f"{LRCLIB_URL}/search", params={"q": f"{title} {artist}"}, timeout=10)
        if search_res.status_code == 200 and search_res.json():
            first = search_res.json()[0]
            lyrics = first.get("syncedLyrics") or first.get("plainLyrics")
            return {"lyrics": lyrics or "Không tìm thấy lời bài hát."}

        return {"lyrics": "Không tìm thấy lời bài hát."}
    except Exception as e:
        return {"lyrics": f"Lỗi lấy lời bài hát: {e}"}


@app.get("/download/{track_id}")
def download_mp3(track_id: str, title: str = "song"):
    """Tải MP3 320kbps chất lượng cao thông qua YouTube Music + yt-dlp"""
    try:
        track_data = fetch_deezer(f"track/{track_id}")
        title = track_data.get("title", title)
        artist_name = track_data.get("artist", {}).get("name", "Unknown")
        album_name = track_data.get("album", {}).get("title", "")
        cover_url = track_data.get("album", {}).get("cover_xl") or track_data.get("album", {}).get("cover_big", "")

        search_query = f"{title} {artist_name}"
        search_results = ytmusic.search(search_query, filter="songs", limit=1)
        if not search_results or "videoId" not in search_results[0]:
            raise HTTPException(status_code=404, detail="Không tìm thấy bài hát trên hệ thống tải")

        yt_video_id = search_results[0]["videoId"]
        yt_url = f"https://music.youtube.com/watch?v={yt_video_id}"

        out_dir = tempfile.gettempdir()
        clean_title = clean_filename(f"{artist_name} - {title}")
        final_mp3 = os.path.join(out_dir, f"{clean_title}.mp3")

        if not os.path.exists(final_mp3):
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': os.path.join(out_dir, f"{clean_title}.%(ext)s"),
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '320',
                }],
                'quiet': True,
                'no_warnings': True,
                'extractor_args': {'youtube': {'player_client': ['android', 'ios']}},
                'http_headers': {'User-Agent': 'Mozilla/5.0'}
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([yt_url])

            embed_id3_metadata(final_mp3, title, artist_name, album_name, cover_url)

        return FileResponse(final_mp3, media_type="audio/mpeg", filename=f"{clean_title}.mp3")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
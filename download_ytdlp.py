# download_ytdlp.py
import sys
from yt_dlp import YoutubeDL
from pathlib import Path

def download(url: str, output_path: str = "downloads", format_choice: str = "best"):
    out_dir = Path(output_path)
    out_dir.mkdir(parents=True, exist_ok=True)
    ydl_opts = {
        'outtmpl': str(out_dir / '%(title)s [%(id)s].%(ext)s'),
        'format': format_choice,  # e.g. 'bestvideo[height<=720]+bestaudio/best'
        'merge_output_format': 'mp4',  # when merging video+audio
        'noplaylist': False,  # set True to disable playlist downloads
        'writesubtitles': False,  # set True to download subtitles
        'ignoreerrors': True,
        'quiet': False,
        'no_warnings': True,
        # 'proxy': 'http://127.0.0.1:8080', # if needed
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python download_ytdlp.py <url> [output_folder] [format]")
    else:
        url = sys.argv[1]
        out = sys.argv[2] if len(sys.argv) > 2 else "downloads"
        fmt = sys.argv[3] if len(sys.argv) > 3 else "best"
        download(url, out, fmt)

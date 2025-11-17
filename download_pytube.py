# download_pytube.py
import sys
from pytube import YouTube
from pathlib import Path

def download_video(url: str, output_path: str = ".", resolution: str = "highest"):
    try:
        yt = YouTube(url, on_progress_callback=on_progress)
    except Exception as e:
        print("Error initializing YouTube:", e)
        return

    print(f"Title: {yt.title}")
    print(f"Author: {yt.author}")
    print(f"Length: {yt.length}s")

    # Select stream
    if resolution == "audio":
        stream = yt.streams.filter(only_audio=True).order_by("abr").desc().first()
    elif resolution == "highest":
        stream = yt.streams.filter(progressive=True).order_by("resolution").desc().first()
    else:
        # try to pick exact resolution like "720p"
        stream = yt.streams.filter(res=resolution, progressive=True).first()
        if stream is None:
            print(f"Requested resolution {resolution} not available. Falling back to highest progressive.")
            stream = yt.streams.filter(progressive=True).order_by("resolution").desc().first()

    if stream is None:
        print("No suitable stream found.")
        return

    out_dir = Path(output_path)
    out_dir.mkdir(parents=True, exist_ok=True)
    print(f"Downloading to {out_dir.resolve()} ...")
    stream.download(output_path=str(out_dir))
    print("Download finished.")

def on_progress(stream, chunk, bytes_remaining):
    total = stream.filesize
    done = total - bytes_remaining
    percent = int(done / total * 100)
    print(f"\rDownloading... {percent}% ", end="")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python download_pytube.py <youtube_url> [output_folder] [resolution|audio]")
    else:
        url = sys.argv[1]
        out = sys.argv[2] if len(sys.argv) > 2 else "."
        res = sys.argv[3] if len(sys.argv) > 3 else "highest"
        download_video(url, out, res)

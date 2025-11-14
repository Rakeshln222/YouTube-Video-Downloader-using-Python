
# 🎬 **YouTube Video Downloader Using Python**

---

## 🔹 1. Project Overview

The **YouTube Video Downloader** is a Python-based application designed to download YouTube videos, audio tracks, or playlists directly to a user’s local system.
It leverages open-source Python libraries — **pytube** or **yt-dlp** — to extract video information and download media in various resolutions and formats (such as MP4 or MP3).

The project provides both **Command Line Interface (CLI)** and an optional **Graphical User Interface (GUI)** using `Tkinter` for user-friendly interaction.

---

## 🔹 2. Objectives

* To develop a Python application capable of downloading videos or audio from YouTube.
* To allow the user to choose:

  * Desired **video resolution (e.g., 720p, 1080p)** or **audio-only**.
  * **Download location** on the system.
* To handle **playlists**, **progress updates**, and **error handling** efficiently.
* To demonstrate the integration of Python with APIs and GUI development.

---

## 🔹 3. Motivation

YouTube is one of the largest video platforms, but offline access is often limited. Many users need a personal tool to download educational lectures, music, or tutorials for offline use.

This project aims to create a **lightweight, customizable, and open-source downloader** that can be easily modified for learning and educational purposes.

---

## 🔹 4. Technologies Used

| Component                  | Description                                                 |
| -------------------------- | ----------------------------------------------------------- |
| **Language**               | Python 3.x                                                  |
| **Main Libraries**         | `pytube` or `yt-dlp`                                        |
| **GUI Toolkit (optional)** | `Tkinter`                                                   |
| **Additional Tools**       | `ffmpeg` (for audio conversion), `tqdm` (for progress bars) |
| **OS Compatibility**       | Windows, macOS, Linux                                       |

---

## 🔹 5. System Requirements

**Hardware:**

* Minimum 2 GB RAM
* Internet connection (for downloading)
* 200 MB free disk space

**Software:**

* Python 3.8 or above
* Installed libraries (`pytube` or `yt-dlp`)
* `ffmpeg` (optional, for audio conversion)

---

## 🔹 6. Libraries and Installation

Use the following commands to install dependencies:

```bash
pip install pytube
# or (recommended for reliability)
pip install yt-dlp
pip install tqdm
```

If you plan to convert videos to MP3:

```bash
# Install ffmpeg:
# Windows: choco install ffmpeg
# macOS: brew install ffmpeg
# Ubuntu: sudo apt install ffmpeg
```

---

## 🔹 7. Working Principle

1. **Input:** User provides the YouTube URL.
2. **Fetch Metadata:** The program uses `pytube` or `yt-dlp` to fetch details such as title, author, duration, and available streams.
3. **Select Stream:** Based on user preference (resolution, audio-only, etc.), the best matching stream is selected.
4. **Download:** The file is downloaded and saved to the selected folder.
5. **(Optional)** Post-processing with `ffmpeg` converts audio streams to MP3.
6. **Completion:** The app notifies the user when the download is complete.

---

## 🔹 8. Project Workflow Diagram

```
 ┌───────────────────────┐
 │    Start Program      │
 └──────────┬────────────┘
            │
            ▼
 ┌──────────────────────────┐
 │ Enter YouTube Video URL │
 └──────────┬──────────────┘
            │
            ▼
 ┌─────────────────────────────┐
 │ Fetch video information     │
 │ using pytube / yt-dlp       │
 └──────────┬─────────────────┘
            │
            ▼
 ┌─────────────────────────────┐
 │ Select format/resolution    │
 └──────────┬─────────────────┘
            │
            ▼
 ┌─────────────────────────────┐
 │ Download video/audio file   │
 └──────────┬─────────────────┘
            │
            ▼
 ┌─────────────────────────────┐
 │ Save file to output folder  │
 └──────────┬─────────────────┘
            │
            ▼
 ┌──────────────────────────┐
 │ Display success message  │
 └──────────┬──────────────┘
            │
            ▼
        ┌───────────┐
        │   End     │
        └───────────┘
```

---

## 🔹 9. Source Code (CLI Version Using `yt-dlp`)

```python
# youtube_downloader.py
from yt_dlp import YoutubeDL
from pathlib import Path

def progress_hook(d):
    if d['status'] == 'downloading':
        print(f"\rDownloading: {d['_percent_str']} ETA: {d['_eta_str']}", end="")
    elif d['status'] == 'finished':
        print("\nDownload complete. Post-processing...")

def download_video(url, output_path="downloads", format_choice="best"):
    Path(output_path).mkdir(parents=True, exist_ok=True)
    
    options = {
        'outtmpl': str(Path(output_path) / '%(title)s [%(id)s].%(ext)s'),
        'format': format_choice,  # e.g. best, bestaudio/best, 720p
        'merge_output_format': 'mp4',
        'progress_hooks': [progress_hook],
        'noplaylist': False,
        'ignoreerrors': True,
    }

    with YoutubeDL(options) as ydl:
        ydl.download([url])

if __name__ == "__main__":
    url = input("Enter YouTube URL: ")
    choice = input("Enter format (best/bestaudio): ")
    path = input("Enter output folder (default: downloads): ") or "downloads"
    download_video(url, path, choice)
```

---

## 🔹 10. GUI Version (Tkinter)

```python
# youtube_gui.py
import tkinter as tk
from tkinter import filedialog, messagebox
import threading
from yt_dlp import YoutubeDL
from pathlib import Path

def download(url, out, fmt):
    Path(out).mkdir(parents=True, exist_ok=True)
    opts = {
        'outtmpl': str(Path(out) / '%(title)s [%(id)s].%(ext)s'),
        'format': fmt,
        'merge_output_format': 'mp4',
        'progress_hooks': [progress_hook],
        'ignoreerrors': True,
    }
    with YoutubeDL(opts) as ydl:
        ydl.download([url])

def progress_hook(d):
    if d['status'] == 'downloading':
        progress_var.set(f"Downloading: {d['_percent_str']} ETA: {d['_eta_str']}")
    elif d['status'] == 'finished':
        progress_var.set("Download complete!")

def browse():
    folder = filedialog.askdirectory()
    if folder:
        folder_var.set(folder)

def start_download():
    url = url_var.get()
    fmt = format_var.get()
    out = folder_var.get()
    if not url:
        messagebox.showerror("Error", "Please enter a URL!")
        return
    threading.Thread(target=download, args=(url, out, fmt), daemon=True).start()

root = tk.Tk()
root.title("YouTube Downloader")

url_var = tk.StringVar()
folder_var = tk.StringVar(value="downloads")
format_var = tk.StringVar(value="best")
progress_var = tk.StringVar()

tk.Label(root, text="YouTube URL:").pack(anchor="w", padx=10)
tk.Entry(root, textvariable=url_var, width=60).pack(padx=10)

tk.Label(root, text="Output Folder:").pack(anchor="w", padx=10)
tk.Entry(root, textvariable=folder_var, width=45).pack(side="left", padx=10)
tk.Button(root, text="Browse", command=browse).pack(side="left")

tk.Label(root, text="Format (best/bestaudio):").pack(anchor="w", padx=10)
tk.Entry(root, textvariable=format_var, width=30).pack(padx=10)

tk.Button(root, text="Download", command=start_download).pack(pady=10)
tk.Label(root, textvariable=progress_var, fg="blue").pack(pady=5)

root.mainloop()
```

---

## 🔹 11. Output Examples

* **Console Output:**

  ```
  Enter YouTube URL: https://www.youtube.com/watch?v=abcd123
  Enter format (best/bestaudio): best
  Enter output folder: downloads
  Downloading:  45.3% ETA: 00:12
  Download complete. Post-processing...
  ```

* **GUI Output:**
  Displays a window with input fields, a browse button, and a real-time progress update label.

---

## 🔹 12. Key Features

✅ Download videos in different resolutions (360p, 720p, 1080p).
✅ Download audio-only files (MP3 format).
✅ Download entire playlists automatically.
✅ GUI for non-technical users.
✅ Progress tracking during downloads.
✅ Error handling for invalid URLs or network issues.

---

## 🔹 13. Advantages

* Lightweight and open-source.
* Easy to use and customizable.
* Supports most video formats.
* Can run on any platform with Python installed.
* Optionally integrates with `ffmpeg` for higher-quality output.

---

## 🔹 14. Limitations

* Depends on YouTube’s internal APIs; may need updates if site structure changes.
* Some videos (age-restricted or private) may fail to download without authentication.
* Requires `ffmpeg` installation for MP3 conversion.
* Large files may take significant time or disk space.

---

## 🔹 15. Future Enhancements

* Add **multi-threaded downloads** for speed optimization.
* Integrate **YouTube Data API** for video search.
* Add **auto-update** and **download queue** features.
* Provide **dark mode UI** and **progress bar widget** in GUI.
* Allow **resuming interrupted downloads**.
* Build **Flask-based web interface** for remote downloading.

---

## 🔹 16. Applications

* Downloading online lectures or tutorials.
* Saving music or podcasts for offline playback.
* Creating a personal video archive.
* Educational project to learn API usage and file handling in Python.

---

## 🔹 17. Conclusion

The **YouTube Video Downloader** project demonstrates the powerful combination of Python’s networking, GUI, and automation capabilities.
It offers a simple yet effective way to interact with online media sources and handle file downloads efficiently.

Through this project, we learn:

* How to integrate APIs and libraries (`yt-dlp`, `pytube`).
* How to design CLI and GUI applications in Python.
* How to handle files, threads, and progress updates.

It’s a practical project that enhances your understanding of Python’s real-world application development.

---

## 🔹 18. References

* [yt-dlp GitHub Repository](https://github.com/yt-dlp/yt-dlp)
* [pytube Documentation](https://pytube.io/en/latest/)
* [Python Tkinter Documentation](https://docs.python.org/3/library/tkinter.html)
* [FFmpeg Documentation](https://ffmpeg.org/documentation.html)

# downloader_gui.py
import threading
import tkinter as tk
from tkinter import filedialog, messagebox
from download_ytdlp import download  # reuse function from earlier

def browse_folder():
    folder = filedialog.askdirectory()
    if folder:
        out_var.set(folder)

def start_download():
    url = url_entry.get().strip()
    out = out_var.get().strip() or "downloads"
    fmt = fmt_entry.get().strip() or "best"
    if not url:
        messagebox.showerror("Error", "Please enter a URL")
        return
    # run in background thread so GUI stays responsive
    threading.Thread(target=run_download, args=(url,out,fmt), daemon=True).start()

def run_download(url, out, fmt):
    try:
        download(url, out, fmt)
        messagebox.showinfo("Done", "Download finished")
    except Exception as e:
        messagebox.showerror("Error", str(e))

root = tk.Tk()
root.title("YouTube Downloader")

tk.Label(root, text="YouTube URL:").grid(row=0, column=0, sticky="w")
url_entry = tk.Entry(root, width=60)
url_entry.grid(row=0, column=1, columnspan=2, pady=4)

tk.Label(root, text="Output folder:").grid(row=1, column=0, sticky="w")
out_var = tk.StringVar(value="downloads")
tk.Entry(root, textvariable=out_var, width=45).grid(row=1, column=1)
tk.Button(root, text="Browse", command=browse_folder).grid(row=1, column=2)

tk.Label(root, text="Format (yt-dlp):").grid(row=2, column=0, sticky="w")
fmt_entry = tk.Entry(root, width=60)
fmt_entry.insert(0, "best")
fmt_entry.grid(row=2, column=1, columnspan=2, pady=4)

tk.Button(root, text="Download", command=start_download).grid(row=3, column=1, pady=8)

root.mainloop()

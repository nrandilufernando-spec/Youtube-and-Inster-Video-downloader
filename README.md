# YouTube & Instagram Video Downloader (yt_dlp)

This script is a command-line tool built using **yt_dlp** to download YouTube and Instagram videos in multiple formats such as 360p, 720p, 1080p, and audio-only.

---

## 📌 Features

* Download video in **360p, 720p, 1080p** MP4 formats.
* Download **audio-only** in M4A.
* Automatically detects available formats.
* Saves videos and audio to predefined folders.
* Includes format filtering logic using `format_id`.

---

## 🛠️ Requirements

Make sure you have:

* Python 3.x installed
* `yt_dlp` module installed

Install using:

```bash
pip install yt-dlp
```

---

## ▶️ How to Use

1. Run the script.
2. Select the platform:

   * **1** → YouTube
   * **2** → Instagram
3. Enter the video URL.
4. Choose the output format:

   * **1** → 360p MP4
   * **2** → 720p MP4
   * **3** → 1080p MP4
   * **4** → Audio only
5. Script downloads the file to the configured folder.

---

## 📦 Code Overview

Below is the script used for downloading videos:

```python
import yt_dlp

name = "None"
format_ids = []
format_ids_audio = []

def selector():
    global index_val
    index_val = input("""\nPlease Select....
1. YouTube
2. Instergram
                        
Enter number: """)


def get_input():
    global link, format_tag
    link = input("Enter YouTube URL: ")
    print("""\nWhat format you need?
          
Press 1 360p MP4
Press 2 720p MP4
Press 3 1080p MP4
Press 4 Audio only\n""")
    format_tag = input("Enter the number:")

#there is a dictionary called info and the key 'formats' and ther another list with dictinaries inside it

def process2():
    with yt_dlp.YoutubeDL() as ydl:
        info = ydl.extract_info(link, download=False)
        inster_formats = info['formats']
        for i in range(len(inster_formats)):
            inster_formats_id = inster_formats[i]['format_id']
            has_video_format_note = (inster_formats[i].get('format_note', 'none')).upper()

            if inster_formats[i]['ext'] == "mp4" and has_video_format_note!='DASH VIDEO':
                format_ids.append(inster_formats_id)
            elif inster_formats[i]['ext']== "m4a" :
                format_ids_audio.append(inster_formats_id)
    process()


def process():
    try:
        global name, ydl_opts
        match (format_tag, index_val):
            case ("1", "1"):
                name = "360p"
                ydl_opts = {
                    'outtmpl': 'C:/Users/Randil fernando/Videos/Yt videos/%(title)s-%(format_note)s.%(ext)s',
                    'format': '18',
                }
            case ("1", "2"):
                name = "360p"
                ydl_opts = {
                    'outtmpl': 'C:/Users/Randil fernando/Videos/Yt videos/%(title)s-%(format_note)s.%(ext)s',
                    'format': f"{format_ids[0]}",
                }
            case ("2", "1"):
                name = "720p"
                ydl_opts = {
                    'outtmpl': 'C:/Users/Randil fernando/Videos/Yt videos/%(title)s.%(ext)s',
                    'format': '22',
                }
            case ("2", "2"):
                name = "720p"
                ydl_opts = {
                    'outtmpl': 'C:/Users/Randil fernando/Videos/Yt videos/%(title)s.%(ext)s',
                    'format': '1',
                }
            case ("3", "1"):
                name = "1080p"
                ydl_opts = {
                    'outtmpl': 'C:/Users/Randil fernando/Videos/Yt videos/%(title)s.%(ext)s',
                    'format': '137',
                }
            case ("3", "2"):
                name = "1080p"
                ydl_opts = {
                    'outtmpl': 'C:/Users/Randil fernando/Videos/Yt videos/%(title)s.%(ext)s',
                    'format': '1',
                }
            case ("4", "1"):
                name = "Audio"
                ydl_opts = {
                    'outtmpl': 'C:/Users/Randil fernando/Music/YT music/%(title)s.%(ext)s',
                    'format': '140',
                }
            case ("4", "2"):
                name = "Audio"
                ydl_opts = {
                    'outtmpl': 'C:/Users/Randil fernando/Music/YT music/%(title)s.%(ext)s',
                    'format': f'{format_ids_audio[0]}',
                }
        get_output()
    except:
        print("'Error', Problem in the data containers index")


def get_output():
    try:
        print(f"\nDownloading {name} format...\n\n")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([link])
        print("Download successfull .....\n.....\n")
    except:
        print("'' ERROR ' System paused due to format error.......")


def test():
    with yt_dlp.YoutubeDL() as ydl:
        info = ydl.extract_info(link, download=False)
        print(info['formats'])
        quit()
    
selector()
get_input()
process2()
```

---

## 📄 Notes

* Instagram URLs must be public.
* Some YouTube formats may not be available depending on the video.
* Modify output paths according to your system.

---

## 📬 Support

If you want, I can also generate a cleaner version of the script or turn this into a fully functional GUI app.

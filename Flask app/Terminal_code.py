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
        # Get video info first
        info = ydl.extract_info(link, download=False)
        inster_formats = info['formats']
        for i in range(len(inster_formats)):
            inster_formats_id = inster_formats[i]['format_id']
            # Safe way to check audio and video codecs
            #has_audio = inster_formats[i].get('acodec', 'none') 
            #has_video = inster_formats[i].get('vcodec', 'none') 
            has_video_format_note = (inster_formats[i].get('format_note', 'none')).upper()

            if inster_formats[i]['ext'] == "mp4" and has_video_format_note!='DASH VIDEO':
                #print(inster_formats[i])
                format_ids.append(inster_formats_id)
            elif inster_formats[i]['ext']== "m4a" :
                format_ids_audio.append(inster_formats_id)

        #print("\ninster format ids mp4", format_ids)
        #print("inster format ids audio only\n", format_ids_audio)
    process()

def process():
    try:
        #print("Now in function called process()")
        global name, ydl_opts
        match (format_tag, index_val):
            case ("1", "1"):
                name = "360p"
                ydl_opts = {
                # 'outtmpl': '%(title)s.%(ext)s',
                'outtmpl': 'C:/Users/Randil fernando/Videos/Yt videos/%(title)s-%(format_note)s.%(ext)s',
                'format': '18',  # Standard 360p MP4 that always plays
            }
            
            case ("1", "2"):
                name = "360p"
                ydl_opts = {
                # 'outtmpl': '%(title)s.%(ext)s',
                'outtmpl': 'C:/Users/Randil fernando/Videos/Yt videos/%(title)s-%(format_note)s.%(ext)s',
                'format': f"{format_ids[0]}",  # Standard 360p MP4 that always plays
            }

            case ("2", "1"):
                name = "720p"
                ydl_opts = {
                # 'outtmpl': '%(title)s.%(ext)s',
                'outtmpl': 'C:/Users/Randil fernando/Videos/Yt videos/%(title)s.%(ext)s',
                'format': '22',
            }
            case ("2", "2"):
                name = "720p"
                ydl_opts = {
                # 'outtmpl': '%(title)s.%(ext)s',
                'outtmpl': 'C:/Users/Randil fernando/Videos/Yt videos/%(title)s.%(ext)s',
                'format': '1',
            }

            case ("3", "1"):
                name = "1080p"
                ydl_opts = {
                # 'outtmpl': '%(title)s.%(ext)s',
                'outtmpl': 'C:/Users/Randil fernando/Videos/Yt videos/%(title)s.%(ext)s',
                'format': '137',
            }

            case ("3", "2"):
                name = "1080p"
                ydl_opts = {
                # 'outtmpl': '%(title)s.%(ext)s',
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
    #print("now in function output()\n")
    
    try:
        #print("now in function try block of output()\n")
        print(f"\nDownloading {name} format...\n\n")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([link])
        print("Download successfull .....\n.....\n")

    except:
        #print("now in function except block of output()\n")
               
        print("'' ERROR ' System paused due to format error.......")


def test():
    with yt_dlp.YoutubeDL() as ydl:
        # Get video info first
        info = ydl.extract_info(link, download=False)
        print(info['formats'])
        quit()
    
    
selector()
get_input()
#test()
process2()
from flask import Flask, render_template, request, jsonify, send_file
import yt_dlp
import os
import tempfile
import threading
import uuid

app = Flask(__name__)

# Global variables (maintaining your original names)
name = "None"
format_ids = []
format_ids_audio = []
link = ""
format_tag = ""
index_val = ""
ydl_opts = {}

# Download tracking
download_status = {}
download_files = {}  # NEW: Store downloaded file paths
download_lock = threading.Lock()

# Configuration - Update these paths as needed
VIDEO_DOWNLOAD_PATH = 'C:/Users/Randil fernando/Videos/Yt videos/%(title)s-%(format_note)s.%(ext)s'
AUDIO_DOWNLOAD_PATH = 'C:/Users/Randil fernando/Music/YT music/%(title)s.%(ext)s'

def selector(platform):
    """Your original selector function adapted for web"""
    global index_val
    index_val = platform
    return index_val

def get_input(url, format_choice):
    """Your original get_input function adapted for web"""
    global link, format_tag
    link = url
    format_tag = format_choice
    return link, format_tag

def process2():
    """Your original process2 function"""
    global format_ids, format_ids_audio
    
    # Reset format lists
    format_ids = []
    format_ids_audio = []
    
    try:
        with yt_dlp.YoutubeDL() as ydl:
            # Get video info first
            info = ydl.extract_info(link, download=False)
            inster_formats = info['formats']
            
            for i in range(len(inster_formats)):
                inster_formats_id = inster_formats[i]['format_id']
                has_video_format_note = (inster_formats[i].get('format_note', 'none')).upper()

                if inster_formats[i]['ext'] == "mp4" and has_video_format_note != 'DASH VIDEO':
                    format_ids.append(inster_formats_id)
                elif inster_formats[i]['ext'] == "m4a":
                    format_ids_audio.append(inster_formats_id)

        process()
        return True
    except Exception as e:
        print(f"Error in process2: {e}")
        return False

def process():
    """Your original process function"""
    global name, ydl_opts, format_ids, format_ids_audio
    
    try:
        # Set download path based on platform
        if index_val == "1":  # YouTube
            base_path = 'C:/Users/Randil fernando/Videos/Yt videos/'
        else:  # Instagram
            base_path = 'C:/Users/Randil fernando/Videos/Yt videos/'
        
        match (format_tag, index_val):
            case ("1", "1"):  # YouTube 360p
                name = "360p"
                ydl_opts = {
                    'outtmpl': 'C:/Users/Randil fernando/Videos/Yt videos/%(title)s-%(format_note)s.%(ext)s',
                    'format': '18',
                }
            
            case ("1", "2"):  # Instagram 360p
                name = "360p"
                ydl_opts = {
                    'outtmpl': 'C:/Users/Randil fernando/Videos/Yt videos/%(title)s-%(format_note)s.%(ext)s',
                    'format': f"{format_ids[0] if format_ids else '18'}",
                }

            case ("2", "1"):  # YouTube 720p
                name = "720p"
                ydl_opts = {
                    'outtmpl': 'C:/Users/Randil fernando/Videos/Yt videos/%(title)s.%(ext)s',
                    'format': '22',
                }
            
            case ("2", "2"):  # Instagram 720p
                name = "720p"
                ydl_opts = {
                    'outtmpl': 'C:/Users/Randil fernando/Videos/Yt videos/%(title)s.%(ext)s',
                    'format': f"{format_ids[1] if format_ids[1] else format_ids[0]}",
                }

            case ("3", "1"):  # YouTube 1080p
                name = "1080p"
                ydl_opts = {
                    'outtmpl': 'C:/Users/Randil fernando/Videos/Yt videos/%(title)s.%(ext)s',
                    'format': '137',
                }

            case ("3", "2"):  # Instagram 1080p
                name = "1080p"
                ydl_opts = {
                    'outtmpl': 'C:/Users/Randil fernando/Videos/Yt videos/%(title)s.%(ext)s',
                    'format': '1',
                }

            case ("4", "1"):  # YouTube Audio
                name = "Audio"
                ydl_opts = {
                    'outtmpl': 'C:/Users/Randil fernando/Music/YT music/%(title)s.%(ext)s',
                    'format': '140',
                }

            case ("4", "2"):  # Instagram Audio
                name = "Audio"
                ydl_opts = {
                    'outtmpl': 'C:/Users/Randil fernando/Music/YT music/%(title)s.%(ext)s',
                    'format': f'{format_ids_audio[0] if format_ids_audio else "140"}',
                }
        
        return True
        
    except Exception as e:
        print(f"Error in process: {e}")
        return False

def get_output(download_id):
    """Your original get_output function adapted for background processing"""
    global name, link, ydl_opts
    
    try:
        print(f"\nDownloading {name} format...\n\n")
        
        # Add progress hook to ydl_opts
        ydl_opts['progress_hooks'] = [lambda d: progress_hook(d, download_id)]
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # NEW: Get info first to track the actual filename
            info = ydl.extract_info(link, download=False)
            actual_filename = ydl.prepare_filename(info)
            
            # Download the video
            ydl.download([link])
            
        # NEW: Store the actual file path for download
        with download_lock:
            download_files[download_id] = actual_filename
            download_status[download_id] = {
                'status': 'completed', 
                'message': f"Download successful - {name} format",
                'filename': os.path.basename(actual_filename)  # NEW: Include filename for display
            }
            
        print("Download successful .....\n.....\n")
        return True

    except Exception as e:
        print(f"Error in get_output: {e}")
        with download_lock:
            download_status[download_id] = {
                'status': 'error', 
                'message': f"Download failed: {str(e)}"
            }
        return False

def progress_hook(d, download_id):
    """Update download progress"""
    if d['status'] == 'downloading':
        total_bytes = d.get('total_bytes') or d.get('total_bytes_estimate', 0)
        downloaded_bytes = d.get('downloaded_bytes', 0)
        
        if total_bytes > 0:
            progress = (downloaded_bytes / total_bytes) * 100
            with download_lock:
                download_status[download_id] = {
                    'status': 'downloading', 
                    'progress': round(progress, 1),
                    'message': f"Downloading... {round(progress, 1)}%"
                }

def test():
    """Your original test function"""
    with yt_dlp.YoutubeDL() as ydl:
        info = ydl.extract_info(link, download=False)
        print(info['formats'])
        return info['formats']

# Flask Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_video_info', methods=['POST'])
def get_video_info():
    """Get video information and available formats"""
    global link
    
    data = request.json
    url = data.get('url')
    platform = data.get('platform', '1')  # Default to YouTube
    
    if not url:
        return jsonify({'error': 'URL is required'}), 400
    
    try:
        # Set global variables (mimicking your original flow)
        selector(platform)
        get_input(url, "")  # Format choice will be set later
        
        # Get video info using yt-dlp
        with yt_dlp.YoutubeDL() as ydl:
            info = ydl.extract_info(url, download=False)
            
            # Get available formats
            formats = info.get('formats', [])
            video_formats = []
            audio_formats = []
            
            for fmt in formats:
                # Video formats
                if fmt.get('vcodec') != 'none' and fmt.get('ext') == 'mp4':
                    format_note = fmt.get('format_note', 'unknown')
                    height = fmt.get('height', 0)
                    if height and format_note != 'DASH VIDEO':
                        video_formats.append({
                            'format_id': fmt['format_id'],
                            'resolution': f"{height}p",
                            'format_note': format_note,
                            'ext': fmt.get('ext', 'mp4')
                        })
                
                # Audio formats
                elif fmt.get('acodec') != 'none' and fmt.get('vcodec') == 'none':
                    audio_formats.append({
                        'format_id': fmt['format_id'],
                        'format_note': fmt.get('format_note', 'audio'),
                        'ext': fmt.get('ext', 'm4a')
                    })
            
            # Remove duplicates and sort
            video_formats = sorted(
                list({f['resolution']: f for f in video_formats}.values()),
                key=lambda x: int(x['resolution'].replace('p', '')),
                reverse=True
            )
            
            return jsonify({
                'title': info.get('title', 'Unknown'),
                'thumbnail': info.get('thumbnail', ''),
                'duration': info.get('duration', 0),
                'video_formats': video_formats,
                'audio_formats': audio_formats
            })
            
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/download', methods=['POST'])
def download():
    """Start download using your original functions"""
    global link, format_tag, index_val
    
    data = request.json
    url = data.get('url')
    platform = data.get('platform')
    format_choice = data.get('format_choice')
    
    if not url or not platform or not format_choice:
        return jsonify({'error': 'URL, platform, and format are required'}), 400
    
    try:
        # Set global variables using your original functions
        selector(platform)
        get_input(url, format_choice)
        
        # Process formats (your original process2 function)
        if not process2():
            return jsonify({'error': 'Failed to process video formats'}), 400
        
        # Generate download ID
        download_id = str(uuid.uuid4())
        
        # Initialize download status
        with download_lock:
            download_status[download_id] = {
                'status': 'starting', 
                'progress': 0,
                'message': 'Starting download...'
            }
        
        # Start download in background thread
        thread = threading.Thread(
            target=get_output, 
            args=(download_id,)
        )
        thread.daemon = True
        thread.start()
        
        return jsonify({
            'download_id': download_id,
            'message': f'Download started for {name} format'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/status/<download_id>')
def get_status(download_id):
    """Get download status"""
    with download_lock:
        status = download_status.get(download_id, {'status': 'unknown', 'message': 'Download not found'})
    return jsonify(status)

# NEW: Download file endpoint
@app.route('/download_file/<download_id>')
def download_file(download_id):
    """Download completed file"""
    with download_lock:
        if download_id in download_files and os.path.exists(download_files[download_id]):
            filename = download_files[download_id]
            download_name = os.path.basename(filename)
            
            return send_file(
                filename,
                as_attachment=True,
                download_name=download_name
            )
        else:
            return jsonify({'error': 'File not found or download not completed'}), 404

""""@app.route('/cleanup/<download_id>', methods=['DELETE'])
def cleanup_download(download_id):
    #Clean up download tracking data
    with download_lock:
        if download_id in download_status:
            del download_status[download_id]
        if download_id in download_files:
            # Note: We don't delete the actual file, just the tracking
            del download_files[download_id]
    return jsonify({'message': 'Cleaned up'})"""


if __name__ == '__main__':
    app.run(debug=True)
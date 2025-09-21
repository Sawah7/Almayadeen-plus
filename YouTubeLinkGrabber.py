import yt_dlp
import os

def get_channel_stream_url(channel_url):
    try:
        ydl_opts = {
            'quiet': True,
            'extract_flat': False,
            'forcejson': True,
            'no_warnings': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(channel_url, download=False)
            
            if 'entries' in info:
                for entry in info['entries']:
                    if entry.get('is_live'):
                        return entry['url']
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None

# Create M3U file
with open('youtube.m3u', 'w', encoding='utf-8') as f:
    f.write('#EXTM3U\n')
    
    try:
        with open('./YouTubeLink.txt', 'r', encoding='utf-8') as channel_file:
            lines = channel_file.readlines()
            i = 0
            while i < len(lines):
                line = lines[i].strip()
                if not line or line.startswith('##'):
                    i += 1
                    continue
                    
                if not line.startswith('http'):
                    # Channel name line
                    if i + 1 < len(lines) and lines[i + 1].startswith('http'):
                        channel_name = line.split('-')[0].strip()
                        group_title = line.split('-')[1].strip() if '-' in line else 'General'
                        stream_url = get_channel_stream_url(lines[i + 1].strip())
                        
                        if stream_url:
                            f.write(f'#EXTINF:-1 group-title="{group_title}", {channel_name}\n')
                            f.write(f'{stream_url}\n')
                        i += 2
                    else:
                        i += 1
                else:
                    i += 1
                    
    except FileNotFoundError:
        print("YouTubeLink.txt not found")
    except Exception as e:
        print(f"Error: {e}")

# Cleanup
if 'temp.txt' in os.listdir():
    os.remove('temp.txt')

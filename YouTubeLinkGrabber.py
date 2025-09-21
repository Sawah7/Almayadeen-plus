import yt_dlp
import os

CHANNEL_URL = "https://www.youtube.com/@france24"

def get_stream_url():
    try:
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'socket_timeout': 5,
            'extract_flat': False
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(CHANNEL_URL, download=False)
            if info and info.get('is_live'):
                return info['url']
    except Exception as e:
        print(f"Error: {e}")
    return None

with open('youtube.m3u', 'w', encoding='utf-8') as f:
    f.write('#EXTM3U\n')
    stream_url = get_stream_url()
    if stream_url:
        f.write('#EXTINF:-1 group-title="News", France 24 Live\n')
        f.write(f'{stream_url}\n')
    else:
        f.write('#EXTINF:-1 group-title="News", France 24 (Offline)\n')
        f.write('https://example.com/offline.m3u8\n')

if 'temp.txt' in os.listdir():
    os.remove('temp.txt')

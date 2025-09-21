import yt_dlp
import os

# Only channel - change URL if needed
CHANNEL_URL = "https://www.youtube.com/@AlMayadeenNews"

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

# Create the file
with open('youtube.m3u', 'w', encoding='utf-8') as f:
    f.write('#EXTM3U\n')
    stream_url = get_stream_url()
    if stream_url:
        f.write('#EXTINF:-1 group-title="AlMayadeen", AlMayadeen TV\n')
        f.write(f'{stream_url}\n')
    else:
        # If no live stream
        f.write('#EXTINF:-1 group-title="AlMayadeen", AlMayadeen (Offline)\n')
        f.write('https://example.com/offline.m3u8\n')

# cleanup
if 'temp.txt' in os.listdir():
    os.remove('temp.txt')

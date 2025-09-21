import yt_dlp
import os
import concurrent.futures

def get_stream_url(channel_info):
    name, url = channel_info
    try:
        ydl_opts = {
            'quiet': True,
            'extract_flat': 'in_playlist',
            'live_from_start': True,
            'no_warnings': True,
            'socket_timeout': 10,
            'extractor_args': {'youtube': {'skip': ['dash', 'hls']}}
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            if info and info.get('is_live'):
                return f'#EXTINF:-1 group-title="Live", {name}\n{info["url"]}'
    except:
        pass
    return None

# Read channels
channels = []
try:
    with open('./YouTubeLink.txt', 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f.readlines() if line.strip() and not line.startswith('#')]
        
        i = 0
        while i < len(lines) - 1:
            if not lines[i].startswith('http') and lines[i+1].startswith('http'):
                channels.append((lines[i], lines[i+1]))
                i += 2
            else:
                i += 1
except:
    channels = []

# Process channels in parallel for speed
results = []
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
    results = list(executor.map(get_stream_url, channels))

# Write results
with open('youtube.m3u', 'w', encoding='utf-8') as f:
    f.write('#EXTM3U\n')
    for result in results:
        if result:
            f.write(result + '\n')

# Cleanup
for temp_file in ['temp.txt', 'watch']:
    if temp_file in os.listdir():
        os.remove(temp_file)

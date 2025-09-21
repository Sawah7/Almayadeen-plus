import requests
import os

def grab(url):
    try:
        response = requests.get(url, timeout=15).text
        if '.m3u8' not in response:
            return None
        end = response.find('.m3u8') + 5
        tuner = 100
        while True:
            if 'https://' in response[end - tuner: end]:
                link = response[end - tuner: end]
                start = link.find('https://')
                end = link.find('.m3u8') + 5
                return link[start: end]
            else:
                tuner += 5
    except:
        return None

# افتح الملف للكتابة من البداية (ينشئه إذا لم يكن موجوداً)
with open('youtube.m3u', 'w', encoding='utf-8') as out_file:
    out_file.write('#EXTM3U\n')  # اكتب السطر الأول
    
    try:
        with open('./YouTubeLink.txt', encoding='utf-8') as in_file:
            for line in in_file:
                line = line.strip()
                if not line or line.startswith('##'):
                    continue
                    
                if not line.startswith('https:'):
                    # سطر اسم القناة
                    line_parts = line.split('-')
                    if len(line_parts) >= 2:
                        ch_name = line_parts[0].strip()
                        grp_title = line_parts[1].strip().title()
                        out_file.write(f'\n#EXTINF:-1 group-title="{grp_title}", {ch_name}\n')
                else:
                    # سطر الرابط
                    stream_url = grab(line)
                    if stream_url:
                        out_file.write(stream_url + '\n')
                        
    except FileNotFoundError:
        print("File YouTubeLink.txt not found")

# التنظيف
if 'temp.txt' in os.listdir():
    os.system('rm temp.txt')
if 'watch' in os.listdir():
    os.system('rm watch*')

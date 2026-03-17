import requests
import re

PAGE_URL = "https://www.sanmarinortv.sm/programmi/web-tv-sport"

headers = {
    "User-Agent": "Mozilla/5.0"
}

r = requests.get(PAGE_URL, headers=headers)

match = re.search(r'https://smrtvlive\.b-cdn\.net[^"]+playlist\.m3u8', r.text)

if match:
    stream = match.group(0)

    m3u = f"""#EXTM3U
#EXTINF:-1 tvg-name="San Marino RTV Sport",San Marino RTV Sport
{stream}
"""

    with open("playlist.m3u", "w") as f:
        f.write(m3u)

    print("Playlist updated")
else:
    print("Stream not found")

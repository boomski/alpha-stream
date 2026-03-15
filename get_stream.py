import requests
import re

url = "https://www.alphacyprus.com.cy/live"

headers = {
    "User-Agent": "Mozilla/5.0"
}

r = requests.get(url, headers=headers)

match = re.search(r'https://l4\.cloudskep\.com/alphacyp/acy/playlist\.m3u8\?wmsAuthSign=[^\'"]+', r.text)

if match:
    stream = match.group(0)

    playlist = "#EXTM3U\n#EXTINF:-1,Alpha Cyprus\n" + stream

    with open("alpha.m3u8", "w") as f:
        f.write(playlist)

    print("Playlist gemaakt:", stream)

else:
    print("Stream niet gevonden")

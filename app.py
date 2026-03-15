from flask import Flask, Response
import requests
from urllib.parse import urljoin

app = Flask(__name__)

MASTER_URL = "https://l4.cloudskep.com/alphacyp/acy/playlist.m3u8"

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://www.alphacyprus.com.cy/",
    "Origin": "https://www.alphacyprus.com.cy"
}

QUALITIES = ["fhd", "hd", "sd"]

def get_master():
    r = requests.get(MASTER_URL, headers=HEADERS, timeout=10)
    r.raise_for_status()
    return r.text

def extract_quality(master, quality):
    for line in master.splitlines():
        if f"/{quality}/" in line and "chunks.m3u8" in line:
            return line

def fetch_playlist(url):
    r = requests.get(url, headers=HEADERS, timeout=10)
    r.raise_for_status()
    return r.text

def rewrite_playlist(content, base_url):
    base = base_url.rsplit("/",1)[0] + "/"
    lines = []
    for line in content.splitlines():
        if line.startswith("#") or line.strip() == "":
            lines.append(line)
        else:
            lines.append(urljoin(base, line))
    return "\n".join(lines)

@app.route("/")
def home():
    return "Stream proxy running"

@app.route("/live/<quality>.m3u8")
def live_quality(quality):
    if quality not in QUALITIES:
        return "Quality not available", 404
    master = get_master()
    stream_url = extract_quality(master, quality)
    playlist = fetch_playlist(stream_url)
    fixed = rewrite_playlist(playlist, stream_url)
    return Response(fixed, mimetype="application/vnd.apple.mpegurl")

@app.route("/iptv.m3u")
def iptv_playlist():
    lines = ["#EXTM3U"]
    for q in QUALITIES:
        lines.append(f"#EXTINF:-1,Alpha Cyprus {q.upper()}")
        lines.append(f"/live/{q}.m3u8")
    return Response("\n".join(lines), mimetype="application/vnd.apple.mpegurl")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

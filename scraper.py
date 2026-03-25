import requests
import re
import datetime

# List of source M3U playlists
SOURCES = [
    "https://raw.githubusercontent.com/abusaeeidx/Mrgify-BDIX-IPTV/main/playlist.m3u",
    "https://raw.githubusercontent.com/FunctionError/PiratesTv/main/combined_playlist.m3u"
]

def fetch_playlist(url):
    try:
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            return response.text
        else:
            print(f"Failed to fetch {url}: Status {response.status_code}")
            return None
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

def parse_m3u(content):
    channels = []
    # Simple regex to extract #EXTINF and the following URL
    # This handles most common M3U formats
    pattern = re.compile(r'(#EXTINF:.*?\n)(https?://[^\s\n]+)', re.DOTALL)
    matches = pattern.findall(content)
    for extinf, url in matches:
        channels.append((extinf.strip(), url.strip()))
    return channels

def main():
    all_channels = []
    seen_urls = set()

    for source in SOURCES:
        print(f"Processing source: {source}")
        content = fetch_playlist(source)
        if content:
            channels = parse_m3u(content)
            for extinf, url in channels:
                if url not in seen_urls:
                    all_channels.append((extinf, url))
                    seen_urls.add(url)
    
    # Generate the combined playlist
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    header = f"""#EXTM3U
#=================================
# NEPAL IPTV AUTO-UPDATED PLAYLIST
# Last Updated: {timestamp}
# Sources: {', '.join(SOURCES)}
#==================================
"""
    
    with open("nepal_iptv.m3u", "w", encoding="utf-8") as f:
        f.write(header)
        for extinf, url in all_channels:
            f.write(f"{extinf}\n{url}\n")
            
    print(f"Successfully generated nepal_iptv.m3u with {len(all_channels)} channels.")

if __name__ == "__main__":
    main()

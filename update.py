import re
import requests

# ਤੇਰੇ ਚੈਨਲਾਂ ਦੇ MPD ਲਿੰਕਸ ਦੀ ਸੂਚੀ
channels = [
    {"name": "Zee Bihar Jharkhand", "mpd": "https://d1g8wgjurz8via.cloudfront.net/bpk-tv/Zeebiharjharkhand/default/manifest.mpd"},
    {"name": "Zee Kannada", "mpd": "https://d1g8wgjurz8via.cloudfront.net/bpk-tv/Zeekannada/default/manifest.mpd"},
    {"name": "Zee TV", "mpd": "https://d1g8wgjurz8via.cloudfront.net/bpk-tv/Zeetv/default/manifest.mpd"},
    {"name": "Zee Cinema", "mpd": "https://d1g8wgjurz8via.cloudfront.net/bpk-tv/Zeecinema/default/manifest.mpd"},
    {"name": "Zee Bollywood", "mpd": "https://d1g8wgjurz8via.cloudfront.net/bpk-tv/Zeebollywood/default/manifest.mpd"},
    {"name": "Zee Anmol", "mpd": "https://d1g8wgjurz8via.cloudfront.net/bpk-tv/Zeeanmol/default/manifest.mpd"},
    {"name": "Zee Anmol Cinema", "mpd": "https://d1g8wgjurz8via.cloudfront.net/bpk-tv/Zeeanmolcinema/default/manifest.mpd"},
    {"name": "Discovery Kids", "mpd": "https://d1g8wgjurz8via.cloudfront.net/bpk-tv/Discoverykids2/default/manifest.mpd"},
    {"name": "And TV", "mpd": "https://d1g8wgjurz8via.cloudfront.net/bpk-tv/Andtv/default/manifest.mpd"},
    {"name": "And Pictures", "mpd": "https://d1g8wgjurz8via.cloudfront.net/bpk-tv/Andpictures/default/manifest.mpd"}
]

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Referer': 'https://allinonereborn2.online/zee5/'
}

m3u_content = "#EXTM3U\n\n"

for ch in channels:
    player_url = f"https://allinonereborn2.online/zee5/player.php?mpd={requests.utils.quote(ch['mpd'], safe='')}"
    keyid = "ed068cf84f0640ccbc7c0e395c0a272e" # ਡਿਫਾਲਟ ਬੈਕਅੱਪ ਕੀ
    key = "bb722190f2bb446391020411a7d0828b"
    
    try:
        res = requests.get(player_url, headers=headers, timeout=5)
        ki_match = re.search(r'key[iI][dD]["\']?\s*[:=]\s*["\']([a-fA-F0-9]{32})["\']', res.text)
        k_match = re.search(r'\bkey["\']?\s*[:=]\s*["\']([a-fA-F0-9]{32})["\']', res.text)
        
        if ki_match: keyid = ki_match.group(1)
        if k_match: key = k_match.group(1)
    except:
        pass
        
    m3u_content += f'#EXTINF:-1 tvg-name="{ch["name"]}" group-title="ZEE5",{ch["name"]}\n'
    m3u_content += '#KODIPROP:inputstream.adaptive.manifest_type=mpd\n'
    m3u_content += '#KODIPROP:inputstream.adaptive.license_type=clearkey\n'
    m3u_content += f'#KODIPROP:inputstream.adaptive.license_key={keyid}:{key}\n'
    m3u_content += f'{ch["mpd"]}\n\n'

with open('zee5_auto.m3u', 'w', encoding='utf-8') as f:
    f.write(m3u_content)

print("M3U file generated successfully!")

import requests
import re

json_url = "https://allinonereborn2.online/sony/sliv3.json"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0",
    "Referer": "https://allinonereborn2.online/",
    "Accept": "*/*"
}

try:
    print("ਸਾਰੇ ਚੈਨਲਾਂ ਦੇ ਤਾਜ਼ਾ ਲਿੰਕ ਅਤੇ ਟੋਕਨ ਫ਼ੈਚ ਕੀਤੇ ਜਾ ਰਹੇ ਨੇ...")
    res = requests.get(json_url, headers=headers, timeout=10)

    if res.status_code == 200:
        data = res.json()
        m3u_data = "#EXTM3U\n\n"
        count = 0

        for ch_id, ch_info in data.items():
            title = ch_info.get("title", ch_id.upper())
            playlist_url = ch_info.get("m3u8", "")

            if playlist_url:
                try:
                    sub_res = requests.get(playlist_url, headers=headers, timeout=5)
                    if sub_res.status_code == 200:
                        lines = sub_res.text.splitlines()
                        highest_res_link = ""

                        for line in lines:
                            if line.startswith("http") and ".m3u8" in line:
                                highest_res_link = line

                        if highest_res_link:
                            m3u_data += f'#EXTINF:-1,{title}\n{highest_res_link}\n\n'
                            count += 1
                except Exception as inner_e:
                    print(f"{title} ਦਾ ਲਿੰਕ ਕੱਢਣ ਵਿੱਚ ਦਿੱਕਤ: {inner_e}")

        filename = "all_sony_live_tokens.m3u"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(m3u_data)

        print(f"ਕੁੱਲ {count} ਚੈਨਲਾਂ ਦੇ ਤਾਜ਼ਾ ਟੋਕਨ ਵਾਲੇ ਲਿੰਕ ਸਫਲਤਾਪੂਰਵਕ ਅੱਪਡੇਟ ਹੋ ਗਏ ਨੇ!")

    else:
        print(f"ਮੇਨ JSON ਫ਼ਾਈਲ ਨਹੀਂ ਖੁੱਲ੍ਹੀ, ਸਟੇਟਸ ਕੋਡ: {res.status_code}")
except Exception as e:
    print(f"ਗ਼ਲਤੀ ਆ ਗਈ: {e}")

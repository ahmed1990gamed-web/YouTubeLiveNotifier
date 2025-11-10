import os
import requests
import json

# === إعدادات ===
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "8520079699:AAF6b1k6j5YUEFAsNqLdPQul1wlWKmSBbJQ")
CHAT_ID = os.getenv("CHAT_ID", "1083934764")
API_KEY = os.getenv("YOUTUBE_API_KEY", "AIzaSyDUBMZZu5MBWqwSq3IoYHfZcfbgYYPwcTw")

# قائمة الكلمات المفتاحية للبحث
KEYWORDS = [
    "Fox and Friends",
    "Gutfeld",
    "FOX NEWS",
    "Jesse Watters Primetime",
    "Jesse Watters Primetim",
    "Fox & Friends",
    "Fox&Friends",
    "ᗷᖇEᗩKIᑎG ᑎEᗯS TᖇUᗰᑭ",
    "the five"
]

SENT_FILE = "sent_ids.txt"

# تحميل IDs السابقة
if os.path.exists(SENT_FILE):
    with open(SENT_FILE, "r") as f:
        sent_ids = set(f.read().splitlines())
else:
    sent_ids = set()

new_ids = set()

for KEYWORD in KEYWORDS:
    # البحث عن البث المباشر
    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "part": "snippet",
        "q": KEYWORD,
        "type": "video",
        "eventType": "live",
        "maxResults": 5,
        "key": API_KEY
    }

    response = requests.get(url, params=params)
    data = response.json()

    for item in data.get("items", []):
        video_id = item["id"]["videoId"]
        title = item["snippet"]["title"]
        link = f"https://www.youtube.com/watch?v={video_id}"
        
        if video_id not in sent_ids:
            message = f"🚨 بدأ بث مباشر!\n\nالكلمة المفتاحية: {KEYWORD}\nالعنوان: {title}\nالرابط: {link}"
            requests.get(
                f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
                params={"chat_id": CHAT_ID, "text": message}
            )
            new_ids.add(video_id)

# تحديث IDs المرسلة
if new_ids:
    with open(SENT_FILE, "a") as f:
        for vid in new_ids:
            f.write(vid + "\n")

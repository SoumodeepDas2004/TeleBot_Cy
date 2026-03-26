import requests
import time
from dotenv import load_dotenv
#from xcollector import fetch_tweets
import os
from rsscollector import fetch_rss


load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = "@cyintel01"

seen_urls = set()   # ✅ move to top

def send_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text
    }
    requests.post(url, json=payload)

def classify_threat(text):
    text = text.lower()
    
    if any(k in text for k in ["missile", "airstrike", "drone", "army", "troops"]):
        return "MILITARY"
    
    if any(k in text for k in ["cyber", "ransomware", "breach", "hack"]):
        return "CYBER"
    
    return "GENERAL"

def detect_country(text):
    text = text.lower()
    
    if "india" in text:
        return "India"
    if "usa" in text or "america" in text:
        return "USA"
    if "russia" in text:
        return "Russia"
    if "ukraine" in text:
        return "Ukraine"
    
    return "Global"

# def run_bot():
#     #tweets = fetch_tweets()
#     tweets = fetch_rss()
#     for t in tweets:
#         if t["url"] in seen_urls:
#             continue
        
#         seen_urls.add(t["url"])

#         threat_type = classify_threat(t['text'])
#         country = detect_country(t['text'])
        
#         message = f"""🚨 {threat_type} ALERT [{country}]

#         {t['text']}

#         🔗 {t['url']}"""
        
#     send_message(message)

def run_bot():
    tweets = fetch_rss()
    
    print("TOTAL FETCHED:", len(tweets))  # debug

    count = 0   # track how many sent
    
    for t in tweets:
        if t["url"] in seen_urls:
            continue
        
        seen_urls.add(t["url"])

        threat_type = classify_threat(t['text'])
        country = detect_country(t['text'])
        # if not is_relevant(t["text"]):
        #     continue

        message = f"""🚨 {threat_type} ALERT [{country}]

        {t['text'][:300]}

        🔗 {t['url']}"""
        
        send_message(message)
        count += 1
        if count >= 5:
            break
        time.sleep(2)

    print("SENT:", count)
KEYWORDS = [
    "war", "missile", "attack",
    "airstrike", "conflict", "military"
]
def is_relevant(text):return any(k in text.lower() for k in KEYWORDS)
        

#  MAIN LOOP (OUTSIDE FUNCTION)
while True:
    try:
        print("Fetching intelligence...")
        run_bot()
    except Exception as e:
        print("ERROR:", e)
    
    for _ in range(7200):
        time.sleep(1)
    
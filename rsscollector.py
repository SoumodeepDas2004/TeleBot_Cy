import feedparser

RSS_FEEDS = [
    "http://feeds.bbci.co.uk/news/world/rss.xml",
    "https://rss.nytimes.com/services/xml/rss/nyt/World.xml",
    "https://www.aljazeera.com/xml/rss/all.xml"
]
def fetch_rss():   # keep same name
    posts = []

    for url in RSS_FEEDS:
        feed = feedparser.parse(url)
        print("COLLECTING RSS FEED")
        for entry in feed.entries[:5]:
            text = entry.title
            
            posts.append({
                "text": text,
                "url": entry.link
            })
    print(posts)
    return posts[:10]
KEYWORDS = [
    "war", "missile", "attack",
    "airstrike", "conflict", "military"
]

def is_relevant(text):
    return any(k in text.lower() for k in KEYWORDS)
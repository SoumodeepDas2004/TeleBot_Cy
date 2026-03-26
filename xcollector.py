#xcollector.py
import snscrape.modules.twitter as sntwitter

def fetch_tweets():
    query = "war OR airstrike OR missile OR conflict OR invasion OR drone attack OR cyberattack OR ransomware"
    
    tweets = []
    
    for tweet in sntwitter.TwitterSearchScraper(query).get_items():
        text = tweet.content
        
        if len(text) < 50:
            continue
        
        tweets.append({
            "text": text,
            "url": tweet.url
        })
        
        if len(tweets) >= 5:
            break
    
    return tweets
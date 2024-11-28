import requests
import json
import datetime
import time
import schedule

# --- Data Sources ---

def get_threatpost_news(limit=1):
    """Scrapes recent news from Threatpost."""
    try:
        url = "https://threatpost.com/"
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes

        from bs4 import BeautifulSoup
        soup = BeautifulSoup(response.content, "html.parser")

        articles = []
        for article in soup.find_all("article", limit=limit):  # Limit the number of articles
            headline = article.find("h2").text.strip()
            link = article.find("a")["href"]
            articles.append({"title": headline, "link": link, "source": "Threatpost"})
        return articles

    except requests.exceptions.RequestException as e:
        print(f"Error fetching Threatpost news: {e}")
        return []

def get_hackernews_news(limit=1):
    """Fetches top stories from Hacker News API."""
    try:
        url = "https://hacker-news.firebaseio.com/v0/topstories.json"
        response = requests.get(url)
        response.raise_for_status()
        top_story_ids = response.json()[:limit]  # Limit the number of stories

        articles = []
        for story_id in top_story_ids:
            story_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
            story_response = requests.get(story_url)
            story_response.raise_for_status()
            story_data = story_response.json()
            if "title" in story_data and "url" in story_data:  # Check if title and url exist
                articles.append({"title": story_data["title"], "link": story_data["url"], "source": "Hacker News"})
        return articles

    except requests.exceptions.RequestException as e:
        print(f"Error fetching Hacker News: {e}")
        return []



# --- Output and Scheduling ---

def display_news(articles):
    """Displays news in the console."""
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"Cybersecurity News - {now}\n")
    for article in articles:
        print(f"[{article['source']}] {article['title']}: {article['link']}\n")

def save_news_to_file(articles, filename="cybersecurity_news.txt"):
    """Saves news to a file."""
    try:
        with open(filename, "a", encoding="utf-8") as f:  # Append to file
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"Cybersecurity News - {now}\n")
            for article in articles:
                f.write(f"[{article['source']}] {article['title']}: {article['link']}\n\n")

    except Exception as e:
        print(f"Error saving news to file: {e}")



def fetch_and_display_news():
    """Fetches news from all sources and displays/saves them."""
    all_articles = get_threatpost_news() + get_hackernews_news() #+ get_thehackernews_news()
    display_news(all_articles)
    save_news_to_file(all_articles)



# --- Scheduling (Optional) ---
# Uncomment to enable scheduling:
#schedule.every().day.at("09:00").do(fetch_and_display_news)  # Run at 9:00 AM every day

# while True:
#     schedule.run_pending()
#     time.sleep(60)  # Check every 60 seconds


# Run once immediately:
fetch_and_display_news()
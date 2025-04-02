import google.generativeai as genai
import requests
import feedparser
from bs4 import BeautifulSoup
import time
import json
import os
from config import GOOGLE_API_KEY, CACHE_EXPIRY

genai.configure(api_key=GOOGLE_API_KEY)

# Cache file path
CACHE_FILE = "news_cache.json"

# Google News RSS Feed for Indian Legal News
INDIAN_LEGAL_NEWS_FEED = "https://news.google.com/rss/search?q=legal+India"

def load_cache():
    """Load news cache from file."""
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as file:
            cache_data = json.load(file)
            if time.time() - cache_data["timestamp"] < CACHE_EXPIRY:
                return cache_data["news"]
    return None

def save_cache(news_articles):
    """Save news articles to cache."""
    cache_data = {"timestamp": time.time(), "news": news_articles}
    with open(CACHE_FILE, "w") as file:
        json.dump(cache_data, file)

def fetch_google_news():
    """Fetch legal news from Google News RSS feed."""
    try:
        feed = feedparser.parse(INDIAN_LEGAL_NEWS_FEED)
        articles = []
        for entry in feed.entries[:5]:
            articles.append({
                "title": entry.title,
                "content": entry.summary,
                "link": entry.link
            })
        return articles
    except Exception as e:
        print(f"Error fetching Google News: {e}")
        return []

def scrape_livelaw():
    """Scrape latest legal news from LiveLaw (https://www.livelaw.in/)."""
    try:
        url = "https://www.livelaw.in/"
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, "html.parser")

        articles = []
        for item in soup.find_all("div", class_="news-card")[:5]:
            title = item.find("h2").text.strip()
            link = item.find("a")["href"]
            summary = item.find("div", class_="news-card-content").text.strip()
            articles.append({"title": title, "content": summary, "link": link})

        return articles
    except Exception as e:
        print(f"Error scraping LiveLaw: {e}")
        return []

def scrape_bar_and_bench():
    """Scrape latest legal news from Bar & Bench (https://www.barandbench.com/)."""
    try:
        url = "https://www.barandbench.com/"
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, "html.parser")

        articles = []
        for item in soup.find_all("div", class_="article-listing")[:5]:
            title = item.find("h3").text.strip()
            link = item.find("a")["href"]
            summary = item.find("p").text.strip()
            articles.append({"title": title, "content": summary, "link": "https://www.barandbench.com" + link})

        return articles
    except Exception as e:
        print(f"Error scraping Bar & Bench: {e}")
        return []

def scrape_the_hindu():
    """Scrape latest legal news from The Hindu (https://www.thehindu.com/)."""
    try:
        url = "https://www.thehindu.com/news/national/"
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, "html.parser")

        articles = []
        for item in soup.find_all("div", class_="story-card")[:5]:
            title = item.find("h2").text.strip()
            link = item.find("a")["href"]
            summary = item.find("p").text.strip() if item.find("p") else "No summary available."
            articles.append({"title": title, "content": summary, "link": link})

        return articles
    except Exception as e:
        print(f"Error scraping The Hindu: {e}")
        return []

def summarize_news(articles):
    """Use Gemini AI to summarize news articles."""
    summaries = []
    for article in articles:
        try:
            prompt = f"Summarize this legal news article:\n{article['content']}"
            summary = genai.generate_text(prompt=prompt).text
            summaries.append({"title": article["title"], "summary": summary, "link": article["link"]})
        except Exception as e:
            print(f"Error summarizing news: {e}")
            summaries.append({"title": article["title"], "summary": "Error in AI summarization.", "link": article["link"]})
    
    return summaries

def get_indian_legal_news():
    """Fetch and summarize legal news from multiple sources, using caching."""
    cached_news = load_cache()
    if cached_news:
        return cached_news

    news_articles = (
        fetch_google_news() +
        scrape_livelaw() +
        scrape_bar_and_bench() +
        scrape_the_hindu()
    )
    summarized_news = summarize_news(news_articles)

    save_cache(summarized_news)
    return summarized_news

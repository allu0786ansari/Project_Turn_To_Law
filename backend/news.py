import google.generativeai as genai
import requests
import feedparser
from bs4 import BeautifulSoup
import time
import json
import os
from concurrent.futures import ThreadPoolExecutor
from config import GOOGLE_API_KEY, CACHE_EXPIRY

genai.configure(api_key=GOOGLE_API_KEY)

# Cache file path
CACHE_FILE = "news_cache.json"

# Google News RSS Feed for Indian Legal News
INDIAN_LEGAL_NEWS_FEED = "https://news.google.com/rss/search?q=legal+India"

# List of scraping sources
SCRAPING_SOURCES = [
    {
        "name": "LiveLaw",
        "url": "https://www.livelaw.in/",
        "article_selector": "div.news-card",
        "title_selector": "h2",
        "link_selector": "a",
        "summary_selector": "div.news-card-content",
        "base_url": "",
    },
    {
        "name": "Bar & Bench",
        "url": "https://www.barandbench.com/",
        "article_selector": "div.article-listing",
        "title_selector": "h3",
        "link_selector": "a",
        "summary_selector": "p",
        "base_url": "https://www.barandbench.com",
    },
    {
        "name": "The Hindu",
        "url": "https://www.thehindu.com/news/national/",
        "article_selector": "div.story-card",
        "title_selector": "h2",
        "link_selector": "a",
        "summary_selector": "p",
        "base_url": "",
    },
]


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


def scrape_source(source):
    """Scrape a single news source."""
    try:
        response = requests.get(source["url"], timeout=5)
        soup = BeautifulSoup(response.text, "html.parser")

        articles = []
        for item in soup.find_all(source["article_selector"])[:5]:
            title = item.find(source["title_selector"]).text.strip()
            link = item.find(source["link_selector"])["href"]
            summary = item.find(source["summary_selector"]).text.strip() if item.find(source["summary_selector"]) else "No summary available."
            full_link = source["base_url"] + link if source["base_url"] else link
            articles.append({"title": title, "content": summary, "link": full_link})

        return articles
    except Exception as e:
        print(f"Error scraping {source['name']}: {e}")
        return []


def scrape_all_sources():
    """Scrape all configured news sources."""
    articles = []
    with ThreadPoolExecutor() as executor:
        results = executor.map(scrape_source, SCRAPING_SOURCES)
        for result in results:
            articles.extend(result)
    return articles


def summarize_news(articles):
    """Use Gemini AI to summarize news articles."""
    summaries = []
    for article in articles:
        try:
            prompt = f"Summarize this legal news article:\n{article['content']}"
            response = genai.generate_text(prompt=prompt)
            summary = response.text if response and hasattr(response, "text") else "No summary available."
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

    news_articles = fetch_google_news() + scrape_all_sources()
    summarized_news = summarize_news(news_articles)

    save_cache(summarized_news)
    return summarized_news

import google.generativeai as genai
import requests
import feedparser
from bs4 import BeautifulSoup
import time
import json
import os
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse, urljoin
import re

# Constants
CACHE_FILE = "news_cache.json"
CACHE_EXPIRY = 3600  # 1 hour
DEFAULT_NEWS_COUNT = 5
REQUEST_DELAY = 1

# Configure Gemini AI
try:
    from config import GOOGLE_API_KEY
    genai.configure(api_key=GOOGLE_API_KEY)
    llm_model = genai.GenerativeModel('gemini-1.5-pro')
    print("Gemini AI configured successfully")
except Exception as e:
    print(f"Error configuring Gemini AI: {e}")
    exit(1)

def clean_html_content(html_content: str) -> str:
    """Clean HTML content and extract plain text."""
    if not html_content:
        return ""
    
    # Remove HTML tags using BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')
    # Get text content
    text = soup.get_text(separator=' ', strip=True)
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def fetch_legal_news():
    """Fetch news from multiple sources."""
    news_sources = [
        "https://news.google.com/rss/search?q=india+supreme+court+law",
        "https://news.google.com/rss/search?q=india+legal+news",
    ]
    
    articles = []
    for source in news_sources:
        try:
            feed = feedparser.parse(source)
            for entry in feed.entries[:10]:  # Get top 10 from each source
                # Clean the title and summary
                clean_title = clean_html_content(entry.title)
                clean_summary = clean_html_content(entry.summary)
                
                # Extract source from title if present
                title_parts = clean_title.split(' - ')
                main_title = title_parts[0]
                source = title_parts[-1] if len(title_parts) > 1 else "Unknown Source"
                
                articles.append({
                    "title": main_title,
                    "link": entry.link,
                    "snippet": clean_summary,
                    "source": source
                })
        except Exception as e:
            print(f"Error fetching from {source}: {e}")
    
    return articles

def summarize_article(title: str, content: str) -> str:
    """Summarize article content using Gemini AI."""
    try:
        # Use the article's summary if available
        if len(content) > 100:  # If we have a decent length summary
            return content
            
        prompt = f"""
        Summarize this legal news article in 2-3 sentences:
        Title: {title}
        Content: {content[:4000]}
        """
        response = llm_model.generate_content(prompt)
        return response.text.strip() if response else content
    except Exception as e:
        print(f"Summarization error for '{title}': {e}")
        # Return the original content if summarization fails
        return content[:500] + "..."  # Truncate long content

def get_indian_legal_news(keywords: list[str] | None = None) -> list[dict]:
    """Get legal news with optional keyword filtering."""
    try:
        # Check cache first if no keywords
        if not keywords and os.path.exists(CACHE_FILE):
            with open(CACHE_FILE, 'r', encoding='utf-8') as f:
                cache = json.load(f)
                if time.time() - cache.get('timestamp', 0) < CACHE_EXPIRY:
                    return cache['articles']

        articles = fetch_legal_news()
        if not articles:
            print("No articles found")
            return []

        # Filter by keywords if provided
        if keywords and any(keywords):
            filtered_articles = []
            for article in articles:
                if any(keyword.lower() in article['title'].lower() or 
                      keyword.lower() in article['snippet'].lower() 
                      for keyword in keywords):
                    filtered_articles.append(article)
            articles = filtered_articles

        # Process and format articles
        processed_articles = []
        for article in articles[:DEFAULT_NEWS_COUNT]:
            formatted_article = {
                "title": article['title'],
                "summary": article['snippet'],
                "link": article['link'],
                "source": article['source']
            }
            processed_articles.append(formatted_article)

        # Cache results if no keywords were used
        if not keywords:
            with open(CACHE_FILE, 'w', encoding='utf-8') as f:
                json.dump({
                    'timestamp': time.time(),
                    'articles': processed_articles
                }, f, ensure_ascii=False, indent=2)

        return processed_articles

    except Exception as e:
        print(f"Error in get_indian_legal_news: {e}")
        return []

import google.generativeai as genai
import requests
import feedparser
from bs4 import BeautifulSoup
import time
import json
import os
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse, urljoin
from urllib import robotparser
import re  # For keyword filtering

# --- Configuration & Initialization ---
try:
    from config import GOOGLE_API_KEY, CACHE_EXPIRY
except ImportError:
    print("Error: config.py not found or missing GOOGLE_API_KEY/CACHE_EXPIRY.")
    print("Please create config.py with your GOOGLE_API_KEY and CACHE_EXPIRY (in seconds).")
    exit(1)

try:
    genai.configure(api_key=GOOGLE_API_KEY)
    llm_model = genai.GenerativeModel('gemini-pro')
    print("Gemini API configured successfully.")
except Exception as e:
    print(f"Error configuring Gemini API: {e}")
    exit(1)

# Cache file path
CACHE_FILE = "news_cache.json"

# News Sources Configuration
INDIAN_LEGAL_NEWS_FEED = "https://news.google.com/rss/search?q=legal+India+law"

SCRAPING_SOURCES = [
    {
        "name": "LiveLaw",
        "url": "https://www.livelaw.in/top-stories",
        "article_selector": "div.news-card-container",
        "title_selector": "h2 > a",
        "link_selector": "h2 > a",
        "summary_selector": "div.news-card-content-container > p",
        "base_url": "https://www.livelaw.in",
    },
    {
        "name": "Bar & Bench",
        "url": "https://www.barandbench.com/news",
        "article_selector": "div.article-card",
        "title_selector": "h3 > a",
        "link_selector": "h3 > a",
        "summary_selector": "p.article-excerpt",
        "base_url": "https://www.barandbench.com",
    },
]

# Constants
REQUEST_DELAY_SECONDS = 1.5
FETCH_TIMEOUT_SECONDS = 20
MAX_ARTICLES_PER_SOURCE = 7
MAX_ARTICLES_TO_PROCESS = 10
MAX_CONTENT_LENGTH_FOR_SUMMARY = 15000

robot_parsers = {}

# --- Caching Functions ---
def load_cache():
    """Load news cache from file if it exists and hasn't expired."""
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, "r", encoding='utf-8') as file:
                cache_data = json.load(file)
                if isinstance(cache_data, dict) and "timestamp" in cache_data and "news" in cache_data:
                    if (time.time() - cache_data["timestamp"]) < CACHE_EXPIRY:
                        print("[Cache] Loading news from valid cache.")
                        return cache_data["news"]
                    else:
                        print("[Cache] Cache expired.")
        except (json.JSONDecodeError, IOError) as e:
            print(f"[Cache] Error loading cache file: {e}")
    else:
        print("[Cache] Cache file not found.")
    return None

def save_cache(news_articles):
    """Save news articles to the cache file."""
    cache_data = {"timestamp": time.time(), "news": news_articles}
    try:
        with open(CACHE_FILE, "w", encoding='utf-8') as file:
            json.dump(cache_data, file, indent=2)
        print(f"[Cache] Saved {len(news_articles)} summarized articles to cache.")
    except IOError as e:
        print(f"[Cache] Error saving cache file: {e}")

# --- robots.txt Checker ---
def can_fetch(url: str) -> bool:
    """Checks robots.txt for the given URL."""
    parsed_url = urlparse(url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
    robots_url = urljoin(base_url, "/robots.txt")

    parser = robot_parsers.get(base_url)
    if not parser:
        parser = robotparser.RobotFileParser()
        parser.set_url(robots_url)
        try:
            print(f"  [Robots] Reading robots.txt for {base_url}")
            parser.read()
            robot_parsers[base_url] = parser
            time.sleep(0.5)
        except Exception as e:
            print(f"  [Robots] Warning: Could not read robots.txt from {robots_url}: {e}")
            return True

    user_agent = "*"
    return parser.can_fetch(user_agent, url)

# --- News Fetching Functions ---
def fetch_google_news():
    """Fetch initial news list (title, link, snippet) from Google News RSS."""
    print("[Fetch] Fetching news from Google News RSS...")
    articles = []
    try:
        feed = feedparser.parse(INDIAN_LEGAL_NEWS_FEED)
        if feed.bozo:
            print(f"  Warning: Feedparser reported issues parsing the feed: {feed.bozo_exception}")

        for entry in feed.entries[:MAX_ARTICLES_PER_SOURCE]:
            articles.append({
                "title": entry.title,
                "link": entry.link,
                "snippet": entry.summary,
                "source": "Google News RSS"
            })
        print(f"  Fetched {len(articles)} initial articles from Google News RSS.")
    except Exception as e:
        print(f"  Error fetching or parsing Google News RSS: {e}")
    return articles

def scrape_source(source_config):
    """Scrape a single news source for initial list (title, link, snippet)."""
    name = source_config["name"]
    url = source_config["url"]
    print(f"[Fetch] Scraping initial list from {name} ({url})...")
    articles = []
    try:
        response = requests.get(url, timeout=FETCH_TIMEOUT_SECONDS, headers={'User-Agent': 'Mozilla/5.0'})
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        items = soup.select(source_config["article_selector"])
        count = 0
        for item in items:
            if count >= MAX_ARTICLES_PER_SOURCE:
                break

            try:
                title_element = item.select_one(source_config["title_selector"])
                link_element = item.select_one(source_config["link_selector"])
                summary_element = item.select_one(source_config["summary_selector"])

                if title_element and link_element and link_element.has_attr('href'):
                    title = title_element.text.strip()
                    raw_link = link_element["href"]
                    full_link = urljoin(source_config.get("base_url", url), raw_link).split('#')[0]
                    snippet = summary_element.text.strip() if summary_element else "No snippet found."

                    articles.append({
                        "title": title,
                        "link": full_link,
                        "snippet": snippet,
                        "source": name
                    })
                    count += 1
            except Exception as e:
                print(f"    Warning: Error processing an item from {name}: {e}")
                continue

        print(f"  Scraped {len(articles)} initial articles from {name}.")
    except requests.exceptions.RequestException as e:
        print(f"  Error scraping {name}: {e}")
    except Exception as e:
        print(f"  Unexpected error during scraping {name}: {e}")

    return articles

def scrape_all_sources_concurrently():
    """Scrape all configured sources concurrently for initial lists."""
    articles = []
    with ThreadPoolExecutor(max_workers=len(SCRAPING_SOURCES)) as executor:
        results = executor.map(scrape_source, SCRAPING_SOURCES)
        for result in results:
            articles.extend(result)
    return articles

def filter_articles_by_keywords(articles: list[dict], keywords: list[str] | None) -> list[dict]:
    """
    Filters articles based on the provided keywords.

    Args:
        articles (list[dict]): List of articles to filter.
        keywords (list[str] | None): List of keywords to filter by.

    Returns:
        list[dict]: Filtered list of articles.
    """
    if not keywords:
        return articles

    print(f"[Filter] Filtering articles by keywords: {keywords}")
    filtered_articles = []
    for article in articles:
        title = article.get("title", "").lower()
        snippet = article.get("snippet", "").lower()
        if any(keyword.lower() in title or keyword.lower() in snippet for keyword in keywords):
            filtered_articles.append(article)

    print(f"[Filter] Found {len(filtered_articles)} articles matching keywords.")
    return filtered_articles

def summarize_article_content(title: str, content: str, link: str) -> dict:
    """
    Summarizes the content of an article using Gemini AI.

    Args:
        title (str): The title of the article.
        content (str): The full content of the article.
        link (str): The URL of the article.

    Returns:
        dict: A dictionary containing the title, summary, and link.
    """
    print(f"[Summarize] Summarizing article: {title}")
    try:
        # Ensure content length is within the allowed limit
        if len(content) > MAX_CONTENT_LENGTH_FOR_SUMMARY:
            print(f"  [Summarize] Content too long, truncating to {MAX_CONTENT_LENGTH_FOR_SUMMARY} characters.")
            content = content[:MAX_CONTENT_LENGTH_FOR_SUMMARY]

        # Prepare the prompt for Gemini AI
        prompt = f"""
        Summarize the following legal news article in a concise and clear manner:

        Title: {title}

        Content:
        {content}

        Provide a summary that highlights the key points.
        """

        # Call the Gemini AI API
        response = llm_model.generate_content(prompt)
        if response and hasattr(response, "text"):
            summary = response.text.strip()
            print(f"  [Summarize] Summary generated successfully for: {title}")
            return {
                "title": title,
                "summary": summary,
                "link": link,
            }
        else:
            print(f"  [Summarize] No summary generated for: {title}")
            return {
                "title": title,
                "summary": "Summary not available. Please read the full article.",
                "link": link,
            }
    except Exception as e:
        print(f"  [Summarize] Error summarizing article '{title}': {e}")
        return {
            "title": title,
            "summary": "Summary not available due to an error. Please read the full article.",
            "link": link,
        }

def fetch_and_extract_content(url: str) -> str:
    """
    Fetch content from a URL and extract meaningful text.

    Args:
        url (str): The URL of the article.

    Returns:
        str: The extracted content, or None if extraction fails.
    """
    print(f"[Fetch] Fetching content from: {url}")
    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=FETCH_TIMEOUT_SECONDS)
        response.raise_for_status()

        if "html" not in response.headers.get("Content-Type", "").lower():
            print("  [Fetch] Skipping non-HTML content.")
            return None

        soup = BeautifulSoup(response.content, "html.parser")
        content_selectors = ["main", "article", "[role='main']", ".content", ".entry-content"]
        text_content = ""

        # Try extracting content using predefined selectors
        for selector in content_selectors:
            element = soup.select_one(selector)
            if element:
                text_content = element.get_text(separator=" ", strip=True)
                break

        # Fallback: Extract content from the <body> tag if no selectors match
        if not text_content:
            body = soup.find("body")
            if body:
                text_content = body.get_text(separator=" ", strip=True)

        # Clean and return the extracted content
        cleaned_text = " ".join(text_content.split())
        return cleaned_text[:MAX_CONTENT_LENGTH_FOR_SUMMARY] if cleaned_text else None
    except Exception as e:
        print(f"  [Fetch] Error fetching content from {url}: {e}")
        return None


def get_indian_legal_news(keywords: list[str] | None = None) -> list[dict]:
    """
    Fetches, filters (optional), gets full content, and summarizes legal news.
    By default, displays the top 5 or 10 news articles with their titles, summaries, and "Read More" links.
    Uses caching only when no keywords are provided.

    Args:
        keywords (list[str] | None): Optional list of keywords to filter news.

    Returns:
        list[dict]: List of summarized news articles (dict with title, summary, link).
    """
    try:
        print("\n--- Starting Legal News Update ---")
        if keywords:
            print(f"Keyword filter applied: {keywords}")
            cached_news = None
        else:
            print("No keyword filter. Checking cache for general news...")
            cached_news = load_cache()

        if cached_news is not None:
            print("[Cache] Returning cached news.")
            return cached_news[:10]  # Return top 10 cached articles by default

        # Fetch initial articles from Google News and other sources
        initial_articles = fetch_google_news()
        initial_articles.extend(scrape_all_sources_concurrently())

        if not initial_articles:
            print("[Update] No initial articles found from any source.")
            return []

        # Remove duplicate articles based on their links
        seen_links = set()
        unique_initial_articles = []
        for article in initial_articles:
            link = article.get('link')
            if link and link not in seen_links:
                unique_initial_articles.append(article)
                seen_links.add(link)
        print(f"[Update] Found {len(unique_initial_articles)} unique initial articles.")

        # Filter articles based on keywords (if provided)
        articles_to_process = filter_articles_by_keywords(unique_initial_articles, keywords)
        articles_to_process = articles_to_process[:MAX_ARTICLES_TO_PROCESS]  # Limit to max articles
        print(f"[Update] Will attempt to fully process up to {len(articles_to_process)} articles.")

        # Summarize articles
        final_summaries = []
        for article in articles_to_process:
            link = article.get("link")
            title = article.get("title", "No Title")

            if not link:
                print(f"  Skipping article with no link: {title}")
                continue

            full_content = fetch_and_extract_content(link)
            if full_content:
                summary_result = summarize_article_content(title, full_content, link)
                if summary_result:
                    final_summaries.append(summary_result)
            else:
                print(f"  Skipping summarization for '{title}' due to content fetch failure.")

            time.sleep(REQUEST_DELAY_SECONDS)

        # Cache the results if no keywords are provided
        if not keywords and final_summaries:
            save_cache(final_summaries)

        # Return the top 5 or 10 articles
        print(f"\n--- Legal News Update Complete ---")
        print(f"Returning {len(final_summaries[:10])} summarized articles.")
        return final_summaries[:10]  # Return top 10 articles by default
    except Exception as e:
        print(f"Error in get_indian_legal_news: {e}")
        return []
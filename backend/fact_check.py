import requests
from bs4 import BeautifulSoup
import google.generativeai as genai
import os
import json
from urllib.parse import urlparse, parse_qs, unquote
import time

# --- Configuration ---

# Set up the Google API key for Gemini AI
try:
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise KeyError("GOOGLE_API_KEY environment variable not set.")
    genai.configure(api_key=api_key)
    llm_model = genai.GenerativeModel("gemini-1.5-pro")
    print("Gemini API configured successfully.")
except KeyError as e:
    print(f"ERROR: {e}")
    exit(1)
except Exception as e:
    print(f"Error configuring Gemini API: {e}")
    exit(1)

# List of authoritative legal sources
LEGAL_SOURCES = [
    "indiankanoon.org",
    "main.sci.gov.in",
    "prsindia.org",
    "legislative.gov.in",
    "lawmin.gov.in",
]

# Headers for web scraping
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
}

# Constants
REQUEST_DELAY_SECONDS = 2
MAX_RESULTS_PER_SOURCE = 2
MAX_CONTENT_LENGTH = 8000
FETCH_TIMEOUT_SECONDS = 15

# --- Helper Functions ---

def search_duckduckgo(query: str, max_results: int = MAX_RESULTS_PER_SOURCE) -> dict:
    """
    Search authoritative legal websites using DuckDuckGo and extract URLs.
    """
    results = {}
    print(f"[Search] Searching DuckDuckGo for: '{query}'")

    for source in LEGAL_SOURCES:
        search_query = f"site:{source} {query}"
        url = f"https://html.duckduckgo.com/html/?q={search_query}"
        print(f"  Querying: {url}")

        try:
            response = requests.get(url, headers=HEADERS, timeout=FETCH_TIMEOUT_SECONDS)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")
            links = soup.find_all("a", class_="result__a", href=True)

            valid_links = []
            for link in links:
                raw_href = link["href"]
                if "duckduckgo.com/y.js" in raw_href:
                    parsed_url = urlparse(raw_href)
                    query_params = parse_qs(parsed_url.query)
                    if "uddg" in query_params:
                        href = unquote(query_params["uddg"][0])
                        if source in urlparse(href).netloc:
                            valid_links.append(href)
                            if len(valid_links) >= max_results:
                                break
            if valid_links:
                results[source] = valid_links
            time.sleep(REQUEST_DELAY_SECONDS)
        except Exception as e:
            print(f"  Error searching {source}: {e}")
            results[source] = [f"Error: {e}"]

    return results

def fetch_and_extract_content(url: str) -> str:
    """
    Fetch content from a URL and extract meaningful text.
    """
    print(f"[Fetch] Fetching content from: {url}")
    try:
        response = requests.get(url, headers=HEADERS, timeout=FETCH_TIMEOUT_SECONDS)
        response.raise_for_status()

        if "html" not in response.headers.get("Content-Type", "").lower():
            print("  Skipping non-HTML content.")
            return None

        soup = BeautifulSoup(response.content, "html.parser")
        content_selectors = ["main", "article", "[role='main']", ".content", ".entry-content"]
        text_content = ""

        for selector in content_selectors:
            element = soup.select_one(selector)
            if element:
                text_content = element.get_text(separator=" ", strip=True)
                break

        if not text_content:
            body = soup.find("body")
            if body:
                text_content = body.get_text(separator=" ", strip=True)

        cleaned_text = " ".join(text_content.split())
        return cleaned_text[:MAX_CONTENT_LENGTH] if cleaned_text else None
    except Exception as e:
        print(f"  Error fetching content from {url}: {e}")
        return None

def analyze_claim_with_llm(claim: str, source_text: str, source_url: str) -> dict:
    """
    Analyze the claim against the source text using Gemini AI.
    """
    print(f"[Analyze] Analyzing claim with content from {source_url}")
    prompt = f"""
    Analyze the following legal claim against the provided source text.

    Claim: "{claim}"

    Source Text:
    {source_text}

    Instructions:
    - Determine if the source text supports, contradicts, or is irrelevant to the claim.
    - Provide a JSON response with the following keys:
      - "status": One of ["Supports", "Contradicts", "Irrelevant"].
      - "reasoning": A brief explanation.
      - "quote": A direct quote from the source text (if applicable).
    """

    try:
        response = llm_model.generate_content(prompt)
        response_text = response.text.strip()

        if response_text.startswith("```json"):
            response_text = response_text[7:].strip()
        if response_text.endswith("```"):
            response_text = response_text[:-3].strip()

        return json.loads(response_text)
    except Exception as e:
        print(f"  Error analyzing claim: {e}")
        return {
            "status": "Error",
            "reasoning": f"Failed to analyze claim: {e}",
            "quote": "",
            "source_url": source_url,
        }

# --- Main Function ---

def fact_check_legal_claim(claim: str) -> dict:
    """
    Fact-check a legal claim by searching authoritative sources and analyzing content.
    """
    print(f"\n[FactCheck] Starting fact-check for claim: '{claim}'")
    sources = search_duckduckgo(claim)
    results = []

    for source, urls in sources.items():
        if isinstance(urls, list) and not urls[0].startswith("Error"):
            for url in urls:
                content = fetch_and_extract_content(url)
                if content:
                    analysis = analyze_claim_with_llm(claim, content, url)
                    results.append(analysis)
                else:
                    results.append({
                        "status": "Error",
                        "reasoning": "Failed to fetch or extract content.",
                        "quote": "",
                        "source_url": url,
                    })

    summary = {
        "supports": sum(1 for r in results if r.get("status") == "Supports"),
        "contradicts": sum(1 for r in results if r.get("status") == "Contradicts"),
        "irrelevant": sum(1 for r in results if r.get("status") == "Irrelevant"),
        "errors": sum(1 for r in results if r.get("status") == "Error"),
    }

    return {
        "claim": claim,
        "results": results,
        "summary": summary,
    }

# --- Example Usage ---
'''if __name__ == "__main__":
    test_claim = "Is Section 124A of the Indian Penal Code related to sedition?"
    result = fact_check_legal_claim(test_claim)
    print(json.dumps(result, indent=2)) 
'''
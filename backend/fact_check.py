import requests
from bs4 import BeautifulSoup
from fastapi import HTTPException
from urllib.parse import quote

LEGAL_SOURCES = [
    "indiankanoon.org",
    "legalaffairs.gov.in",
    "lawmin.gov.in",
]

GOOGLE_SEARCH_URL = "https://www.google.com/search?q="

def search_legal_sources(query: str, max_results: int = 3) -> dict:
    """Search authoritative legal websites using Google."""
    results = {}
    encoded_query = quote(query)

    for source in LEGAL_SOURCES:
        search_url = f"{GOOGLE_SEARCH_URL}site:{source} {encoded_query}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }

        try:
            response = requests.get(search_url, headers=headers, timeout=5)
            if response.status_code != 200:
                continue

            soup = BeautifulSoup(response.text, "html.parser")
            links = soup.find_all("a", href=True)

            valid_links = []
            for link in links:
                href = link["href"]
                if "url?q=" in href and source in href:
                    url = href.split("url?q=")[1].split("&")[0]
                    valid_links.append(url)

            results[source] = valid_links[:max_results] if valid_links else ["No relevant links found."]
        except requests.RequestException:
            continue

    return results if results else {"error": "No legal sources found."}


def fact_check_legal_claim(claim: str) -> dict:
    """Fact-check a legal claim using Google search on trusted sources."""
    try:
        sources = search_legal_sources(claim)
        return {
            "claim": claim,
            "verified_sources": sources
        }
    except HTTPException as e:
        return {"error": e.detail}

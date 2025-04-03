import requests
from bs4 import BeautifulSoup
from fastapi import HTTPException

# List of authoritative legal sources
LEGAL_SOURCES = [
    "indiankanoon.org",
    "legalaffairs.gov.in",
    "lawmin.gov.in",
]

# Headers for HTTP requests to mimic a browser
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

def search_legal_sources(query: str, max_results: int = 3) -> dict:
    """
    Search authoritative legal websites using DuckDuckGo and scrape results.

    Args:
        query (str): The legal claim or query to search for.
        max_results (int): Maximum number of results to return per source.

    Returns:
        dict: A dictionary containing the source and its corresponding links.
    """
    results = {}

    for source in LEGAL_SOURCES:
        search_query = f"site:{source} {query}"
        url = f"https://duckduckgo.com/html/?q={search_query}"

        try:
            response = requests.get(url, headers=HEADERS)
            response.raise_for_status()  # Raise an error for HTTP issues

            # Parse the HTML response
            soup = BeautifulSoup(response.text, "html.parser")
            links = soup.find_all("a", class_="result__a", href=True)

            # Extract valid links
            valid_links = []
            for link in links[:max_results]:
                href = link["href"]
                if source in href:
                    valid_links.append(href)

            results[source] = valid_links if valid_links else ["No relevant links found."]
        except requests.exceptions.RequestException as e:
            # Log the exception for debugging purposes
            print(f"Error while searching {source}: {e}")
            results[source] = ["Error occurred while fetching results."]
        except Exception as e:
            print(f"Unexpected error while processing {source}: {e}")
            results[source] = ["Unexpected error occurred."]

    return results if results else {"error": "No legal sources found."}


def fact_check_legal_claim(claim: str) -> dict:
    """
    Fact-check a legal claim using reliable legal sources.

    Args:
        claim (str): The legal claim to verify.

    Returns:
        dict: A dictionary containing the claim and verified sources.
    """
    try:
        sources = search_legal_sources(claim)
        if "error" in sources:
            return {"error": sources["error"]}

        # Add a confidence score based on the number of valid links found
        confidence_score = sum(len(links) for links in sources.values() if isinstance(links, list))
        return {
            "claim": claim,
            "verified_sources": sources,
            "confidence_score": confidence_score,  # Confidence score based on results
        }
    except Exception as e:
        # Catch unexpected errors and log them
        print(f"Unexpected error during fact-checking: {e}")
        return {"error": "An unexpected error occurred while fact-checking the claim."}

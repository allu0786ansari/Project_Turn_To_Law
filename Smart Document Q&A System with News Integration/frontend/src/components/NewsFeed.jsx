import { useEffect, useState, useCallback, useMemo } from "react";
import { getNewsFeed } from "../api";
import "../styles/NewsFeed.css";
import debounce from "lodash.debounce";

const NewsFeed = () => {
  const [news, setNews] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [keywords, setKeywords] = useState("");

  // Memoize the fetchNews function to prevent unnecessary recreations
  const fetchNews = useCallback(async (searchKeywords = []) => {
    setLoading(true);
    setError(null);
    try {
      const newsData = await getNewsFeed(searchKeywords);
      setNews(Array.isArray(newsData) ? newsData : []);
    } catch (error) {
      console.error("Failed to fetch news:", error);
      setError(error.message || "Failed to fetch legal news. Please try again.");
    } finally {
      setLoading(false);
    }
  }, []);

  // Create a stable debounced function using useMemo
  const debouncedFetchNews = useMemo(
    () =>
      debounce((searchKeywords) => {
        fetchNews(searchKeywords);
      }, 500),
    [fetchNews]
  );

  // Cleanup debounce on unmount
  useEffect(() => {
    return () => {
      debouncedFetchNews.cancel();
    };
  }, [debouncedFetchNews]);

  // Handle keyword search with proper dependency tracking
  const handleSearch = useCallback(() => {
    if (!keywords.trim()) {
      fetchNews([]); // Fetch all news if keywords are empty
      return;
    }
    const keywordArray = keywords
      .split(",")
      .map((kw) => kw.trim())
      .filter(Boolean); // Remove empty strings
    debouncedFetchNews(keywordArray);
  }, [keywords, debouncedFetchNews, fetchNews]);

  // Auto-search when keywords change
  useEffect(() => {
    handleSearch();
  }, [handleSearch]);

  // Initial fetch
  useEffect(() => {
    fetchNews();
    return () => setNews([]); // Cleanup on unmount
  }, [fetchNews]);

  return (
    <div className="news-feed-container">
      <h2 className="news-feed-title">Latest Legal News</h2>

      <div className="news-feed-search">
        <input
          type="text"
          value={keywords}
          onChange={(e) => setKeywords(e.target.value)}
          placeholder="Enter keywords (e.g., Supreme Court, IPC)"
          className="news-feed-input"
          aria-label="Keyword search input"
        />
        <button 
          onClick={handleSearch} 
          className="news-feed-button" 
          aria-label="Search news"
          disabled={loading}
        >
          {loading ? "Searching..." : "Search"}
        </button>
      </div>

      {loading && <p className="news-feed-loading">Loading news...</p>}

      {error && (
        <p className="news-feed-error" role="alert">
          {error}
        </p>
      )}

      {!loading && !error && news.length === 0 && (
        <p className="news-feed-empty" role="status">
          No news articles available at the moment.
        </p>
      )}

      {!loading && !error && news.length > 0 && (
        <div className="news-articles-container">
          {news.map((article, idx) => (
            <div key={article.link || idx} className="news-article">
              <h3 className="news-article-title">{article.title}</h3>
              <p className="news-article-summary">{article.summary}</p>
              <a
                href={article.link}
                className="news-article-link"
                target="_blank"
                rel="noopener noreferrer"
                aria-label={`Read more about ${article.title}`}
              >
                Read more
              </a>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default NewsFeed;

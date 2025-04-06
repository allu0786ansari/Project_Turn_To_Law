import { useEffect, useState, useCallback, useMemo } from "react";
import { getNewsFeed } from "../api";
import "../styles/NewsFeed.css";
import debounce from "lodash.debounce";

// Separate NewsArticle component for better organization
const NewsArticle = ({ article }) => (
  <div className="news-article">
    <h3 className="news-article-title">{article.title}</h3>
    {article.source && <p className="news-article-source">{article.source}</p>}
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
);

const NewsFeed = () => {
  const [news, setNews] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [keywords, setKeywords] = useState("");

  const fetchNews = useCallback(async (searchKeywords = []) => {
    setLoading(true);
    setError(null);
    try {
      const newsData = await getNewsFeed(searchKeywords);
      if (Array.isArray(newsData)) {
        setNews(newsData);
      } else {
        console.warn("Invalid news data format:", newsData);
        setNews([]);
      }
    } catch (error) {
      console.error("Failed to fetch news:", error);
      setError(error.message || "Failed to fetch legal news. Please try again.");
    } finally {
      setLoading(false);
    }
  }, []);

  const debouncedFetchNews = useMemo(
    () =>
      debounce((searchKeywords) => {
        fetchNews(searchKeywords);
      }, 800), // Increased debounce delay for better performance
    [fetchNews]
  );

  useEffect(() => {
    return () => {
      debouncedFetchNews.cancel();
    };
  }, [debouncedFetchNews]);

  const handleSearch = useCallback(() => {
    const trimmedKeywords = keywords.trim();
    if (!trimmedKeywords) {
      fetchNews([]); // Fetch all news if keywords are empty
      return;
    }
    const keywordArray = trimmedKeywords
      .split(",")
      .map((kw) => kw.trim())
      .filter(Boolean);
    
    console.log("Searching with keywords:", keywordArray);
    debouncedFetchNews(keywordArray);
  }, [keywords, debouncedFetchNews, fetchNews]);

  // Handle keyword changes
  const handleKeywordChange = (e) => {
    setKeywords(e.target.value);
  };

  // Handle Enter key press
  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleSearch();
    }
  };

  useEffect(() => {
    handleSearch();
  }, [handleSearch]);

  useEffect(() => {
    fetchNews();
    return () => setNews([]);
  }, [fetchNews]);

  return (
    <div className="news-feed-container">
      <h2 className="news-feed-title">Latest Legal News</h2>

      <div className="news-feed-search">
        <input
          type="text"
          value={keywords}
          onChange={handleKeywordChange}
          onKeyPress={handleKeyPress}
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

      {loading && (
        <p className="news-feed-loading" role="status">
          Loading news...
        </p>
      )}

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
          {news.map((article) => (
            <NewsArticle 
              key={article.link || article.title} 
              article={article} 
            />
          ))}
        </div>
      )}
    </div>
  );
};

export default NewsFeed;

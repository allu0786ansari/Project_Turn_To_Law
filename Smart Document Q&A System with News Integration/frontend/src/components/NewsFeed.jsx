import { useEffect, useState, useCallback } from "react";
import { getNewsFeed } from "../api"; // Import the API function
import "../styles/NewsFeed.css";
import debounce from "lodash.debounce";

const NewsFeed = () => {
  const [news, setNews] = useState([]); // State to store news articles
  const [loading, setLoading] = useState(true); // Track loading state
  const [error, setError] = useState(null); // Track error state
  const [keywords, setKeywords] = useState(""); // State to store user-provided keywords

  // Fetch news articles from the backend
  const fetchNews = async (keywords = []) => {
    setLoading(true);
    setError(null); // Reset error state
    try {
      const newsData = await getNewsFeed(keywords); // Call the API function with keywords
      setNews(newsData);
    } catch (error) {
      console.error("Failed to fetch news:", error);
      setError(error.message || "Failed to fetch legal news. Please try again.");
    } finally {
      setLoading(false); // Reset loading state
    }
  };

  // Stable debounce function
  const debouncedFetchNews = useCallback(
    debounce((keywords) => {
      fetchNews(keywords);
    }, 500), // 500ms debounce delay
    [] // Empty dependency array ensures this function is stable
  );

  // Handle keyword search
  const handleSearch = useCallback(() => {
    const keywordArray = keywords.split(",").map((kw) => kw.trim()); // Split keywords by commas
    debouncedFetchNews(keywordArray); // Use the stable debounced function
  }, [keywords, debouncedFetchNews]); // Include dependencies

  // Fetch news on component mount
  useEffect(() => {
    fetchNews(); // Fetch all news by default
  }, []); // Empty dependency array ensures this runs only once on mount

  return (
    <div className="news-feed-container">
      <h2 className="news-feed-title">Latest Legal News</h2>

      {/* Keyword Search */}
      <div className="news-feed-search">
        <input
          type="text"
          value={keywords}
          onChange={(e) => setKeywords(e.target.value)}
          placeholder="Enter keywords (e.g., Supreme Court, IPC)"
          className="news-feed-input"
          aria-label="Keyword search input"
        />
        <button onClick={handleSearch} className="news-feed-button" aria-label="Search news">
          Search
        </button>
      </div>

      {/* Loading State */}
      {loading && <p className="news-feed-loading">Loading news...</p>}

      {/* Error State */}
      {error && <p className="news-feed-error">{error}</p>}

      {/* Empty State */}
      {!loading && !error && news.length === 0 && (
        <p className="news-feed-empty">No news articles available at the moment.</p>
      )}

      {/* News Articles */}
      {!loading &&
        !error &&
        news.map((article, idx) => (
          <div key={idx} className="news-article">
            <h3 className="news-article-title">{article.title}</h3>
            <p className="news-article-summary">{article.summary}</p>
            <a
              href={article.link}
              className="news-article-link"
              target="_blank"
              rel="noopener noreferrer"
            >
              Read more
            </a>
          </div>
        ))}
    </div>
  );
};

export default NewsFeed;
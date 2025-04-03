import { useEffect, useState } from "react";
import { getNewsFeed } from "../api"; // Import the API function
import "../styles/NewsFeed.css";

const NewsFeed = () => {
  const [news, setNews] = useState([]); // State to store news articles
  const [loading, setLoading] = useState(true); // Track loading state
  const [error, setError] = useState(null); // Track error state

  useEffect(() => {
    const fetchNews = async () => {
      try {
        const newsData = await getNewsFeed(); // Call the API function
        setNews(newsData);
      } catch (error) {
        console.error("Failed to fetch news:", error);
        setError("Failed to fetch legal news. Please try again later.");
      } finally {
        setLoading(false); // Reset loading state
      }
    };

    fetchNews();
  }, []);

  return (
    <div className="news-feed-container">
      <h2 className="news-feed-title">Latest Legal News</h2>

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
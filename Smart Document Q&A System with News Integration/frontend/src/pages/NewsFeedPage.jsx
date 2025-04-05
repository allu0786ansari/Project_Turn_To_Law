import NewsFeed from "../components/NewsFeed";
import "../styles/NewsFeed.css"; // Add a CSS file for page-specific styling

const NewsFeedPage = () => {
  return (
    <div className="news-feed-page-container p-4">
      <h1 className="news-feed-page-title">Latest Legal News</h1>
      <p className="news-feed-page-description">
        Stay updated with the latest legal news and developments from trusted sources.
      </p>
      <NewsFeed />
    </div>
  );
};

export default NewsFeedPage;

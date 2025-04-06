import NewsFeed from "../components/NewsFeed";
import "../styles/NewsFeed.css"; // Add a CSS file for page-specific styling

const NewsFeedPage = () => {
  return (
    <div className="news-feed-page-container p-4">
      
      <NewsFeed />
    </div>
  );
};

export default NewsFeedPage;

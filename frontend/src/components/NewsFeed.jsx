import { useEffect, useState } from "react";
import axios from "../api";
import '../styles/NewsFeed.css';

const NewsFeed = () => {
  const [news, setNews] = useState([]);

  useEffect(() => {
    const fetchNews = async () => {
      try {
        const res = await axios.get("/news");
        setNews(res.data);
      } catch (error) {
        console.error("Failed to fetch news", error);
      }
    };
    fetchNews();
  }, []);

  return (
    <div className="p-4">
      <h2 className="text-xl font-bold mb-4">Legal News</h2>
      {news.map((article, idx) => (
        <div key={idx} className="mb-4 p-3 border rounded">
          <h3 className="font-bold">{article.title}</h3>
          <p>{article.summary}</p>
          <a href={article.link} className="text-blue-600" target="_blank">Read more</a>
        </div>
      ))}
    </div>
  );
};

export default NewsFeed;

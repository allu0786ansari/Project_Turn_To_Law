import { Link } from "react-router-dom";
import '../styles/NavBar.css';

const Navbar = () => {
  return (
    <nav className="bg-blue-600 p-4 text-white flex justify-between">
      <h1 className="text-lg font-bold">Smart Legal Q&A</h1>
      <div>
        <Link className="px-4" to="/">Home</Link>
        <Link className="px-4" to="/newsfeed">Newsfeed</Link>
        <Link className="px-4" to="/about">About</Link>
      </div>
    </nav>
  );
};

export default Navbar;

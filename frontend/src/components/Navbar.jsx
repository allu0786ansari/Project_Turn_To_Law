import { NavLink } from "react-router-dom";
import "../styles/NavBar.css";

const Navbar = () => {
  return (
    <nav className="navbar">
      <h1 className="navbar-title">Smart Legal Q&A</h1>
      <div className="navbar-links">
        <NavLink
          to="/"
          className={({ isActive }) => (isActive ? "active-link navbar-link" : "navbar-link")}
          aria-label="Home"
        >
          Home
        </NavLink>
        <NavLink
          to="/newsfeed"
          className={({ isActive }) => (isActive ? "active-link navbar-link" : "navbar-link")}
          aria-label="Newsfeed"
        >
          Newsfeed
        </NavLink>
        <NavLink
          to="/about"
          className={({ isActive }) => (isActive ? "active-link navbar-link" : "navbar-link")}
          aria-label="About"
        >
          About
        </NavLink>
      </div>
    </nav>
  );
};

export default Navbar;

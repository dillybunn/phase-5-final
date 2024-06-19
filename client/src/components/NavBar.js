import React from "react";
import { Link } from "react-router-dom";

function NavBar({ userId }) {
  return (
    <nav>
      <ul>
        <li>
          <Link to="/">Home</Link>
        </li>
        {userId && (
          <>
            <li>
              <Link to="/users">Users</Link>
            </li>
            <li>
              <Link to="/sales_calls">Sales Calls</Link>
            </li>
            <li>
              <Link to="/ratings">Ratings</Link>
            </li>
            <li>
              <Link to="/stages">Stages</Link>
            </li>
            <li>
              <Link to="/opportunities">Opportunities</Link>
            </li>
          </>
        )}
        {!userId && (
          <li>
            <Link to="/login">Login</Link>
          </li>
        )}
      </ul>
    </nav>
  );
}

export default NavBar;

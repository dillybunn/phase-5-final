import React from "react";

function Home({ userId }) {
  return (
    <div>
      <h2>Welcome, User {userId}!</h2>
      <p>Use the navigation bar to access different sections of the app.</p>
    </div>
  );
}

export default Home;

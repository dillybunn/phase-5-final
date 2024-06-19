import React, { useState } from "react";

function LogIn({ setUserId }) {
  const [username, setUsername] = useState("");

  const handleLogin = () => {
    // Mock login function
    if (username) {
      setUserId(username);
    }
  };

  return (
    <div>
      <h2>Login</h2>
      <input
        type="text"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
        placeholder="Username"
      />
      <button onClick={handleLogin}>Log In</button>
    </div>
  );
}

export default LogIn;

import React, { useState } from "react";
import { useHistory } from "react-router-dom";
import { useAppContext } from "./AppContext";

function LogIn() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const { setUserId } = useAppContext();
  const history = useHistory();

  const handleLogIn = (e) => {
    e.preventDefault();

    fetch("http://localhost:5555/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ username, password }),
      credentials: "include",
    })
      .then((r) => r.json())
      .then((data) => {
        if (data.id) {
          setUserId(data.id);
          history.push("/dashboard");
        } else {
          alert("Login failed");
        }
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  };

  return (
    <form onSubmit={handleLogIn}>
      <input
        type="text"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
        placeholder="Username"
      />
      <input
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        placeholder="Password"
      />
      <button type="submit">Log In</button>
    </form>
  );
}

export default LogIn;

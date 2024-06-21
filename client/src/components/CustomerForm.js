import React, { useState } from "react";
import { useAppContext } from "./AppContext";

function CustomerForm({ onAddCustomer }) {
  const { userId } = useAppContext();
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();

    console.log("Form Data:", { name, email, user_id: userId });

    fetch("http://localhost:5555/customers", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      credentials: "include",
      body: JSON.stringify({
        name,
        email,
        user_id: userId,
      }),
    })
      .then((r) => r.json())
      .then((newCustomer) => {
        onAddCustomer(newCustomer);
        setName("");
        setEmail("");
      })
      .catch((error) => console.error("Error:", error));
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        value={name}
        onChange={(e) => setName(e.target.value)}
        placeholder="Name"
      />
      <input
        type="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        placeholder="Email"
      />
      <button type="submit">Add Customer</button>
    </form>
  );
}

export default CustomerForm;

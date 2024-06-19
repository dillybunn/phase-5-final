import React, { useEffect, useState } from "react";

function SalesCalls({ userId }) {
  const [salesCalls, setSalesCalls] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch("http://localhost:5555/sales_calls")
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        return response.json();
      })
      .then((data) => {
        setSalesCalls(data);
        setLoading(false);
      })
      .catch((error) => {
        setError(error);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>Error: {error.message}</div>;
  }

  return (
    <div>
      <h2>Sales Calls</h2>
      <ul>
        {salesCalls.map((call) => (
          <li key={call.id}>
            Date: {call.date}, Notes: {call.notes}, Rating: {call.rating_id},
            Stage: {call.stage_id}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default SalesCalls;

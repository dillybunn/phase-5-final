import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

function CustomerDetails() {
  const { id } = useParams();
  const [customer, setCustomer] = useState(null);
  const [newSalesCall, setNewSalesCall] = useState({
    date: "",
    notes: "",
    rating_id: "",
    stage_id: "",
  });
  const [newOpportunity, setNewOpportunity] = useState({
    description: "",
    sales_call_id: "",
  });
  const [ratings, setRatings] = useState([]);
  const [stages, setStages] = useState([]);
  const [salesCalls, setSalesCalls] = useState([]);

  useEffect(() => {
    fetch(`http://localhost:5555/customers/${id}`, {
      credentials: "include",
    })
      .then((r) => r.json())
      .then((data) => {
        setCustomer(data);
        setSalesCalls(data.sales_calls || []);
      })
      .catch((error) => console.error("Error:", error));
  }, [id]);

  useEffect(() => {
    fetch("http://localhost:5555/ratings", {
      credentials: "include",
    })
      .then((r) => r.json())
      .then((data) => setRatings(data))
      .catch((error) => console.error("Error:", error));

    fetch("http://localhost:5555/stages", {
      credentials: "include",
    })
      .then((r) => r.json())
      .then((data) => setStages(data))
      .catch((error) => console.error("Error:", error));
  }, []);

  const handleInputChange = (e, setter) => {
    const { name, value } = e.target;
    setter((prev) => ({ ...prev, [name]: value }));
  };

  const handleSalesCallSubmit = (e) => {
    e.preventDefault();

    fetch(`http://localhost:5555/sales_calls`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      credentials: "include",
      body: JSON.stringify({
        ...newSalesCall,
        user_id: customer.user.id,
        customer_id: customer.id,
      }),
    })
      .then((r) => {
        if (!r.ok) {
          throw new Error(`Error: ${r.statusText}`);
        }
        return r.json();
      })
      .then((data) => {
        setSalesCalls((prev) => [...prev, data]); // Update salesCalls state
        setNewSalesCall({ date: "", notes: "", rating_id: "", stage_id: "" });
      })
      .catch((error) => console.error("Error:", error));
  };

  const handleOpportunitySubmit = (e) => {
    e.preventDefault();

    if (!newOpportunity.sales_call_id) {
      console.error("sales_call_id is required");
      return;
    }

    fetch(`http://localhost:5555/opportunities`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      credentials: "include",
      body: JSON.stringify({
        ...newOpportunity,
        customer_id: customer.id,
      }),
    })
      .then((r) => {
        if (!r.ok) {
          throw new Error(`Error: ${r.statusText}`);
        }
        return r.json();
      })
      .then((data) => {
        setCustomer((prev) => ({
          ...prev,
          opportunities: [...prev.opportunities, data],
        }));
        setNewOpportunity({ description: "", sales_call_id: "" });
      })
      .catch((error) => console.error("Error:", error));
  };

  if (!customer) {
    return <div>Loading...</div>;
  }

  const opportunities = customer.opportunities || [];

  return (
    <div>
      <h1>Customer Details: {customer.name}</h1>
      <h2>Contact Information</h2>
      <p>Email: {customer.email}</p>

      <h2>Sales Calls</h2>
      <table>
        <thead>
          <tr>
            <th>Date</th>
            <th>Notes</th>
            <th>Rating</th>
            <th>Stage</th>
            {/* <th>Opportunities</th> */}
          </tr>
        </thead>
        <tbody>
          {salesCalls
            .sort((a, b) => new Date(a.date) - new Date(b.date))
            .map((call) => (
              <tr key={call.id}>
                <td>{new Date(call.date).toLocaleDateString()}</td>
                <td>{call.notes}</td>
                <td>{call.rating ? call.rating.value : "N/A"}</td>
                <td>{call.stage ? call.stage.name : "N/A"}</td>
                <td>
                  {/* {call.opportunities && call.opportunities.length > 0 ? (
                    <ul>
                      {call.opportunities.map((op) => (
                        <li key={op.id}>{op.description}</li>
                      ))}
                    </ul>
                  ) : (
                    "N/A"
                  )} */}
                </td>
              </tr>
            ))}
        </tbody>
      </table>

      <h3>Add New Sales Call</h3>
      <form onSubmit={handleSalesCallSubmit}>
        <input
          type="date"
          name="date"
          value={newSalesCall.date}
          onChange={(e) => handleInputChange(e, setNewSalesCall)}
          required
        />
        <input
          type="text"
          name="notes"
          value={newSalesCall.notes}
          onChange={(e) => handleInputChange(e, setNewSalesCall)}
          placeholder="Notes"
          required
        />
        <select
          name="rating_id"
          value={newSalesCall.rating_id}
          onChange={(e) => handleInputChange(e, setNewSalesCall)}
          required
        >
          <option value="">Select Rating</option>
          {ratings.map((rating) => (
            <option key={rating.id} value={rating.id}>
              {rating.value}
            </option>
          ))}
        </select>
        <select
          name="stage_id"
          value={newSalesCall.stage_id}
          onChange={(e) => handleInputChange(e, setNewSalesCall)}
          required
        >
          <option value="">Select Stage</option>
          {stages.map((stage) => (
            <option key={stage.id} value={stage.id}>
              {stage.name}
            </option>
          ))}
        </select>
        <button type="submit">Add Sales Call</button>
      </form>

      <h2>Opportunities</h2>
      <ul>
        {opportunities.map((opportunity) => (
          <li key={opportunity.id}>{opportunity.description}</li>
        ))}
      </ul>

      <h3>Add New Opportunity</h3>
      <form onSubmit={handleOpportunitySubmit}>
        <input
          type="text"
          name="description"
          value={newOpportunity.description}
          onChange={(e) => handleInputChange(e, setNewOpportunity)}
          placeholder="Description"
          required
        />
        <select
          name="sales_call_id"
          value={newOpportunity.sales_call_id}
          onChange={(e) => handleInputChange(e, setNewOpportunity)}
          required
        >
          <option value="">Select Sales Call</option>
          {salesCalls.map((call) => (
            <option key={call.id} value={call.id}>
              {new Date(call.date).toLocaleDateString()} - {call.notes}
            </option>
          ))}
        </select>
        <button type="submit">Add Opportunity</button>
      </form>
    </div>
  );
}

export default CustomerDetails;

import React, { useEffect, useState } from "react";
import { useAppContext } from "./AppContext";
import CustomerForm from "./CustomerForm";
import { Link } from "react-router-dom";

function Dashboard() {
  const { userId } = useAppContext();
  const [customers, setCustomers] = useState([]);

  useEffect(() => {
    if (userId) {
      fetch(`http://localhost:5555/users/${userId}/customers`)
        .then((r) => {
          if (!r.ok) {
            throw new Error("Failed to fetch customers");
          }
          return r.json();
        })
        .then((data) => setCustomers(data))
        .catch((error) => console.error("Error:", error));
    }
  }, [userId]);

  const handleAddCustomer = (newCustomer) => {
    setCustomers([...customers, newCustomer]);
  };

  if (!userId) {
    return <div>Please log in.</div>;
  }

  return (
    <div>
      <h1>Dashboard</h1>
      <h2>Customers</h2>
      <ul>
        {customers.map((customer) => (
          <li key={customer.id}>
            <Link to={`/customers/${customer.id}`}>{customer.name}</Link>
            {/* <ul>
              {customer.sales_calls.map((call) => (
                <li key={call.id}>{call.notes}</li>
              ))}
              {customer.opportunities.map((opportunity) => (
                <li key={opportunity.id}>{opportunity.description}</li>
              ))}
            </ul> */}
          </li>
        ))}
      </ul>
      <CustomerForm onAddCustomer={handleAddCustomer} />
    </div>
  );
}

export default Dashboard;

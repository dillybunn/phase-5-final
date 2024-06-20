// import React, { useEffect, useState } from "react";
// import { useParams } from "react-router-dom";

// function CustomerDetails() {
//   const { customerId } = useParams();
//   const [customer, setCustomer] = useState(null);

//   useEffect(() => {
//     fetch(`http://localhost:5555/customers/${customerId}`)
//       .then((r) => r.json())
//       .then((data) => setCustomer(data))
//       .catch((error) => console.error("Error:", error));
//   }, [customerId]);

//   if (!customer) {
//     return <div>Loading...</div>;
//   }

//   return (
//     <div>
//       <h1>{customer.name}</h1>
//       <p>Email: {customer.email}</p>
//       <h2>Sales Calls</h2>
//       <ul>
//         {customer.sales_calls.map((call) => (
//           <li key={call.id}>{call.notes}</li>
//         ))}
//       </ul>
//       <h2>Opportunities</h2>
//       <ul>
//         {customer.opportunities.map((opportunity) => (
//           <li key={opportunity.id}>{opportunity.description}</li>
//         ))}
//       </ul>
//     </div>
//   );
// }

// export default CustomerDetails;
import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

function CustomerDetails() {
  const { customerId } = useParams();
  const [customer, setCustomer] = useState(null);
  const [isEditing, setIsEditing] = useState(false);
  const [editData, setEditData] = useState({ name: "", email: "" });
  const [editSalesCalls, setEditSalesCalls] = useState([]);
  const [editOpportunities, setEditOpportunities] = useState([]);

  useEffect(() => {
    fetch(`http://localhost:5555/customers/${customerId}`)
      .then((r) => r.json())
      .then((data) => {
        setCustomer(data);
        setEditData({ name: data.name, email: data.email });
        setEditSalesCalls(data.sales_calls);
        setEditOpportunities(data.opportunities);
      })
      .catch((error) => console.error("Error:", error));
  }, [customerId]);

  const handleEditClick = () => {
    setIsEditing(true);
  };

  const handleCancelClick = () => {
    setIsEditing(false);
    setEditData({ name: customer.name, email: customer.email });
    setEditSalesCalls(customer.sales_calls);
    setEditOpportunities(customer.opportunities);
  };

  const handleSaveClick = () => {
    fetch(`http://localhost:5555/customers/${customerId}`, {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(editData),
    })
      .then((r) => r.json())
      .then((updatedCustomer) => {
        setCustomer(updatedCustomer);
        setIsEditing(false);
      })
      .catch((error) => console.error("Error:", error));

    editSalesCalls.forEach((call) => {
      fetch(`http://localhost:5555/sales_calls/${call.id}`, {
        method: "PATCH",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(call),
      }).catch((error) => console.error("Error:", error));
    });

    editOpportunities.forEach((opportunity) => {
      fetch(`http://localhost:5555/opportunities/${opportunity.id}`, {
        method: "PATCH",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(opportunity),
      }).catch((error) => console.error("Error:", error));
    });
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setEditData((prevData) => ({ ...prevData, [name]: value }));
  };

  const handleSalesCallChange = (id, key, value) => {
    setEditSalesCalls((prevSalesCalls) =>
      prevSalesCalls.map((call) =>
        call.id === id ? { ...call, [key]: value } : call
      )
    );
  };

  const handleOpportunityChange = (id, key, value) => {
    setEditOpportunities((prevOpportunities) =>
      prevOpportunities.map((opportunity) =>
        opportunity.id === id ? { ...opportunity, [key]: value } : opportunity
      )
    );
  };

  if (!customer) {
    return <div>Loading...</div>;
  }

  return (
    <div>
      <h1>Customer Details</h1>
      {isEditing ? (
        <div>
          <input
            type="text"
            name="name"
            value={editData.name}
            onChange={handleChange}
          />
          <input
            type="email"
            name="email"
            value={editData.email}
            onChange={handleChange}
          />
          <button onClick={handleSaveClick}>Save</button>
          <button onClick={handleCancelClick}>Cancel</button>
        </div>
      ) : (
        <div>
          <p>Name: {customer.name}</p>
          <p>Email: {customer.email}</p>
          <button onClick={handleEditClick}>Edit</button>
        </div>
      )}
      <h2>Sales Calls</h2>
      <ul>
        {editSalesCalls.map((call) => (
          <li key={call.id}>
            {isEditing ? (
              <input
                type="text"
                value={call.notes}
                onChange={(e) =>
                  handleSalesCallChange(call.id, "notes", e.target.value)
                }
              />
            ) : (
              call.notes
            )}
          </li>
        ))}
      </ul>
      <h2>Opportunities</h2>
      <ul>
        {editOpportunities.map((opportunity) => (
          <li key={opportunity.id}>
            {isEditing ? (
              <input
                type="text"
                value={opportunity.description}
                onChange={(e) =>
                  handleOpportunityChange(
                    opportunity.id,
                    "description",
                    e.target.value
                  )
                }
              />
            ) : (
              opportunity.description
            )}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default CustomerDetails;

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
  const { id } = useParams();
  const [customer, setCustomer] = useState(null);
  const [formData, setFormData] = useState({
    name: "",
    email: "",
  });

  useEffect(() => {
    fetch(`http://localhost:5555/customers/${id}`, {
      credentials: "include",
    })
      .then((r) => r.json())
      .then((data) => {
        setCustomer(data);
        setFormData({
          name: data.name,
          email: data.email,
        });
      })
      .catch((error) => console.error("Error:", error));
  }, [id]);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSaveClick = () => {
    fetch(`http://localhost:5555/customers/${id}`, {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json",
      },
      credentials: "include",
      body: JSON.stringify(formData),
    })
      .then((r) => r.json())
      .then((updatedCustomer) => setCustomer(updatedCustomer))
      .catch((error) => console.error("Error:", error));
  };

  if (!customer) {
    return <div>Loading...</div>;
  }

  return (
    <div>
      <h1>Customer Details</h1>
      <input
        type="text"
        name="name"
        value={formData.name}
        onChange={handleChange}
        placeholder="Name"
      />
      <input
        type="email"
        name="email"
        value={formData.email}
        onChange={handleChange}
        placeholder="Email"
      />
      <button onClick={handleSaveClick}>Save</button>

      <h2>Sales Calls</h2>
      <ul>
        {customer.sales_calls.map((call) => (
          <li key={call.id}>{call.notes}</li>
        ))}
      </ul>

      <h2>Opportunities</h2>
      <ul>
        {customer.opportunities.map((opportunity) => (
          <li key={opportunity.id}>{opportunity.description}</li>
        ))}
      </ul>
    </div>
  );
}

export default CustomerDetails;

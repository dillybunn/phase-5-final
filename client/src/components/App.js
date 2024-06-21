import React from "react";
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";
import { AppProvider } from "./AppContext";
import Dashboard from "./Dashboard";
import Login from "./LogIn";
import CustomerDetails from "./CustomerDetails";

function App() {
  return (
    <AppProvider>
      <Router>
        <Switch>
          <Route path="/login" component={Login} />
          <Route path="/dashboard" component={Dashboard} />
          <Route path="/customers/:id" component={CustomerDetails} />
          <Route path="/" component={Login} />
        </Switch>
      </Router>
    </AppProvider>
  );
}

export default App;

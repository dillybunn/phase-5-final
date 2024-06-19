import React, { useState } from "react";
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";
import NavBar from "./NavBar";
import Users from "./Users";
import SalesCalls from "./SalesCalls";
import Ratings from "./Ratings";
import Stages from "./Stages";
import Opportunities from "./Opportunities";
import Home from "./Home";
import LogIn from "./LogIn";

function App() {
  const [userId, setUserId] = useState("");

  return (
    <Router>
      <NavBar userId={userId} />
      <div className="wrapper">
        <Switch>
          <Route exact path="/">
            {userId ? (
              <Home userId={userId} />
            ) : (
              <LogIn setUserId={setUserId} />
            )}
          </Route>
          <Route exact path="/login">
            <LogIn setUserId={setUserId} />
          </Route>
          <Route exact path="/users">
            {userId ? (
              <Users userId={userId} />
            ) : (
              <LogIn setUserId={setUserId} />
            )}
          </Route>
          <Route exact path="/sales_calls">
            {userId ? (
              <SalesCalls userId={userId} />
            ) : (
              <LogIn setUserId={setUserId} />
            )}
          </Route>
          <Route exact path="/ratings">
            {userId ? (
              <Ratings userId={userId} />
            ) : (
              <LogIn setUserId={setUserId} />
            )}
          </Route>
          <Route exact path="/stages">
            {userId ? (
              <Stages userId={userId} />
            ) : (
              <LogIn setUserId={setUserId} />
            )}
          </Route>
          <Route exact path="/opportunities">
            {userId ? (
              <Opportunities userId={userId} />
            ) : (
              <LogIn setUserId={setUserId} />
            )}
          </Route>
        </Switch>
      </div>
    </Router>
  );
}

export default App;

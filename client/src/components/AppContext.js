import React, { createContext, useState, useContext } from "react";

const AppContext = createContext();

const AppProvider = ({ children }) => {
  const [userId, setUserId] = useState(null);

  return (
    <AppContext.Provider value={{ userId, setUserId }}>
      {children}
    </AppContext.Provider>
  );
};

const useAppContext = () => {
  return useContext(AppContext);
};

export { AppProvider, useAppContext };

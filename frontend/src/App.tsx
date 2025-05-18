import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { useState, useEffect } from "react";
import axios from "axios";

import Home from "./page/Home";
import History from "./page/History";
import Navbar from "./components/Navbar";

export default function App() {
  const fetchAPI = async () => {
    const response = await axios.get("http://localhost:8080/api/users");
    console.log(response.data.user);
  };

  useEffect(() => {
    fetchAPI();
  }, []);

  return (
    <Router>
      <Navbar />
      <div className="pt-16">
        {" "}
        <Routes>
          <Route path="/home" element={<Home />} />
          <Route path="/history" element={<History />} />
        </Routes>
      </div>
    </Router>
  );
}

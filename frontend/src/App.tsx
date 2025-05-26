import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

import Home from "./page/Home";
import History from "./page/History";

export default function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/history" element={<History />} />
      </Routes>
    </Router>
  );
}

import React from 'react';
import './App.css';
import Navbar from './components/Navbar.jsx';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import '@fortawesome/fontawesome-free/css/all.min.css';
import Home from './components/pages/Home.jsx';
import F1 from './components/pages/F1.jsx';
import SignUp from './components/pages/SignUp.jsx';
import Login from './components/pages/Login.jsx';
import Logout from './components/pages/Logout.jsx';
import Submitted from './components/pages/Submitted.jsx';
import Report from './components/pages/Report.jsx';
import ShowReport from './components/pages/ShowReport.jsx';
import Chatbot from './components/pages/Chatbot.jsx';  // Import Chatbot

function App() {
  return (
    <>
      <Router>
        <Navbar />
        <Routes>
          <Route path="/" exact element={<Home />} />
          <Route path="/sign-up" element={<SignUp />} />
          <Route path="/login" element={<Login />} />
          <Route path="/logout" element={<Logout />} />
          <Route path="/form" element={<F1 />} />
          <Route path="/submitted-info" element={<Submitted />} />
          <Route path="/report" element={<Report />} />
          <Route path="/show_report" element={<ShowReport />} />
          <Route path="/chatbot" element={<Chatbot />} /> {/* Add chatbot route */}
        </Routes>
      </Router>
    </>
  );
}

export default App;

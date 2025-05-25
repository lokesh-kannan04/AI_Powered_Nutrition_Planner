import React, { useState } from "react";
import "./Sidebar.css"; // Import the CSS file for styling

function Sidebar() {
  const [isSidebarOpen, setIsSidebarOpen] = useState(false); // State to manage sidebar visibility

  const toggleSidebar = () => {
    setIsSidebarOpen(!isSidebarOpen); // Toggle sidebar visibility
  };

  const closeSidebar = () => {
    setIsSidebarOpen(false);
  };

  return (
    <>
      {/* Menu Text Button */}
      <div className="menu-text" onClick={toggleSidebar}>
        Menu
      </div>

      {/* Sidebar */}
      <div className={`sidebar ${isSidebarOpen ? "open" : ""}`}>
        <h2>Sidebar</h2>
        <ul>
          <li><a href="/">Home</a></li>
          <li><a href="/about">About</a></li>
          <li><a href="/services">Services</a></li>
          <li><a href="/contact">Contact</a></li>
          <li><button onClick={closeSidebar}>Close</button></li>
        </ul>
      </div>
    </>
  );
}

export default Sidebar;

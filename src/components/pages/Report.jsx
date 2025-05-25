import React, { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import './Report.css';
import { useNavigate } from 'react-router-dom'; // Import useNavigate

const Report = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const formData = location.state?.formData || {};
  const [signUpData, setSignUpData] = useState({
    name: '',
    email: '',
    phone: '',
    location: '',
    age: '',
    gender: '',
    height: '',
    weight: '',
    goal: '',
  });
  const [loading, setLoading] = useState(false);

  // Fetch current user's data when the component mounts
  useEffect(() => {
    const fetchCurrentUserData = async () => {
      const session_key = localStorage.getItem("session_key");
      if (!session_key) {
        console.log("Session Key is missing! Please log in again.");
        return;
      }

      try {
        const response = await fetch('http://127.0.0.1:8000/api/get_current_user/', {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'Session-Key': session_key,
          },
          credentials: 'include',  // Include cookies if needed
        });

        const data = await response.json();
        if (response.ok) {
          // Update signUpData with the fetched user data
          setSignUpData({
            name: data.user.name || '',
            email: data.user.email || '',
            phone: data.user.phone || '',
            location: data.user.location || '',
            age: data.user.age || '',
            gender: data.user.gender || '',
            height: data.user.height || '',
            weight: data.user.weight || '',
            goal: data.user.goal || '',
          });
          console.log("Current user's data:", data.user);
        } else {
          console.error(`Error: ${data.message || 'Something went wrong'}`);
        }
      } catch (error) {
        console.error('Fetch error:', error);
      }
    };

    fetchCurrentUserData();
  }, []);

  if (!formData || Object.keys(formData).length === 0) {
    return <h2>No data submitted. Please fill the form first.</h2>;
  }

  console.log(formData);

  // Function to generate and download the report
  const generateReport = () => {
    const reportContent = `
      Nutrition Deficiency Assessment Report
      ------------------------------------

      User Details:
      -------------
      Name: ${signUpData.name || "Not provided"}
      Email: ${signUpData.email || "Not provided"}
      Phone: ${signUpData.phone || "Not provided"}
      Location: ${signUpData.location || "Not provided"}
      Age: ${signUpData.age || "Not provided"}
      Gender: ${signUpData.gender || "Not provided"}
      Height: ${signUpData.height || "Not provided"} cm
      Weight: ${signUpData.weight || "Not provided"} kg
      Goal: ${signUpData.goal || "Not provided"}

      Nutrition Details:
      -----------------
      Dietary Preference: ${formData.dietaryPreference || "Not provided"}
      Medical Conditions: ${formData.medicalConditions || "None"}
      Symptoms: ${formData.symptoms.join(", ") || "No symptoms reported"}
      Food Frequency: ${Object.entries(formData.foodFrequency).map(([food, freq]) => `${food}: ${freq}`).join(", ") || "No food frequency data"}
      Water Intake: ${formData.waterIntake || "Not specified"}
      Allergies: ${formData.allergies || "None"}
      Additional Symptoms: ${formData.extra_symptoms || "None"}
    `;

    const blob = new Blob([reportContent], { type: 'text/plain' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = 'Nutrition_Deficiency_Report.txt';
    link.click();
    URL.revokeObjectURL(link.href);
  };

  // Function to save report data to backend
  const handleSubmit = async () => {
    setLoading(true);

    const session_key = localStorage.getItem("session_key");  
    if (!session_key) {
      alert("Session Key is missing! Please log in again.");
      setLoading(false);
      return;
    }

    const headers = {
      'Content-Type': 'application/json',
      'Session-Key': session_key
    };

    const reportData = {
      user: signUpData,
      nutrition: formData
    };

    try {
      const response = await fetch('http://127.0.0.1:8000/api/submit_assessment/', {
        method: 'POST',
        credentials: "include", 
        headers: headers,
        body: JSON.stringify(reportData),
      });

      const data = await response.json();
      console.log("Response received:", data);

      if (response.ok) {
        alert('Report saved successfully!');
        navigate("/login");
      } else {
        alert(`Error: ${data.message || 'Something went wrong'}`);
      }
    } catch (error) {
      console.error('Fetch error:', error);
      alert('Something went wrong!');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="report-container">
      <h2>Nutrition Deficiency Assessment Report</h2>
      <div className="report-content">
        {/* Display User Details */}
        <div className="report-section">
          <h3>User Details</h3>
          <p><strong>Name:</strong> {signUpData.name || "Not provided"}</p>
          <p><strong>Email:</strong> {signUpData.email || "Not provided"}</p>
          <p><strong>Phone:</strong> {signUpData.phone || "Not provided"}</p>
          <p><strong>Location:</strong> {signUpData.location || "Not provided"}</p>
          <p><strong>Age:</strong> {signUpData.age || "Not provided"}</p>
          <p><strong>Gender:</strong> {signUpData.gender || "Not provided"}</p>
          <p><strong>Height:</strong> {signUpData.height || "Not provided"} cm</p>
          <p><strong>Weight:</strong> {signUpData.weight || "Not provided"} kg</p>
          <p><strong>Goal:</strong> {signUpData.goal || "Not provided"}</p>
        </div>

        {/* Display Nutrition Details */}
        <div className="report-section">
          <h3>Nutrition Details</h3>
          <p><strong>Dietary Preference:</strong> {formData.dietaryPreference || "Not provided"}</p>
          <p><strong>Medical Conditions:</strong> {formData.medicalConditions || "None"}</p>
          <p><strong>Symptoms:</strong> {formData.symptoms.join(", ") || "No symptoms reported"}</p>
          <p><strong>Food Frequency:</strong> {Object.entries(formData.foodFrequency).map(([food, freq]) => `${food}: ${freq}`).join(", ") || "No food frequency data"}</p>
          <p><strong>Water Intake:</strong> {formData.waterIntake || "Not specified"}</p>
          <p><strong>Allergies:</strong> {formData.allergies || "None"}</p>
          <p><strong>Additional Symptoms:</strong> {formData.extra_symptoms || "None"}</p>
        </div>
      </div>

      <div className="report-buttons">
        <button className="download-btn" onClick={generateReport}>Download Report</button>
        <button className="save-btn" onClick={handleSubmit} disabled={loading}>
          {loading ? "Saving..." : "Save My Report"}
        </button>
      </div>
    </div>
  );
};

export default Report;
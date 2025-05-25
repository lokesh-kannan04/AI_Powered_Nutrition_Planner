import React from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import './Submitted.css';

const Submitted = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const formData = location.state?.formData || {};
  const signUpData = location.state?.signUpData || {}; // Retrieve signUpData

  if (!formData || Object.keys(formData).length === 0) {
    return <h2>No data submitted. Please fill the form first.</h2>;
  }

  return (
    <div className='body'>
      <div className="confirmation-container">
        <h2>Submitted Information</h2>
        <div className="summary-card">
          {/* Dietary Preference */}
          <div className="summary-section">
            <h3>Dietary Preference</h3>
            <p>{formData.dietaryPreference || "Not provided"}</p>
          </div>

          {/* Medical Conditions */}
          <div className="summary-section">
            <h3>Medical Conditions</h3>
            <p>{formData.medicalConditions || "None"}</p>
          </div>

          {/* Symptoms */}
          <div className="summary-section">
            <h3>Symptoms</h3>
            <ul>
              {formData.symptoms.length > 0 
                ? formData.symptoms.map((symptom, index) => <li key={index}>{symptom}</li>) 
                : <li>No symptoms reported</li>
              }
            </ul>
          </div>

          {/* Food Frequency */}
          <div className="summary-section">
            <h3>Food Frequency</h3>
            <ul>
              {formData.foodFrequency && Object.keys(formData.foodFrequency).length > 0 ? (
                Object.entries(formData.foodFrequency).map(([food, frequency]) => (
                  <li key={food}>{food}: {frequency}</li>
                ))
              ) : (
                <li>No food frequency data</li>
              )}
            </ul>
          </div>

          {/* Water Intake */}
          <div className="summary-section">
            <h3>Water Intake</h3>
            <p>{formData.waterIntake || "Not specified"}</p>
          </div>

          {/* Allergies */}
          <div className="summary-section">
            <h3>Allergies</h3>
            <p>{formData.allergies || "None"}</p>
          </div>

          {/* Additional Symptoms */}
          <div className="summary-section">
            <h3>Additional Symptoms</h3>
            <p>{formData.extra_symptoms || "None"}</p>
          </div>
        </div>

        <div className="button-group">
          <button className="edit-btn" onClick={() => navigate("/form", { state: { formData } })}>Edit</button>
          <button className="report-btn" onClick={() => navigate('/report', { state: { formData, signUpData } })}>My Report</button>
        </div>
      </div>
    </div>
  );
};

export default Submitted;
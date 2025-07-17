import React, { useState } from 'react';
import './Form.css';

function Form() {
  const [step, setStep] = useState(1);
  const [formData, setFormData] = useState({
    dietaryPreference: '',
    medicalConditions: '',
    symptoms: [],
    foodFrequency: {},
    waterIntake: '',
    allergies: '',
    extra_symptoms: ''
  });

  const handleCheckboxChange = (event) => {
    const { name, checked } = event.target;
    setFormData((prev) => ({
      ...prev,
      symptoms: checked
        ? [...prev.symptoms, name]
        : prev.symptoms.filter((symptom) => symptom !== name)
    }));
  };

  const handleFoodFrequencyChange = (food, value) => {
    setFormData((prev) => ({
      ...prev,
      foodFrequency: { ...prev.foodFrequency, [food]: value }
    }));
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    console.log(formData);
    alert('Form Submitted Successfully!');
  };

  const nextStep = () => {
    if (step < 5) setStep(step + 1);
  };

  const prevStep = () => {
    if (step > 1) setStep(step - 1);
  };

  const renderStep = () => {
    switch (step) {
      case 1:
        return (
          <div className="step">
            <h3>Step 1: Dietary Preference</h3>
            <div className="diet-options">
              {['Vegetarian', 'Non-Vegetarian', 'Vegan'].map((diet) => (
                <label key={diet}>
                  <input type="radio" name="dietaryPreference" value={diet} onChange={(e) => setFormData({...formData, dietaryPreference: e.target.value})} /> {diet}
                </label>
              ))}
            </div>
          </div>
        );
      case 2:
        return (
          <div className="step">
            <h3>Step 2: Medical Conditions</h3>
            <input type="text" placeholder="e.g., Diabetes, Thyroid issues" onChange={(e) => setFormData({...formData, medicalConditions: e.target.value})} />
          </div>
        );
      case 3:
        return (
          <div className="step">
            <h3>Step 3: Symptoms</h3>
            <div className="checkbox-group">
              {["Fatigue or weakness", "Hair loss or brittle nails", "Pale skin", "Frequent infections", "Muscle cramps or bone pain", "Dry or scaly skin", "Poor night vision", "Numbness or tingling in hands/feet", "Slow wound healing", "Loss of appetite"].map((symptom) => (
                <label key={symptom}>
                  <input type="checkbox" name={symptom} onChange={handleCheckboxChange} /> {symptom}
                </label>
              ))}
            </div>
          </div>
        );
      case 4:
        return (
          <div className="step">
            <h3>Step 4: Food Frequency</h3>
            <table>
              <thead>
                <tr>
                  <th>Food Group</th>
                  <th>Daily</th>
                  <th>Few times a week</th>
                  <th>Rarely</th>
                  <th>Never</th>
                </tr>
              </thead>
              <tbody>
                {["Dairy", "Leafy Greens", "Fruits", "Meat, Fish, or Eggs", "Legumes", "Nuts & Seeds", "Whole Grains"].map((food) => (
                  <tr key={food}>
                    <td>{food}</td>
                    {["Daily", "Few times a week", "Rarely", "Never"].map((freq) => (
                      <td key={freq}>
                        <input type="radio" name={food} value={freq} onChange={() => handleFoodFrequencyChange(food, freq)} />
                      </td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        );
      case 5:
        return (
          <div className="step">
            <h3>Step 5: Final Details</h3>
            <label>Do you drink enough water daily?</label>
            <div className="water-options">
              {["Yes (2+ liters)", "Sometimes", "No (Less than 1 liter)"].map((option) => (
                <label key={option}>
                  <input type="radio" name="waterIntake" value={option} onChange={(e) => setFormData({...formData, waterIntake: e.target.value})} /> {option}
                </label>
              ))}
            </div>
            <label>Any dietary restrictions or allergies?</label>
            <input type="text" placeholder="Enter any dietary restrictions" onChange={(e) => setFormData({...formData, allergies: e.target.value})} />
            <label>Any other symptoms you want to add?</label>
            <textarea placeholder="Enter other symptoms (if any)" onChange={(e) => setFormData({...formData, extra_symptoms: e.target.value})} />
          </div>
        );
      default:
        return null;
    }
  };

  return (
    <div className="form-container">
      <h2>Nutrition Deficiency Assessment</h2>
      <div className="progress-bar">
        <div className="progress" style={{ width: `${(step / 5) * 100}%` }}></div>
      </div>
      <form onSubmit={handleSubmit}>
        {renderStep()}
        <div className="navigation-buttons">
          {step > 1 && <button type="button" onClick={prevStep}>Previous</button>}
          {step < 5 && <button type="button" onClick={nextStep}>Next</button>}
          {step === 5 && <button type="submit" className="submit-button">Submit</button>}
        </div>
      </form>
    </div>
  );
}

export default Form;

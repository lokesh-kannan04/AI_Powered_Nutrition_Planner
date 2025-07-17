import React, { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import './F1.css';

function F1() {
  const [step, setStep] = useState(1);
  const location = useLocation();
  const navigate = useNavigate();

  const initialFormData = location.state?.formData || {
    dietaryPreference: '',
    medicalConditions: '',
    symptoms: [],
    foodFrequency: {},
    waterIntake: '',
    allergies: '',
    extra_symptoms: ''
  };

  const [formData, setFormData] = useState(initialFormData);

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
    navigate('/submitted-info', { state: { formData } });
  };

  const nextStep = () => { if (step < 5) setStep(step + 1); };
  const prevStep = () => { if (step > 1) setStep(step - 1); };

  return (
    <div className='f1-body'>
      <div className="f1-form-container">
        <h2 className="f1-title">Nutrition Deficiency Assessment</h2>
        <div className="f1-progress-bar">
          <div className="f1-progress" style={{ width: `${(step / 5) * 100}%` }}></div>
        </div>
        <form onSubmit={handleSubmit} className="f1-form">
          <div className="f1-step f1-card">
            {step === 1 && (
              <>
                <h3>Step 1: Dietary Preference</h3>
                <img className='f1-svgicons' src="images/fruit salad-pana.svg" alt="Diet preference" />
                <div className="f1-diet-options">
                  {["Vegetarian", "Non-Vegetarian", "Vegan"].map((diet) => (
                    <label key={diet}>
                      <input type="radio" name="dietaryPreference" value={diet}
                        checked={formData.dietaryPreference === diet}
                        onChange={(e) => setFormData({ ...formData, dietaryPreference: e.target.value })}
                      />
                      {diet}
                    </label>
                  ))}
                </div>
              </>
            )}
            {step === 2 && (
              <>
                <h3>Step 2: Medical Conditions</h3>
                <img className='f1-svgicons' src="images/Medicine-cuate.svg" alt="Medical Examination" />
                <input type="text" placeholder="e.g., Diabetes, Thyroid issues"
                  value={formData.medicalConditions}
                  onChange={(e) => setFormData({ ...formData, medicalConditions: e.target.value })}
                />
              </>
            )}
            {step === 3 && (
              <>
                <h3>Step 3: Symptoms</h3>
                <img className='f1-svgicons' src="images/slide2.svg" alt="Symptoms Check" />
                <div className="f1-checkbox-group">
                  {["Fatigue or weakness", "Hair loss or brittle nails", "Pale skin", "Frequent infections", "Muscle cramps or bone pain", "Dry or scaly skin", "Poor night vision", "Loss of appetite", "Numbness or tingling in hands/feet", "Slow wound healing"].map((symptom) => (
                    <label key={symptom}>
                      <input type="checkbox" name={symptom}
                        checked={formData.symptoms.includes(symptom)}
                        onChange={handleCheckboxChange}
                      />
                      {symptom}
                    </label>
                  ))}
                </div>
              </>
            )}
            {step === 4 && (
              <>
                <h3>Step 4: Food Frequency</h3>
                <table className="f1-table">
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
                            <input type="radio" name={food} value={freq}
                              checked={formData.foodFrequency[food] === freq}
                              onChange={() => handleFoodFrequencyChange(food, freq)}
                            />
                          </td>
                        ))}
                      </tr>
                    ))}
                  </tbody>
                </table>
              </>
            )}
            {step === 5 && (
              <>
                <h3>Step 5: Final Details</h3>
                <label>Do you drink enough water daily?</label>
                <div className="f1-water-options">
                  {["Yes (2+ litres)", "Sometimes", "No (Less than 1 litre)"].map((option) => (
                    <label key={option}>
                      <input type="radio" name="waterIntake" value={option}
                        checked={formData.waterIntake === option}
                        onChange={(e) => setFormData({ ...formData, waterIntake: e.target.value })}
                      />
                      {option}
                    </label>
                  ))}
                </div>
                <label>Any dietary restrictions or allergies?</label>
                <input type="text" placeholder="Enter any dietary restrictions"
                  value={formData.allergies}
                  onChange={(e) => setFormData({ ...formData, allergies: e.target.value })}
                />
                <label>Any other symptoms you want to add?</label>
                <textarea placeholder="Enter other symptoms (if any)"
                  value={formData.extra_symptoms}
                  onChange={(e) => setFormData({ ...formData, extra_symptoms: e.target.value })}
                />
              </>
            )}
          </div>
          <div className="f1-navigation-buttons">
            {step > 1 && <button type="button" className="f1-prev-button" onClick={prevStep}>Previous</button>}
            {step < 5 && <button type="button" className="f1-next-button" onClick={nextStep}>Next</button>}
            {step === 5 && <button type="submit" className="f1-submit-button">Submit</button>}
          </div>
        </form>
      </div>
    </div>
  );
}

export default F1;
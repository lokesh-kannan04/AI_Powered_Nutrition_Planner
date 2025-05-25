import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './ShowReport.css';

// SVG Icons
const UserIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
    <circle cx="12" cy="7" r="4"></circle>
  </svg>
);

const DietIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M12 2.69l5.66 5.66a8 8 0 1 1-11.31 0z"></path>
    <circle cx="12" cy="12" r="2"></circle>
  </svg>
);

const MedicalIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M18 8h1a4 4 0 0 1 0 8h-1"></path>
    <path d="M2 8h16v9a4 4 0 0 1-4 4H6a4 4 0 0 1-4-4V8z"></path>
    <line x1="6" y1="1" x2="6" y2="4"></line>
    <line x1="10" y1="1" x2="10" y2="4"></line>
    <line x1="14" y1="1" x2="14" y2="4"></line>
  </svg>
);

const WaterIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M22 12h-4l-3 9L9 3l-3 9H2"></path>
  </svg>
);

const AllergyIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M20.24 12.24a6 6 0 0 0-8.49-8.49L5 10.5V19h8.5z"></path>
    <line x1="16" y1="8" x2="2" y2="22"></line>
    <line x1="17.5" y1="15" x2="9" y2="15"></line>
  </svg>
);

const NutrientIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <circle cx="12" cy="12" r="10"></circle>
    <path d="M8 14s1.5 2 4 2 4-2 4-2"></path>
    <line x1="9" y1="9" x2="9.01" y2="9"></line>
    <line x1="15" y1="9" x2="15.01" y2="9"></line>
  </svg>
);

const DownloadIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
    <polyline points="7 10 12 15 17 10"></polyline>
    <line x1="12" y1="15" x2="12" y2="3"></line>
  </svg>
);

const BackIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <line x1="19" y1="12" x2="5" y2="12"></line>
    <polyline points="12 19 5 12 12 5"></polyline>
  </svg>
);

const ChevronIcon = ({ expanded }) => (
  <svg 
    xmlns="http://www.w3.org/2000/svg" 
    width="16" 
    height="16" 
    viewBox="0 0 24 24" 
    fill="none" 
    stroke="currentColor" 
    strokeWidth="2" 
    strokeLinecap="round" 
    strokeLinejoin="round"
    style={{
      transform: expanded ? 'rotate(90deg)' : 'rotate(0deg)',
      transition: 'transform 0.2s ease'
    }}
  >
    <polyline points="9 18 15 12 9 6"></polyline>
  </svg>
);

const ShowReport = () => {
  const [reportData, setReportData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [expandedGoals, setExpandedGoals] = useState(false);
  const [expandedTargets, setExpandedTargets] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchAssessmentData = async () => {
      try {
        const sessionKey = localStorage.getItem('session_key');
        if (!sessionKey) {
          throw new Error('Session key is missing. Please log in again.');
        }

        const response = await fetch('http://localhost:8000/api/get-assessment/', {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'Session-Key': sessionKey
          },
          credentials: 'include'
        });

        if (!response.ok) {
          throw new Error(`Failed to fetch data: ${response.status}`);
        }

        const data = await response.json();
        console.log(data);
        if (!data || typeof data !== 'object') {
          throw new Error('Invalid data received from server');
        }

        setReportData(data);
      } catch (err) {
        console.error('Error fetching assessment data:', err);
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchAssessmentData();
  }, []);

  const handleBack = () => navigate(-1);

  const handleDownload = () => {
    if (!reportData) return;
    
    const element = document.createElement('a');
    const file = new Blob([JSON.stringify(reportData, null, 2)], { 
      type: 'application/json' 
    });
    element.href = URL.createObjectURL(file);
    element.download = 'nutrition_report.json';
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
  };

  const goToCB1 = async () => {
    try {
      const session_key = localStorage.getItem('session_key');
      if (!session_key) {
        console.error('Session Key is missing! Please log in again.');
        return;
      }
      const response = await fetch('http://127.0.0.1:8000/api/chatbot/', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Session-Key': session_key,
        },
        mode: 'cors',
        credentials: 'include',
      });
  
      if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);
  
      const data = await response.json();
      if (data.redirect_url) {
        window.location.href = data.redirect_url;
      }
    } catch (error) {
      console.error('Fetch Error:', error.message);
    }
  };

  const goToCB2 = async () => {
    try {
      const session_key = localStorage.getItem('session_key');
      if (!session_key) {
        console.error('Session Key is missing! Please log in again.');
        return;
      }
      const response = await fetch('http://127.0.0.1:8000/api/nutritionix/', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Session-Key': session_key,
        },
        mode: 'cors',
        credentials: 'include',
      });

      if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);

      const data = await response.json();
      if (data.redirect_url) {
        window.location.href = data.redirect_url;
      } else {
        console.error('Redirect URL not found in response.');
      }
    } catch (error) {
      console.error('Fetch Error:', error.message);
    }
  };

  const goToCB3 = async () => {
    try {
      const session_key = localStorage.getItem('session_key');
      console.log(session_key);
      if (!session_key) {
        console.error('Session Key is missing! Please log in again.');
        return;
      }
      const response = await fetch('http://127.0.0.1:8000/api/tgr/', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Session-Key': session_key,
        },
        mode: 'cors',
        credentials: 'include',
      });
  
      if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);
  
      const data = await response.json();
      if (data.redirect_url) {
        window.location.href = data.redirect_url;
      }
    } catch (error) {
      console.error('Fetch Error:', error.message);
    }
  };

  if (loading) {
    return (
      <div className="loading-container">
        <div className="loading-spinner"></div>
        <p>Generating your personalized nutrition report...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="error-container">
        <div className="error-icon">⚠️</div>
        <h3>Error Loading Report</h3>
        <p>{error}</p>
        <button className="btn-primary" onClick={() => window.location.reload()}>
          Try Again
        </button>
      </div>
    );
  }

  if (!reportData) {
    return (
      <div className="error-container">
        <div className="error-icon">⚠️</div>
        <h3>No Data Available</h3>
        <p>Unable to load nutrition report data.</p>
      </div>
    );
  }

  return (
    <div className="report-page">
      {/* Nutrition Goals Dropdown */}
      <div className={`dropdown-section ${expandedGoals ? 'expanded' : ''}`}>
        <div 
          className="dropdown-header"
          onClick={() => setExpandedGoals(!expandedGoals)}
        >
          <ChevronIcon expanded={expandedGoals} />
          <h2>Nutrition Goals</h2>
        </div>
        {expandedGoals && (
          <div className="dropdown-content">
            <div className="goal-summary-card">
              <div className="card-header">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M12 2v4M12 18v4M4.93 4.93l2.83 2.83M16.24 16.24l2.83 2.83M2 12h4M18 12h4M4.93 19.07l2.83-2.83M16.24 7.76l2.83-2.83"></path>
                </svg>
                <h2>Nutrition Goals</h2>
              </div>
              <div className="card-content">
                {reportData.goal ? (
                  <>
                    <div className="goal-metrics">
                      <div className="metric-item">
                        <span className="metric-label">BMR</span>
                        <span className="metric-value">{reportData.goal.BMR} kcal/day</span>
                        <span className="metric-description">Basal Metabolic Rate</span>
                      </div>
                      <div className="metric-item">
                        <span className="metric-label">TDEE</span>
                        <span className="metric-value">{reportData.goal.TDEE} kcal/day</span>
                        <span className="metric-description">Total Daily Energy Expenditure</span>
                      </div>
                      <div className="metric-item">
                        <span className="metric-label">Target</span>
                        <span className="metric-value">{reportData.goal['Goal Calories']} kcal</span>
                        <span className="metric-description">Daily Calorie Target</span>
                      </div>
                    </div>

                    <div className="macros-section">
                      <h3>Macronutrient Targets</h3>
                      <div className="macros-grid">
                        <div className="macro-item">
                          <span className="macro-label">Protein</span>
                          <span className="macro-value">{reportData.goal.Macros.protein_g}g</span>
                        </div>
                        <div className="macro-item">
                          <span className="macro-label">Carbs</span>
                          <span className="macro-value">{reportData.goal.Macros.carbs_g}g</span>
                        </div>
                        <div className="macro-item">
                          <span className="macro-label">Fats</span>
                          <span className="macro-value">
                            {reportData.goal.Macros.fat_g ?? reportData.goal.Macros.fat_g ?? '--'}g
                          </span>
                        </div>
                        <div className="macro-item">
                          <span className="macro-label">Fiber</span>
                          <span className="macro-value">{reportData.goal.Macros.fiber_g}g</span>
                        </div>
                      </div>
                    </div>

                    {reportData.goal.Micronutrients && Object.keys(reportData.goal.Micronutrients).length > 0 && (
                      <div className="micronutrients-section">
                        <h3>Key Micronutrients</h3>
                        <div className="micronutrients-grid">
                          {Object.entries(reportData.goal.Micronutrients).map(([nutrient, info]) => (
                            <div className="micronutrient-item" key={nutrient}>
                              <span className="micronutrient-label">
                                {nutrient.charAt(0).toUpperCase() + nutrient.slice(1)}
                              </span>
                              <span className="micronutrient-value">Def : {info.pa}</span>
                              <span className="micronutrient-sources">Regular : {info.sa}</span>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}

                    <div className="goal-summary">
                      <h3>Plan Summary</h3>
                      <p>
                        Your goal is to <strong>{reportData.goal.Goal?.toLowerCase() ?? 'maintain fitness'}</strong> with a{' '}
                        <strong>{reportData.goal.ActivityLevel?.toLowerCase() ?? 'moderate'}</strong> activity level.
                      </p>
                    </div>
                    

                    <div className="goal-tracker-card">
                      <div className="card-header">
                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                          <path d="M22 12h-4l-3 9L9 3l-3 9H2"></path>
                        </svg>
                        <h2>Daily Progress Tracker</h2>
                      </div>
                      <div className="card-content">
                        {reportData.nutritional_goals ? (
                          <>
                            {/* Calories Tracker */}
                            <div className="tracker-item">
                              <div className="tracker-header">
                                <span className="tracker-label">Calories</span>
                                <span className="tracker-values">
                                  {reportData.nutritional_goals.calories_taken || 0} / {reportData.nutritional_goals.goal_calories} kcal
                                </span>
                              </div>
                              <div className="tracker-slider">
                                <div 
                                  className="slider-fill"
                                  style={{
                                    width: `${Math.min(
                                      (parseInt(reportData.nutritional_goals.calories_taken) / 
                                      parseInt(reportData.nutritional_goals.goal_calories)) * 100, 
                                      100
                                    )}%`
                                  }}
                                ></div>
                              </div>
                            </div>

                            {/* Macros Trackers */}
                            <div className="macros-tracker">
                              <h3>Macronutrients</h3>
                              <div className="macros-tracker-grid">
                                {/* Protein */}
                                <div className="tracker-item">
                                  <div className="tracker-header">
                                    <span className="tracker-label">Protein</span>
                                    <span className="tracker-values">
                                      {reportData.nutritional_goals.protein_taken || '0g'} / {reportData.nutritional_goals.protein_goal}
                                    </span>
                                  </div>
                                  <div className="tracker-slider">
                                    <div 
                                      className="slider-fill"
                                      style={{
                                        width: `${Math.min(
                                          (parseInt(reportData.nutritional_goals.protein_taken) / 
                                          parseInt(reportData.nutritional_goals.protein_goal)) * 100, 
                                          100
                                        )}%`
                                      }}
                                    ></div>
                                  </div>
                                </div>

                                {/* Fat */}
                                <div className="tracker-item">
                                  <div className="tracker-header">
                                    <span className="tracker-label">Fat</span>
                                    <span className="tracker-values">
                                      {reportData.nutritional_goals.fat_taken || '0g'} / {reportData.nutritional_goals.fat_goal}
                                    </span>
                                  </div>
                                  <div className="tracker-slider">
                                    <div 
                                      className="slider-fill"
                                      style={{
                                        width: `${Math.min(
                                          (parseInt(reportData.nutritional_goals.fat_taken) / 
                                          parseInt(reportData.nutritional_goals.fat_goal)) * 100, 
                                          100
                                        )}%`
                                      }}
                                    ></div>
                                  </div>
                                </div>

                                {/* Carbs */}
                                <div className="tracker-item">
                                  <div className="tracker-header">
                                    <span className="tracker-label">Carbs</span>
                                    <span className="tracker-values">
                                      {reportData.nutritional_goals.carbs_taken || '0g'} / {reportData.nutritional_goals.carbs_goal}
                                    </span>
                                  </div>
                                  <div className="tracker-slider">
                                    <div 
                                      className="slider-fill"
                                      style={{
                                        width: `${Math.min(
                                          (parseInt(reportData.nutritional_goals.carbs_taken) / 
                                          parseInt(reportData.nutritional_goals.carbs_goal)) * 100, 
                                          100
                                        )}%`
                                      }}
                                    ></div>
                                  </div>
                                </div>

                                {/* Fiber */}
                                <div className="tracker-item">
                                  <div className="tracker-header">
                                    <span className="tracker-label">Fiber</span>
                                    <span className="tracker-values">
                                      {reportData.nutritional_goals.fiber_taken || '0g'} / {reportData.nutritional_goals.fiber_goal}
                                    </span>
                                  </div>
                                  <div className="tracker-slider">
                                    <div 
                                      className="slider-fill"
                                      style={{
                                        width: `${Math.min(
                                          (parseInt(reportData.nutritional_goals.fiber_taken) / 
                                          parseInt(reportData.nutritional_goals.fiber_goal)) * 100, 
                                          100
                                        )}%`
                                      }}
                                    ></div>
                                  </div>
                                </div>
                              </div>
                            </div>

                            {/* Micronutrients Trackers */}
                            <div className="micronutrients-tracker">
                              <h3>Micronutrients</h3>
                              <div className="micro-tracker-grid">
                                {/* Micro 1 */}
                                {reportData.nutritional_goals.micro1_name && (
                                  <div className="tracker-item">
                                    <div className="tracker-header">
                                      <span className="tracker-label">
                                        {reportData.nutritional_goals.micro1_name.charAt(0).toUpperCase() + 
                                        reportData.nutritional_goals.micro1_name.slice(1)}
                                      </span>
                                      <span className="tracker-values">
                                        {reportData.nutritional_goals.micro1_taken || '0'} / {reportData.nutritional_goals.micro1_goal}
                                      </span>
                                    </div>
                                    <div className="tracker-slider">
                                      <div 
                                        className="slider-fill"
                                        style={{
                                          width: `${Math.min(
                                            (parseFloat(reportData.nutritional_goals.micro1_taken) / 
                                            parseFloat(reportData.nutritional_goals.micro1_goal)) * 100, 
                                            100
                                          )}%`
                                        }}
                                      ></div>
                                    </div>
                                  </div>
                                )}

                                {/* Micro 2 */}
                                {reportData.nutritional_goals.micro2_name && (
                                  <div className="tracker-item">
                                    <div className="tracker-header">
                                      <span className="tracker-label">
                                        {reportData.nutritional_goals.micro2_name.charAt(0).toUpperCase() + 
                                        reportData.nutritional_goals.micro2_name.slice(1)}
                                      </span>
                                      <span className="tracker-values">
                                        {reportData.nutritional_goals.micro2_taken || '0'} / {reportData.nutritional_goals.micro2_goal}
                                      </span>
                                    </div>
                                    <div className="tracker-slider">
                                      <div 
                                        className="slider-fill"
                                        style={{
                                          width: `${Math.min(
                                            (parseFloat(reportData.nutritional_goals.micro2_taken) / 
                                            parseFloat(reportData.nutritional_goals.micro2_goal)) * 100, 
                                            100
                                          )}%`
                                        }}
                                      ></div>
                                    </div>
                                  </div>
                                )}

                                {/* Micro 3 */}
                                {reportData.nutritional_goals.micro3_name && (
                                  <div className="tracker-item">
                                    <div className="tracker-header">
                                      <span className="tracker-label">
                                        {reportData.nutritional_goals.micro3_name.charAt(0).toUpperCase() + 
                                        reportData.nutritional_goals.micro3_name.slice(1)}
                                      </span>
                                      <span className="tracker-values">
                                        {reportData.nutritional_goals.micro3_taken || '0'} / {reportData.nutritional_goals.micro3_goal}
                                      </span>
                                    </div>
                                    <div className="tracker-slider">
                                      <div 
                                        className="slider-fill"
                                        style={{
                                          width: `${Math.min(
                                            (parseFloat(reportData.nutritional_goals.micro3_taken) / 
                                            parseFloat(reportData.nutritional_goals.micro3_goal)) * 100, 
                                            100
                                          )}%`
                                        }}
                                      ></div>
                                    </div>
                                  </div>
                                )}
                              </div>
                            </div>
                          </>
                        ) : (
                          <p className="no-tracker-data">No tracking data available yet.</p>
                        )}
                      </div>
                    </div>
                  </>
                ) : (
                  <p className="no-goals">No specific nutrition goals were set.</p>
                )}
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Nutrition Targets Dropdown */}
      <div className={`dropdown-section ${expandedTargets ? 'expanded' : ''}`}>
        <div 
          className="dropdown-header"
          onClick={() => setExpandedTargets(!expandedTargets)}
        >
          <ChevronIcon expanded={expandedTargets} />
          <h2>Nutrition Targets</h2>
        </div>
        {expandedTargets && (
          <div className="dropdown-content">
            <div className="target-summary-card">
              <div className="card-header">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <circle cx="12" cy="12" r="10"></circle>
                  <path d="M16 12l-4-4-4 4M12 16V8"></path>
                </svg>
                <h2>Nutrition Targets</h2>
              </div>
              <div className="card-content">
                {reportData.target?.basics && (
                  <>
                    <div className="target-metrics">
                      <div className="metric-item">
                        <span className="metric-label">BMR</span>
                        <span className="metric-value">{reportData.target.basics.BMR.original}</span>
                        <span className="metric-description">Basal Metabolic Rate</span>
                      </div>
                      <div className="metric-item">
                        <span className="metric-label">TDEE</span>
                        <span className="metric-value">{reportData.target.basics.TDEE.original}</span>
                        <span className="metric-description">Total Daily Energy Expenditure</span>
                      </div>
                      <div className="metric-item">
                        <span className="metric-label">Goal Calories</span>
                        <span className="metric-value">{reportData.target.basics.goal_calories.value}</span>
                        <span className="metric-description">Daily Target ({reportData.target.basics.goal})</span>
                      </div>
                    </div>

                    <div className="macros-section">
                      <h3>Macronutrient Targets</h3>
                      <div className="macros-grid">
                        <div className="macro-item">
                          <span className="macro-label">Protein</span>
                          <span className="macro-value">{reportData.target.macros.protein_g.value}g</span>
                        </div>
                        <div className="macro-item">
                          <span className="macro-label">Carbs</span>
                          <span className="macro-value">{reportData.target.macros.carbs_g.value}g</span>
                        </div>
                        <div className="macro-item">
                          <span className="macro-label">Fats</span>
                          <span className="macro-value">{reportData.target.macros.fat_g.value}g</span>
                        </div>
                        <div className="macro-item">
                          <span className="macro-label">Fiber</span>
                          <span className="macro-value">{reportData.target.macros.fiber_g.value}g</span>
                        </div>
                      </div>
                    </div>

                    {reportData.target.micronutrients && (
                      <div className="micronutrients-section">
                        <h3>Key Micronutrient Targets</h3>
                        <div className="micronutrients-grid">
                          {Object.entries(reportData.target.micronutrients).map(([nutrient, data]) => (
                            <div className="micronutrient-item" key={nutrient}>
                              <span className="micronutrient-label">
                                {nutrient.charAt(0).toUpperCase() + nutrient.slice(1)}
                              </span>
                              <span className="micronutrient-value">
                                Standard: {data.standard.value} {data.standard.unit}
                              </span>
                              <span className="micronutrient-value">
                                Personalized: {data.personalized.value} {data.standard.unit}
                              </span>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}

                  <div className="goal-tracker-card">
                    <div className="card-header">
                      <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                        <path d="M22 12h-4l-3 9L9 3l-3 9H2"></path>
                      </svg>
                      <h2>Daily Progress Tracker</h2>
                    </div>
                    <div className="card-content">
                      {reportData.monthly_goals ? (
                        <>
                          {/* Calories Tracker */}
                          <div className="tracker-item">
                            <div className="tracker-header">
                              <span className="tracker-label">Calories</span>
                              <span className="tracker-values">
                                {reportData.monthly_goals.calories_taken || 0} / {reportData.monthly_goals.goal_calories} kcal
                              </span>
                            </div>
                            <div className="tracker-slider">
                              <div 
                                className="slider-fill"
                                style={{
                                  width: `${Math.min(
                                    (parseInt(reportData.monthly_goals.calories_taken) / 
                                    parseInt(reportData.monthly_goals.goal_calories)) * 100, 
                                    100
                                  )}%`
                                }}
                              ></div>
                            </div>
                          </div>

                          {/* Macros Trackers */}
                          <div className="macros-tracker">
                            <h3>Macronutrients</h3>
                            <div className="macros-tracker-grid">
                              {/* Protein */}
                              <div className="tracker-item">
                                <div className="tracker-header">
                                  <span className="tracker-label">Protein</span>
                                  <span className="tracker-values">
                                    {reportData.monthly_goals.protein_taken || '0g'} / {reportData.monthly_goals.protein_goal}
                                  </span>
                                </div>
                                <div className="tracker-slider">
                                  <div 
                                    className="slider-fill"
                                    style={{
                                      width: `${Math.min(
                                        (parseInt(reportData.monthly_goals.protein_taken) / 
                                        parseInt(reportData.monthly_goals.protein_goal)) * 100, 
                                        100
                                      )}%`
                                    }}
                                  ></div>
                                </div>
                              </div>

                              {/* Fat */}
                              <div className="tracker-item">
                                <div className="tracker-header">
                                  <span className="tracker-label">Fat</span>
                                  <span className="tracker-values">
                                    {reportData.monthly_goals.fat_taken || '0g'} / {reportData.monthly_goals.fat_goal}
                                  </span>
                                </div>
                                <div className="tracker-slider">
                                  <div 
                                    className="slider-fill"
                                    style={{
                                      width: `${Math.min(
                                        (parseInt(reportData.monthly_goals.fat_taken) / 
                                        parseInt(reportData.monthly_goals.fat_goal)) * 100, 
                                        100
                                      )}%`
                                    }}
                                  ></div>
                                </div>
                              </div>

                              {/* Carbs */}
                              <div className="tracker-item">
                                <div className="tracker-header">
                                  <span className="tracker-label">Carbs</span>
                                  <span className="tracker-values">
                                    {reportData.monthly_goals.carbs_taken || '0g'} / {reportData.monthly_goals.carbs_goal}
                                  </span>
                                </div>
                                <div className="tracker-slider">
                                  <div 
                                    className="slider-fill"
                                    style={{
                                      width: `${Math.min(
                                        (parseInt(reportData.monthly_goals.carbs_taken) / 
                                        parseInt(reportData.monthly_goals.carbs_goal)) * 100, 
                                        100
                                      )}%`
                                    }}
                                  ></div>
                                </div>
                              </div>

                              {/* Fiber */}
                              <div className="tracker-item">
                                <div className="tracker-header">
                                  <span className="tracker-label">Fiber</span>
                                  <span className="tracker-values">
                                    {reportData.monthly_goals.fiber_taken || '0g'} / {reportData.monthly_goals.fiber_goal}
                                  </span>
                                </div>
                                <div className="tracker-slider">
                                  <div 
                                    className="slider-fill"
                                    style={{
                                      width: `${Math.min(
                                        (parseInt(reportData.monthly_goals.fiber_taken) / 
                                        parseInt(reportData.monthly_goals.fiber_goal)) * 100, 
                                        100
                                      )}%`
                                    }}
                                  ></div>
                                </div>
                              </div>
                            </div>
                          </div>

                          {/* Micronutrients Trackers */}
                          <div className="micronutrients-tracker">
                            <h3>Micronutrients</h3>
                            <div className="micro-tracker-grid">
                              {/* Micro 1 */}
                              {reportData.monthly_goals.micro1_name && (
                                <div className="tracker-item">
                                  <div className="tracker-header">
                                    <span className="tracker-label">
                                      {reportData.monthly_goals.micro1_name.charAt(0).toUpperCase() + 
                                      reportData.monthly_goals.micro1_name.slice(1)}
                                    </span>
                                    <span className="tracker-values">
                                      {reportData.monthly_goals.micro1_taken || '0'} / {reportData.monthly_goals.micro1_goal}
                                    </span>
                                  </div>
                                  <div className="tracker-slider">
                                    <div 
                                      className="slider-fill"
                                      style={{
                                        width: `${Math.min(
                                          (parseFloat(reportData.monthly_goals.micro1_taken) / 
                                          parseFloat(reportData.monthly_goals.micro1_goal)) * 100, 
                                          100
                                        )}%`
                                      }}
                                    ></div>
                                  </div>
                                </div>
                              )}

                              {/* Micro 2 */}
                              {reportData.monthly_goals.micro2_name && (
                                <div className="tracker-item">
                                  <div className="tracker-header">
                                    <span className="tracker-label">
                                      {reportData.monthly_goals.micro2_name.charAt(0).toUpperCase() + 
                                      reportData.monthly_goals.micro2_name.slice(1)}
                                    </span>
                                    <span className="tracker-values">
                                      {reportData.monthly_goals.micro2_taken || '0'} / {reportData.monthly_goals.micro2_goal}
                                    </span>
                                  </div>
                                  <div className="tracker-slider">
                                    <div 
                                      className="slider-fill"
                                      style={{
                                        width: `${Math.min(
                                          (parseFloat(reportData.monthly_goals.micro2_taken) / 
                                          parseFloat(reportData.monthly_goals.micro2_goal)) * 100, 
                                          100
                                        )}%`
                                      }}
                                    ></div>
                                  </div>
                                </div>
                              )}

                              {/* Micro 3 */}
                              {reportData.monthly_goals.micro3_name && (
                                <div className="tracker-item">
                                  <div className="tracker-header">
                                    <span className="tracker-label">
                                      {reportData.monthly_goals.micro3_name.charAt(0).toUpperCase() + 
                                      reportData.monthly_goals.micro3_name.slice(1)}
                                    </span>
                                    <span className="tracker-values">
                                      {reportData.monthly_goals.micro3_taken || '0'} / {reportData.monthly_goals.micro3_goal}
                                    </span>
                                  </div>
                                  <div className="tracker-slider">
                                    <div 
                                      className="slider-fill"
                                      style={{
                                        width: `${Math.min(
                                          (parseFloat(reportData.monthly_goals.micro3_taken) / 
                                          parseFloat(reportData.monthly_goals.micro3_goal)) * 100, 
                                          100
                                        )}%`
                                      }}
                                    ></div>
                                  </div>
                                </div>
                              )}
                            </div>
                          </div>
                        </>
                      ) : (
                        <p className="no-tracker-data">No tracking data available yet.</p>
                      )}
                    </div>
                  </div>

                    
                  </>
                )}
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Main Report Container */}
      <div className="report-container">
        <header className="report-header">
          <h1 className="report-title">
            <span className="title-icon">🍏</span>
            Nutrition Assessment Report
          </h1>
          <p className="report-meta">
            Generated on {new Date(reportData.submitted_at).toLocaleDateString('en-US', {
              year: 'numeric',
              month: 'long',
              day: 'numeric',
              hour: '2-digit',
              minute: '2-digit'
            })}
          </p>
        </header>

        <div className="toolbar">
          <div className="chatbot-buttons">
            <button className="btn-chatbot" onClick={goToCB1}>
              <span className="btn-icon">🤖</span> Nutrition Chatbot
            </button>
            <button className="btn-chatbot" onClick={goToCB2}>
              <span className="btn-icon">🔍</span> Food Analyzer
            </button>
            <button className="btn-chatbot" onClick={goToCB3}>
              <span className="btn-icon">📊</span> Meal Planner
            </button>
          </div>
        </div>

        <div className="report-grid">
          <div className="report-card personal-card">
            <div className="card-header">
              <UserIcon />
              <h2>Personal Details</h2>
            </div>
            <div className="card-content">
              <div className="detail-item">
                <span className="detail-label">Assessment Date:</span>
                <span className="detail-value">
                  {new Date(reportData.submitted_at).toLocaleDateString()}
                </span>
              </div>
            </div>
          </div>

          <div className="report-card">
            <div className="card-header">
              <DietIcon />
              <h2>Dietary Preferences</h2>
            </div>
            <div className="card-content">
              <div className="diet-tag">{reportData.dietaryPreference}</div>
            </div>
          </div>

          <div className="report-card">
            <div className="card-header">
              <MedicalIcon />
              <h2>Health Profile</h2>
            </div>
            <div className="card-content">
              <div className="health-item">
                <h3>Medical Conditions</h3>
                <p>{reportData.medicalConditions || 'None reported'}</p>
              </div>
              <div className="health-item">
                <h3>Allergies</h3>
                <p>{reportData.allergies || 'None reported'}</p>
              </div>
            </div>
          </div>

          <div className="report-card symptoms-card">
            <div className="card-header">
              <MedicalIcon />
              <h2>Reported Symptoms</h2>
            </div>
            <div className="card-content">
              <ul className="symptoms-list">
                {reportData.symptoms?.map((symptom, index) => (
                  <li key={index}>
                    <span className="symptom-bullet">•</span>
                    {symptom}
                  </li>
                ))}
              </ul>
            </div>
          </div>

          <div className="report-card wide-card">
            <div className="card-header">
              <DietIcon />
              <h2>Food Frequency Analysis</h2>
            </div>
            <div className="card-content">
              <div className="table-container">
                <table>
                  <thead>
                    <tr>
                      <th>Food Item</th>
                      <th>Consumption Frequency</th>
                    </tr>
                  </thead>
                  <tbody>
                    {reportData.foodFrequency && Object.entries(reportData.foodFrequency).map(([food, frequency], index) => (
                      <tr key={index}>
                        <td>{food}</td>
                        <td>
                          <div className="frequency-bar" style={{ width: `${(frequency / 7) * 100}%` }}>
                            {frequency}x/week
                          </div>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>

          <div className="report-card">
            <div className="card-header">
              <WaterIcon />
              <h2>Hydration</h2>
            </div>
            <div className="card-content">
              <div className="water-intake">
                <div className="water-amount">{reportData.waterIntake}</div>
                <div className="water-label">Daily Average</div>
              </div>
            </div>
          </div>

          <div className="report-card wide-card">
            <div className="card-header">
              <NutrientIcon />
              <h2>Nutritional Insights</h2>
            </div>
            <div className="card-content">
              <h3>Potential Deficiencies</h3>
              <div className="deficiency-grid">
                {reportData.deficiencies?.map((deficiency, index) => (
                  <div className="deficiency-item" key={index}>
                    <div className="deficiency-name">{deficiency}</div>
                    <div className="deficiency-meter">
                      <div 
                        className="meter-fill" 
                        style={{ width: `${reportData.percentages?.[index] || 0}%` }}
                      ></div>
                      <span className="meter-value">{reportData.percentages?.[index] || 0}% likelihood</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>

        <div className="report-actions">
          <button className="btn-secondary" onClick={handleBack}>
            <BackIcon /> Back to Dashboard
          </button>
          <button className="btn-primary" onClick={handleDownload}>
            <DownloadIcon /> Download Full Report
          </button>
        </div>
      </div>
    </div>
  );
};

export default ShowReport;
import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import './Register.css';

const Register = () => {
    const navigate = useNavigate();
    const [step, setStep] = useState(0);
    
    const [formData, setFormData] = useState({
        name: "",
        email: "",
        phone: "",
        location: "",
        age: "",
        gender: "",
        height: "",
        weight: "",
        goal: "",
        password: ""
    });

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData({
            ...formData,
            [name]: value,
        });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        console.log("Submitting Data:", formData);

        try {
            const response = await fetch("http://127.0.0.1:8000/api/submit_form/", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(formData),
            });

            if (response.ok) {
                alert("Form Submitted Successfully.");
                navigate("/login", { state: { signupData: formData } });
            } else {
                alert("Failed to submit form.");
            }
        } catch (error) {
            console.error("Error:", error);
            alert("Something went wrong!");
        }
    };

    const nextStep = () => {
        if (step < 4) setStep(step + 1);
    };

    const prevStep = () => {
        if (step > 0) setStep(step - 1);
    };

    const formSteps = [
        [
            { label: "Name:", name: "name", type: "text", placeholder: "Enter your name", icon: "👤" },
            { label: "Email:", name: "email", type: "email", placeholder: "Enter your email", icon: "✉️" },
            { label: "Phone:", name: "phone", type: "tel", placeholder: "Enter your phone", icon: "📱" }
        ],
        [
            { label: "Location:", name: "location", type: "text", placeholder: "Enter your location", icon: "📍" },
            { label: "Age:", name: "age", type: "number", placeholder: "Enter your age", icon: "🎂" }
        ],
        [
            { label: "Gender:", name: "gender", type: "select", options: ["Male", "Female", "Other"], icon: "🚻" },
            { label: "Height (cm):", name: "height", type: "number", placeholder: "Enter your height", icon: "📏" }
        ],
        [
            { label: "Weight (kg):", name: "weight", type: "number", placeholder: "Enter your weight", icon: "⚖️" },
            { label: "Goal:", name: "goal", type: "select", options: ["Gain", "Lose", "Fit"], icon: "🎯" }
        ],
        [
            { label: "Password:", name: "password", type: "password", placeholder: "Enter your password", icon: "🔒" }
        ]
    ];

    const stepTitles = [
        " ",
        " ",
        " ",
        " ",
        " "
    ];

    return (
        <div className="registration-container">
            <div className="registration-card">
                <div className="card-header">
                    <h2>Create Your Account</h2>
                    {/* <p className="subtitle">Join our fitness community in just a few steps</p> */}
                    
                    <div className="progress-indicator">
                        {[0, 1, 2, 3, 4].map((stepNumber) => (
                            <React.Fragment key={stepNumber}>
                                <div className={`progress-step ${step === stepNumber ? 'active' : ''} ${step > stepNumber ? 'completed' : ''}`}>
                                    <div className="step-number">
                                        {step > stepNumber ? '✓' : stepNumber + 1}
                                    </div>
                                    {stepNumber < 4 && (
                                        <div className={`step-connector ${step > stepNumber ? 'completed' : ''}`} />
                                    )}
                                </div>
                            </React.Fragment>
                        ))}
                    </div>
                </div>

                <div className="registration-form">
                    <form onSubmit={handleSubmit}>
                        <h3 style={{color: '#2c3e50', marginBottom: '1.5rem', textAlign: 'center'}}>
                            {stepTitles[step]}
                        </h3>
                        
                        <div className="form-fields">
                            {formSteps[step].map((field, index) => (
                                <div className="form-field" key={index} 
                                     style={field.type === "select" ? {gridColumn: "1 / -1"} : {}}>
                                    <label>
                                        <span className="field-icon">{field.icon}</span>
                                        {field.label}
                                    </label>
                                    {field.type === "select" ? (
                                        <select 
                                            name={field.name} 
                                            value={formData[field.name]} 
                                            onChange={handleChange} 
                                            required
                                        >
                                            <option value="">Select {field.label.toLowerCase().replace(':', '')}</option>
                                            {field.options.map((option, idx) => (
                                                <option key={idx} value={option}>{option}</option>
                                            ))}
                                        </select>
                                    ) : (
                                        <input
                                            type={field.type}
                                            name={field.name}
                                            value={formData[field.name]}
                                            onChange={handleChange}
                                            required
                                            placeholder={field.placeholder}
                                        />
                                    )}
                                </div>
                            ))}
                        </div>

                        <div className="form-actions">
                            <span className="step-counter">Step {step + 1} of {formSteps.length}</span>
                            <div style={{display: 'flex', gap: '1rem'}}>
                                {step > 0 && (
                                    <button 
                                        type="button" 
                                        className="nav-button secondary" 
                                        onClick={prevStep}
                                    >
                                        ← Back
                                    </button>
                                )}
                                {step < formSteps.length - 1 ? (
                                    <button 
                                        type="button" 
                                        className="nav-button primary" 
                                        onClick={nextStep}
                                    >
                                        Next →
                                    </button>
                                ) : (
                                    <button 
                                        type="submit" 
                                        className="submit-button"
                                    >
                                        Complete Registration
                                    </button>
                                )}
                            </div>
                        </div>
                    </form>

                    <div className="form-footer">
                        <div className="security-badge">
                            <span className="lock-icon">🔒</span>
                            Your information is securely encrypted
                        </div>
                        <p className="login-prompt">
                            Already have an account? <a href="/login">Log in</a>
                        </p>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Register;
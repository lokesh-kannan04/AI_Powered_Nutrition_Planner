import React from 'react';
import Footer from './Footer.jsx';
import Register from './Register.jsx';
import './SignUp.css';
import Content from './Content.jsx';

function SignUp() {
  return (
    <div className="signup-page">
      <div className="signup-hero">
        <div className="signup-hero-content">
          <h1 className="signup-hero-title">Transform Your Health Journey</h1>
          <p className="signup-hero-subtitle">Get personalized nutrition plans tailored to your unique needs and goals</p>
        </div>
      </div>

      <div className="signup-container">
        <div className="signup-main">
          <div className="signup-card">
            <Register />
          </div>

          <div className="signup-benefits-section">
            <div className="signup-benefits-content">
              <h3 className="signup-benefits-title">Your Journey Starts Now!</h3>
              <div className="signup-benefits-image">
                <img src="images/slide1.svg" alt="Healthy lifestyle" />
              </div>
              
              <ul className="signup-benefits-list">
                <li className="signup-benefit-item">
                  <span className="signup-benefit-icon">🍎</span>
                  <span>Personalized meal plans</span>
                </li>
                <li className="signup-benefit-item">
                  <span className="signup-benefit-icon">📊</span>
                  <span>AI-powered nutrition analysis</span>
                </li>
                <li className="signup-benefit-item">
                  <span className="signup-benefit-icon">🏆</span>
                  <span>Progress tracking dashboard</span>
                </li>
                <li className="signup-benefit-item">
                  <span className="signup-benefit-icon">💬</span>
                  <span>24/7 nutrition support</span>
                </li>
              </ul>
            </div>
          </div>
        </div>

        <div className="signup-features-section">
          <Content />
        </div>
      </div>

      <Footer />
    </div>
  );
}

export default SignUp;
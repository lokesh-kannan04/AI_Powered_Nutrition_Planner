import React, { useState, useEffect } from "react";
import "./Content.css";

function Content() {
  const [slide, setSlide] = useState(0);
  const [isPaused, setIsPaused] = useState(false);
  const [fade, setFade] = useState(true);

  const slides = [
    {
      title: "AI Nutrition Analysis",
      content: [
        "AI-driven analysis of your health data to detect nutrient deficiencies",
        "Provides tailored diet recommendations based on your unique needs",
        "Continuous monitoring of your nutritional intake"
      ],
      icon: "🤖"
    },
    {
      title: "Personalized Diet Plans",
      content: [
        "Custom diet charts based on available food items",
        "Prevents health risks by recommending compatible foods",
        "AI chatbot for meal suggestions and tracking"
      ],
      icon: "🍽️"
    },
    {
      title: "Progress Tracking",
      content: [
        "Automatically updates your nutrition plan based on progress",
        "Tracks weight, BMI, and nutrient intake",
        "Adapts to help you meet your health goals"
      ],
      icon: "📈"
    }
  ];

  useEffect(() => {
    if (!isPaused) {
      const interval = setInterval(() => {
        setFade(false);
        setTimeout(() => {
          setSlide((prev) => (prev + 1) % slides.length);
          setFade(true);
        }, 300);
      }, 5000);

      return () => clearInterval(interval);
    }
  }, [isPaused, slides.length]);

  const nextSlide = () => {
    setFade(false);
    setTimeout(() => {
      setSlide((prev) => (prev + 1) % slides.length);
      setFade(true);
    }, 300);
  };

  const prevSlide = () => {
    setFade(false);
    setTimeout(() => {
      setSlide((prev) => (prev - 1 + slides.length) % slides.length);
      setFade(true);
    }, 300);
  };

  return (
    <div 
      className="content-slider" 
      onMouseEnter={() => setIsPaused(true)} 
      onMouseLeave={() => setIsPaused(false)}
    >
      <button className="slider-nav left" onClick={prevSlide}>
        &#10094;
      </button>

      <div className={`slide ${fade ? "fade-in" : "fade-out"}`}>
        <div className="slide-icon">{slides[slide].icon}</div>
        <h3 className="slide-title">{slides[slide].title}</h3>
        <ul className="slide-list">
          {slides[slide].content.map((item, index) => (
            <li key={index} className="slide-item">
              <span className="bullet">•</span>
              {item}
            </li>
          ))}
        </ul>
      </div>

      <button className="slider-nav right" onClick={nextSlide}>
        &#10095;
      </button>

      <div className="slider-dots">
        {slides.map((_, index) => (
          <button
            key={index}
            className={`dot ${index === slide ? 'active' : ''}`}
            onClick={() => {
              setFade(false);
              setTimeout(() => {
                setSlide(index);
                setFade(true);
              }, 300);
            }}
          />
        ))}
      </div>
    </div>
  );
}

export default Content;
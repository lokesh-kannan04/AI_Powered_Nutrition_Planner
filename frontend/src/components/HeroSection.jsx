import React from 'react';
import { Typewriter } from 'react-simple-typewriter';
import Button from './Button.jsx';
import './HeroSection.css';
import '../App.css';
import Footer from './pages/Footer.jsx';

function HeroSection() {
  return (
    <>
    <div className='hero-container'>
      <div className='hero-left'>
      <h1>
        <Typewriter
          words={[
            'Every meal is an opportunity to nourish your body.',
            'Make every bite count!',
            'Eat well, live well.'
          ]}
          loop={Infinity}
          cursor
          cursorStyle="|"
          typeSpeed={50}
          deleteSpeed={30}
          delaySpeed={2000}
        />
      </h1>
      <p></p>
      <p>What are you waiting for?</p>
      <div className='hero-btns'>
        <Button className='btns' buttonStyle='btn--outline' buttonSize='btn--large'>
          GET STARTED
        </Button>
      </div>
      </div>

      <div className='hero-right'>
          <img src='/images/bowl5.jpg'></img>
      </div>
      

    </div>
    <div className='footer'>
    <Footer />
 </div>
 </>
    
  );
}

export default HeroSection;

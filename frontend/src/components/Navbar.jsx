import React, { use } from 'react';
import {useState, useEffect} from 'react';
import {Link} from 'react-router-dom';
import './Navbar.css'
import Button from './Button.jsx';

const Navbar = () => {

    const [click, setClick] = useState(false);
    const [button, setButton] = useState(true);

    const handleClick = () => setClick(!click);
    const closeMobileMenu = () => setClick(false);
    const showButton = () => {
        if(window.innerWidth <= 960){
            setButton(false);
        }
        else{
            setButton(true);
        }
    }

    useEffect( () => {
        showButton();
    }, []);

    window.addEventListener('resize',showButton)

  return (
    <>
    <nav className='navbar'>
        <div className='navbar-container'>
            <Link to="/" className="navbar-logo" onClick={closeMobileMenu}>
               <label className='title'>Nutrition Assistant</label> &nbsp;   <i className='fas fa-clipboard-list'/>
            </Link>
            <div className='menu-icon' onClick={handleClick}>
                <i className={click ? 'fas fa-times' : 'fas fa-bars'}  />
            </div>
            <ul className={click ? 'nav-menu active' : 'nav-menu'}>
                <li className='nav-item'>
                    <Link to='/' className='nav-links' onClick={closeMobileMenu}>
                        Home
                    </Link>
                </li>
                <li className='nav-item'>
                    <Link to='/logout' className='nav-links' onClick={closeMobileMenu}>
                        Logout
                    </Link>
                </li>
                <li className='nav-item'>
                    <Link to='/login' className='nav-links' onClick={closeMobileMenu}>
                        Login
                    </Link>
                </li>
                <li className='nav-item'>
                    <Link to='/sign-up' className='nav-links-mobile' onClick={closeMobileMenu}>
                        Sign Up
                    </Link>
                </li>
            </ul>
            {button && <Link to="/sign-up"><Button buttonStyle='btn--outline'>SIGN UP</Button></Link>}
        </div>
    </nav>
    </>
  )
}

export default Navbar
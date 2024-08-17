import React from 'react';
import { useLocation } from 'react-router-dom';
import './Navbar.css';

const Navbar = ({user, setUser, location}) => {
    const logout = () => {
        setUser({});
        localStorage.removeItem("user");
    }
    return (
        <nav className='navbar'>
            <ul>
                {user.username && <li className={location === "/wordle" ? "active-breadcrumb" : undefined}><a href="/wordle">Play</a></li>}
                {user.username && <li className={location === "/wordleN" ? "active-breadcrumb" : undefined}><a href="/wordleN">6,7,8 Letter Wordle</a></li>}
                {user.username && <li className={location === "/achievements" ? "active-breadcrumb" : undefined}><a href="/achievements">Achievements</a></li>}
                <li className={location === "/leaderboard" ? "active-breadcrumb" : undefined}><a href="/leaderboard">Leaderboard</a></li>
                {!user.username && <li className={location === "/login" ? "active-breadcrumb" : undefined}><a href="/login">Login</a></li>}
                {!user.username && <li className={location === "/signup" ? "active-breadcrumb" : undefined}><a href="/signup">Signup</a></li>}
                {user.username && <li onClick={logout}><a>Logout</a></li>}
            </ul>
        </nav>
    );
};

export default Navbar;
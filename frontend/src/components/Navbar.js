import React from 'react';
import './Navbar.css';

const Navbar = ({user, setUser}) => {
    const logout = () => {
        setUser({});
        localStorage.removeItem("user");
    }
    return (
        <nav className='navbar'>
            <ul>
                {user.username && <li><a href="/wordle">Play</a></li>}
                <li><a href="/leaderboard">Leaderboard</a></li>
                {!user.username && <li><a href="/login">Login</a></li>}
                {!user.username && <li><a href="/signup">Signup</a></li>}
                {user.username && <li onClick={logout}><a>Logout</a></li>}
            </ul>
        </nav>
    );
};

export default Navbar;
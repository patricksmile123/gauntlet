import React, { useState } from 'react';
import './Login.css';


function Login({setUser}) {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [errors, setErrors] = useState({});

    const handleSubmit = async (e) => {
        e.preventDefault();
        console.log("Using the handleSubmit function");
        try {
            const response = await fetch('/api/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ username, password })
            });
            if (!response.ok) {
                    alert('Username or Password was incorrect');
            } else {
                const data = await response.json();
                console.log('Success:', data);
                setUser(data);
                // Handle success (e.g., redirect to another page or update the UI)
            }
            // Handle response here if needed
        } catch (error) {
            console.error('Error! HELP!', error);
        }
    };

    return (
        <div class="loginDiv">
            <h1>Login</h1>
            <form onSubmit={handleSubmit}>
                <label>
                    Username:
                    <input
                        type="text"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                    />
                </label>
                <br />
                <label>
                    Password:
                    <input
                        type="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                    />
                </label>
                <br />
                <button type="submit">Login</button>
            </form>
        </div>
    );
}

export default Login;
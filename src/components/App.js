import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import Wordle from './Wordle';
import './App.css';
import Signup from './Signup';
import Login from './Login';
import Logout from './Logout';	
import Leaderboard from './Leaderboard';
import Navbar from './Navbar';


function App() {
	const [user, setUser] = useState({});
	useEffect(() => {
		JSON.stringify(user) === "{}" && localStorage.getItem("user") && setUser(JSON.parse(localStorage.getItem("user")))
		JSON.stringify(user) !== "{}" && localStorage.setItem("user", JSON.stringify(user))
		console.log(user)
	}, [user]);
	return (
		<><Navbar user={user} setUser={setUser}/>
		
	  <div className="content">
		<Router>
			<Routes>
				<Route path="/leaderboard" element={<Leaderboard />} />
			{!!(user.username) && <>
				<Route path="/wordle" element={<Wordle user={user} />} />
			</>}
			{!(user.username) && <>
				<Route path="/signup" element={<Signup user={user} />}/>
				<Route path="/login" element={<Login user={user} setUser={setUser}/>}/>
			</>}
			<Route path="*" element={<Navigate user={user} to={!!(user.username) ? "/wordle" : "/login"}/>} /> 
			</Routes>
		</Router>
	  </div>
	  </>
	);
  }

export default App;

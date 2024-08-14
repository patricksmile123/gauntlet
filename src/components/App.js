import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate, json } from 'react-router-dom';
import Wordle from './Wordle';
import './App.css';
import Signup from './Signup';
import Login from './Login';
import LocationProvider from './LocationProvider';
import Leaderboard from './Leaderboard';
import Navbar from './Navbar';
import Achievements from './Achievements';
import { SnackbarProvider, VariantType, useSnackbar } from 'notistack';



function App() {
	const [user, setUser] = useState(localStorage.getItem("user") ? JSON.parse(localStorage.getItem("user")) : {});
	const [location, setLocation] = useState("");

	useEffect(() => {
		JSON.stringify(user) === "{}" && localStorage.getItem("user") && setUser(JSON.parse(localStorage.getItem("user")))
		JSON.stringify(user) !== "{}" && localStorage.setItem("user", JSON.stringify(user))
		console.log(`app ${JSON.stringify(user)}`)
	}, [user]);

	return (
		<><Navbar user={user} setUser={setUser} location={location}/>
		<SnackbarProvider maxSnack={10}>
	  <div className="content">
		<Router>
			<Routes>
			{!!(user.username) && <>
				<Route path="/wordle" element={<Wordle user={user} />} />
				<Route path="/achievements" element={<Achievements user={user} />} />
				<Route path="/leaderboard" element={<Leaderboard user={user} />} />
			</>}
			{!(user.username) && <>
				<Route path="/signup" element={<Signup user={user} />}/>
				<Route path="/login" element={<Login user={user} setUser={setUser}/>}/>
				<Route path="/leaderboard" element={<Leaderboard user={user} />} />
			</>}
			<Route path="*" element={<Navigate user={user} to={!!(user.username) ? "/wordle" : "/login"}/>} /> 
			</Routes>
			<LocationProvider setLocation={setLocation} />
		</Router>
	  </div>
	  </SnackbarProvider>
	  </>
	);
  } 

export default App;

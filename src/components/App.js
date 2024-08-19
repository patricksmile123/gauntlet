import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate, json, useSearchParams, useLocation } from 'react-router-dom';
import Wordle from './Wordle';
import './App.css';
import LocationProvider from './LocationProvider';
import { SnackbarProvider, VariantType, useSnackbar } from 'notistack';



function App() {
	const [user, setUser] = useState(localStorage.getItem("user") ? JSON.parse(localStorage.getItem("user")) : {});
	const [location, setLocation] = useState("");
	const [wordLength, setWordLength] = useState(0);

	useEffect(() => {
		JSON.stringify(user) === "{}" && localStorage.getItem("user") && setUser(JSON.parse(localStorage.getItem("user")))
		JSON.stringify(user) !== "{}" && localStorage.setItem("user", JSON.stringify(user))
	}, [user]);
	let query = ""
	if (location.startsWith("/shared")) {
		query = location.split("/").pop();
	}
	return (
	  <div className="content">
		<Router>
			<Routes>
				<Route path="*" element={<Wordle user={user} />} /> 
			</Routes>
			<LocationProvider setLocation={setLocation} />
		</Router>
	  </div>
	);
  } 

export default App;

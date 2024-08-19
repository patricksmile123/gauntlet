import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Wordle from './Wordle';
import './App.css';



function App() {

	return (
	  <div className="content">
		<Router>
			<Routes>
				<Route path="*" element={<Wordle />} /> 
			</Routes>
		</Router>
	  </div>
	);
  } 

export default App;

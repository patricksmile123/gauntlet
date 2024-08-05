import React, { useState, useEffect } from 'react';
import './App.css';
import Keyboard from './Keyboard';


function Wordle({user}) {
    const [guess, setGuess] = useState("");
    const [letterData, setResult] = useState([]);
    const [isLoss, setIsLoss] = useState(false)
    const [isWin, setIsWin] = useState(false)
    const [isDisabled, setDisabled] = useState(false)
    const [keyDictionary, setKeyDictionary] = useState([
        { "key": "Q", "state": "" },
        { "key": "W", "state": "" },
        { "key": "E", "state": "" },
        { "key": "R", "state": "" },
        { "key": "T", "state": "" },
        { "key": "Y", "state": "" },
        { "key": "U", "state": "" },
        { "key": "I", "state": "" },
        { "key": "O", "state": "" },
        { "key": "P", "state": "" },
        { "key": "A", "state": "" },
        { "key": "S", "state": "" },
        { "key": "D", "state": "" },
        { "key": "F", "state": "" },
        { "key": "G", "state": "" },
        { "key": "H", "state": "" },
        { "key": "J", "state": "" },
        { "key": "K", "state": "" },
        { "key": "L", "state": "" },
        { "key": "Z", "state": "" },
        { "key": "X", "state": "" },
        { "key": "C", "state": "" },
        { "key": "V", "state": "" },
        { "key": "B", "state": "" },
        { "key": "N", "state": "" },
        { "key": "M", "state": "" }
    ]);

    useEffect(() => {
        const fetchData = async () => {
            console.log("hello")
        const response = await fetch('/api/createGame', {
            method: 'GET',
            headers: { 
                'authorization': `Bearer ${user.token}`
            },
        });
        if (response.ok) {
            const data = await response.json();
            console.log(data);
            setResult(data.map(previousGuess => {
                console.log(previousGuess);  
                let tempData = {
                }
                for (let i = 0; i < 5; i++) {
                        let currentLetter = previousGuess.guess.charAt(i).toUpperCase()
                        tempData["l"+ i] = {"letter": currentLetter,"result": previousGuess.result[i]}
                        for (let j = 0; j < keyDictionary.length; j++){
                            if (keyDictionary[j].key.toUpperCase() == currentLetter){
                                keyDictionary[j].state = previousGuess.result[i]
                                console.log(keyDictionary[j].key)
                            }
                    }
                }
                return tempData
            }));
        }}
        fetchData().catch(console.error);
    }, [])

    const handleGuess = async () => {
    try {
        if (guess.length !== 5){
            return
        }
        console.log("Sending guess:", { guess });
        const response = await fetch('/api/guess', {
            method: 'POST',
            headers: {
                'authorization': `Bearer ${user.token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ guess: guess})
        });

        if (response.ok) {
            const data = await response.json();
            console.log(data);  
            let tempData = {
            }
            if (data.result.every(val=>val === "correct")){
                setIsWin(true)
                setDisabled(true)
            }
            else if (data.guessCount >= 5){
                console.log("hello")
                setIsLoss(true)
                setDisabled(true)
            }
            for (let i = 0; i < 5; i++) {
                    let currentLetter = guess.charAt(i).toUpperCase()
                    tempData["l"+ i] = {"letter": currentLetter,"result": data.result[i]}
                    for (let j = 0; j < keyDictionary.length; j++){
                        if (keyDictionary[j].key.toUpperCase() == currentLetter){
                            keyDictionary[j].state = data.result[i]
                            console.log(keyDictionary[j].key)
                        }
                }
                setResult([
                    ...letterData,
                    tempData
                ])
                console.log(letterData)
            }
        }
     } catch (error) {
    }
    };
    const handleKeyPress = (letter) => { 
        if (guess.length < 5) {
            setGuess(`${guess}${letter}` )
        }
    }

    return (
        <div className="App">
            <header className="App-header">
                <h1>Wordle</h1>
                <input
                    type="text"
                    value={guess}
                    onChange={(e) => setGuess(e.target.value)}
                    minLength={5}
                    maxLength={5}
                />
                <button disabled={isDisabled} onClick={handleGuess}>Submit Guess</button>	
                <table className="guessTable">{letterData.map(entry => (
                    <tr>
                        <td className={entry.l0.result}>{entry.l0.letter}</td>
                        <td className={entry.l1.result}>{entry.l1.letter}</td>
                        <td className={entry.l2.result}>{entry.l2.letter}</td>
                        <td className={entry.l3.result}>{entry.l3.letter}</td>
                        <td className={entry.l4.result}>{entry.l4.letter}</td>
                    </tr>))}
                </table>
                {isWin? (
                    <div>Win!</div>
                ):(<div></div>)}				
                {isLoss? (
                    <div>Loss</div>
                ):(<div></div>)}
            </header>
            <Keyboard keyDictionary={keyDictionary} onKeyPress={handleKeyPress} />
        </div>
    );
}
    export default Wordle;
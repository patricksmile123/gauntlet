import React, { useState, useEffect } from 'react';
import './App.css';
import Keyboard from './Keyboard';
import { SnackbarProvider, VariantType, useSnackbar } from 'notistack';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';
import Modal from '@mui/material/Modal';
import Tooltip from '@mui/material/Tooltip';

const style = {
    position: 'absolute',
    top: '50%',
    left: '50%',
    transform: 'translate(-50%, -50%)',
    width: 400,
    bgcolor: '#5c5470',
    border: '2px solid #000',
    boxShadow: 24,
    p: 4,
};

function Wordle({user}) {
    console.log(`Wordle ${JSON.stringify(user)}`)
    const [guess, setGuess] = useState("");
    const [letterData, setResult] = useState([]);
    const [isLoss, setIsLoss] = useState(false)
    const [isWin, setIsWin] = useState(false)
    const [allowSend, setAllowSend] = useState(true)
    const [isDisabled, setDisabled] = useState(false)
    const [answer, setAnswer] = useState("")
    const [showOutcomeModal, setShowOutcomeModal] = useState(false)
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

    const { enqueueSnackbar } = useSnackbar();
    
    const share = async () => {
        try {
            const response = await fetch('/api/createSharedGame', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ answer: answer})
            })
            if (response.ok) {
                const data = await response.json();
                navigator.clipboard.writeText(`${window.location.origin}/shared/${data.uuid}`)
                enqueueSnackbar('Link copied to clipboard')
            }
        }
        catch (error) {
            console.error(error)
        }
    }

    useEffect(() => {
        const fetchData = async () => {
        const response = await fetch('/api/createGame', {
            method: 'GET',
            headers: {
                'shareduuid' : window.location.pathname.split("/").pop(),
                'authorization': `Bearer ${user.token}`
            },
        });
        if (response.ok) {
            const data = await response.json();
            setResult(data.map(previousGuess => {
                let tempData = {
                }
                for (let i = 0; i < 5; i++) {
                        let currentLetter = previousGuess.guess.charAt(i).toUpperCase()
                        tempData["l"+ i] = {"letter": currentLetter,"result": previousGuess.result[i]}
                        setKeyDictionary(keyDictionary.map(entry => {
                            if (entry.key.toUpperCase() === currentLetter){
                                entry.state = data.result[i]
                            }
                            return entry
                        }))
                }
                return tempData
            }));
        }}
        fetchData().catch(console.error);
    }, [])

    const backspace = () => {
        setGuess(guess.slice(0, -1))
    }

    const handleGuess = async () => {
        if (allowSend) {
            try {
                if (guess.length !== 5){
                    return
                }
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
                    data.new_achievements.forEach(achievement => {
                        enqueueSnackbar(`🏆 ${achievement}`)
                    })

                    setGuess('')
                    
                    let tempData = {
                    }
                    if (data.result.every(val=>val === "correct")){
                        setIsWin(true)
                        setAnswer(guess)
                        setShowOutcomeModal(true)
                        setDisabled(true)
                    }
                    else if (data.guessCount >= 6){
                        setIsLoss(true)
                        setAnswer(data.answer)
                        setShowOutcomeModal(true)
                        setDisabled(true)
                    }
                    for (let i = 0; i < 5; i++) {
                            let currentLetter = guess.charAt(i).toUpperCase()
                            tempData["l"+ i] = {"letter": currentLetter,"result": data.result[i]}
                            setKeyDictionary(keyDictionary.map(entry => {
                                if (entry.key.toUpperCase() === currentLetter){
                                    entry.state = data.result[i]
                                }
                                return entry
                            }))
                        setResult([
                            ...letterData,
                            tempData
                        ])
                    }
                    setAllowSend(true)
                }
            } catch (error) {
            }
        }
    };
    const handleKeyPress = (letter) => { 
        if (guess.length < 5) {
            setGuess(`${guess}${letter}` )
        }
    }

    const playAgain = () => {
        setGuess("")
        setResult([])
        setIsLoss(false)
        setIsWin(false)
        setDisabled(false)
        setAnswer("")
        setShowOutcomeModal(false)
        setKeyDictionary(keyDictionary.map(entry => {
            entry.state = ""
            return entry
        }))
        const fetchData = async () => {
            const response = await fetch('/api/createGame', {
                method: 'GET',
                headers: { 
                    'authorization': `Bearer ${user.token}`
                },
            });
            if (response.ok) {
                const data = await response.json();
                setResult(data.map(previousGuess => {
                    let tempData = {
                    }
                    for (let i = 0; i < 5; i++) {
                            let currentLetter = previousGuess.guess.charAt(i).toUpperCase()
                            tempData["l"+ i] = {"letter": currentLetter,"result": previousGuess.result[i]}
                            for (let j = 0; j < keyDictionary.length; j++){
                                if (keyDictionary[j].key.toUpperCase() === currentLetter){
                                    keyDictionary[j].state = previousGuess.result[i]
                                }
                        }
                    }
                    return tempData
                }));
            }}
            fetchData().catch(console.error);
    }

    return (
        <SnackbarProvider maxSnack={10}>
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
                <button disabled={isDisabled && !allowSend} onClick={handleGuess}>Submit Guess</button>	
                <table className="guessTable">{letterData.map(entry => (
                    <tr>
                        <td className={entry.l0.result}>{entry.l0.letter}</td>
                        <td className={entry.l1.result}>{entry.l1.letter}</td>
                        <td className={entry.l2.result}>{entry.l2.letter}</td>
                        <td className={entry.l3.result}>{entry.l3.letter}</td>
                        <td className={entry.l4.result}>{entry.l4.letter}</td>
                    </tr>))}
                </table>				
                {isLoss? (<>
                    <Typography variant='h6'>The answer was {answer}</Typography>
                    </>
                ):(<div></div>)}
            </header>
            <Keyboard handleGuess={handleGuess} backspace={backspace} keyDictionary={keyDictionary} onKeyPress={handleKeyPress} />
            <Modal
                open={showOutcomeModal}
                onClose={() => setShowOutcomeModal(false)}
                aria-labelledby="modal-modal-title"
                aria-describedby="modal-modal-description"
            >
                <Box sx={style}>
                <Typography id="modal-modal-title" variant="h6" component="h2">
                    {isWin? "You Won, congratulations!" : "You Lost, better luck next time!"}
                </Typography>
                <Button onClick={playAgain}>Play Again</Button>
                <Tooltip title="Copy share link to clipboard" placement="top"><Button onClick={share}>Share this game</Button></Tooltip>
                <button onClick={() => setShowOutcomeModal(false)}>Close</button>
                </Box>
            </Modal>
        </div>
        </SnackbarProvider>
    );
}
    export default Wordle;
import React from 'react';
import Key from './Key';

// [
//   { "key": "Q", "state": "GUESSED_CORRECT" },
//   { "key": "W", "state": "GUESSED_DISABLED" },
//   { "key": "E", "state": "GUESSED_WRONG_PLACE" }
// ]

const Keyboard = ({onKeyPress, keyDictionary, handleGuess, backspace}) => {
    const keyPressed = (letter) => () =>{
        console.log("Key Pressed: ", letter);
        onKeyPress(letter);
    }
    document.addEventListener('keyup', (e) => {
        if (e.code === "Enter") {
            handleGuess();
        }
    })
    return ( 
        <div className="keyboard">
            {keyDictionary.map((entry) => <Key letter={entry.key} key={entry.key} onClick={keyPressed(entry.key)} state={entry.state} /> )}
            <Key letter="↵" onClick={handleGuess} state="" />
            <Key letter="⌫" onClick={backspace} state="" />
        </div>
    );
};

export default Keyboard;
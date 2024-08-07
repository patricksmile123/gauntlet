import React from 'react';
import Key from './Key';

// [
//   { "key": "Q", "state": "GUESSED_CORRECT" },
//   { "key": "W", "state": "GUESSED_DISABLED" },
//   { "key": "E", "state": "GUESSED_WRONG_PLACE" }
// ]

const Keyboard = ({onKeyPress, keyDictionary}) => {
    const keyPressed = (letter) => () =>{
        console.log("Key Pressed: ", letter);
        onKeyPress(letter);
    }
    return ( 
        <div className="keyboard">
            {keyDictionary.map((entry) => <Key letter={entry.key} key={entry.key} onClick={keyPressed(entry.key)} state={entry.state} /> )}
        </div>
    );
};

export default Keyboard;
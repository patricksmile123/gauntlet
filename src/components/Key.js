import React from 'react';



function Key({ letter, onClick, state }) {
    
    return (
        <button onClick={onClick}>
            {letter}
        </button>
    );
}

export default Key;
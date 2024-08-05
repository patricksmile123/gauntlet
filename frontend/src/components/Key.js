import React from 'react';



function Key({ letter, onClick, state }) {
    
    return (
        <button onClick={onClick} class={state}>
            {letter}
        </button>
    );
}

export default Key;
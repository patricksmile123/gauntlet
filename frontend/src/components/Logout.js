import React, { useEffect } from 'react';

function Logout({setUser}) {
   useEffect(() => {
    setUser({});
    localStorage.removeItem("user");
   }, []);

    return (
        <div>
        </div>
    );
}

export default Logout;

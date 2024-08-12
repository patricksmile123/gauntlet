import React from 'react';
import { useLocation } from 'react-router-dom';

const LocationProvider = ({setLocation}) => {
    const location = useLocation();
    setLocation(location.pathname);
    return <></>;
}

export default LocationProvider

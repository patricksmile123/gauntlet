import React, { useEffect } from 'react';

const [achievement, setAchievement] = useState([]);

const Achievements = ({user}) => {

    useEffect(() => {
        console.log(user)
        const fetchData = async () => {
            const response = await fetch('/api/achievement_getter', {
                method: 'GET',
                headers: { 'authorization': `Bearer ${user.token}`,
                },
                body: JSON.stringify({user})
            });
            if (response.ok) {
                const data = await response.json();
                console.log(data);
                setAchievement(data);
            } 
            else {
                console.log('An error occurred');}
        }, []});
        fetchData().catch(console.error);

    return (
        <div>
            <h1>Achievements</h1>
            <ul>
                {achievement.map((achievement) => (
                    <li key={achievement.id}>{achievement.name}</li>
                ))}
            </ul>
        </div>
    );
};

export default Achievements;
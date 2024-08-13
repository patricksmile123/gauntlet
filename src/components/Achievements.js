import React, { useEffect, useState } from 'react';
import './Achievements.css';

function Achievements ({user}) {
    const [achievement, setAchievement] = useState([]);
    useEffect(() => {
        if (!user.token) {
            console.log('No token available');
            return;
        }

        const fetchData = async () => {
            try {
                const response = await fetch('/api/achievement_getter', {
                    method: 'POST',
                    headers: {
                        'Authorization': `Bearer ${user.token}`,
                    },
                });

                if (response.ok) {
                    const data = await response.json();
                    console.log(data);
                    setAchievement(data);
                } else {
                    console.log('An error occurred while fetching the achievements');
                }
            } catch (error) {
                console.error('Error fetching data:', error);
            }
        };
        fetchData();
    }, [user.token]); 

    return (
        <div>
            <h1 className="AchievementHeader">Achievements</h1>
            <ul className="AchievementList">
                {achievement.map((achievement) => (
                    <li className="AchievementData" key={achievement.id}>{achievement.name}</li>
                ))}
            </ul>
        </div>
    );
}

export default Achievements;

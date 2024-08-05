import React, { useEffect, useState } from 'react';
import './Leaderboard.css';

const Leaderboard = () => {
    const [scores, setScores] = useState([]);

    useEffect(() => {
        // Fetch leaderboard scores from JSON API
        const fetchScores = async () => {
            try {
                const response = await fetch('/api/leaderboard');
                const data = await response.json();
                setScores(data);
            } catch (error) {
                console.error('Error fetching leaderboard scores:', error);
            }
        };
        fetchScores();
    }, []);

    return (
        <div className="leaderboardDiv">
            <h1>Leaderboard</h1>
            <table className="leaderboardTable">
                <thead>
                    <tr>
                        <th>Rank</th>
                        <th>Username</th>
                        <th>Average Score</th>
                        <th>Average Time</th>

                    </tr>
                </thead>
                <tbody>
                    {scores.map((score, index) => (
                        <tr key={index}>
                            <td>{score.rank}</td>
                            <td>{score.firstname}</td>
                            <td>{score.averageScore}</td>
                            <td>{score.averageTime}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

export default Leaderboard;
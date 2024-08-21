import React, { useEffect, useState } from 'react';
import './Leaderboard.css';

const Leaderboard = ({user}) => {
    const [leaderboard1, setLeaderboard1] = useState([]);
    const [leaderboard2, setLeaderboard2] = useState([]);
    const [leaderboard3, setLeaderboard3] = useState([]);
    const [leaderboard4, setLeaderboard4] = useState([]);

    console.log(`Leaderboard ${JSON.stringify(user)}`)

    useEffect(() => {
        const fetchScores = async () => {
            try {
                const response = await fetch('/api/leaderboard');
                const data = await response.json();
                
                // Assuming the data is an array of arrays
                const [leaderboard1, leaderboard2, leaderboard3, leaderboard4] = data;
    
                setLeaderboard1(leaderboard1);
                setLeaderboard2(leaderboard2);
                console.log(`Leaderboard 6 ${JSON.stringify(leaderboard2)}`)
                setLeaderboard3(leaderboard3);
                setLeaderboard4(leaderboard4);
            } catch (error) {
                console.error('Error fetching leaderboard scores:', error);
            }
        };
        fetchScores();
    }, []);
    

    return (
        <div className="leaderboardDiv">
            <h1>Leaderboard for 5 letters</h1>
            <table className="leaderboardTable">
                <thead>
                    <tr>
                        <th>Rank</th>
                        <th>Username</th>
                        <th>Average Score</th>
                        <th>Average Time(s)</th>

                    </tr>
                </thead>
                <tbody>
                    {leaderboard1.map((leaderboard1, index) => (
                        <tr key={index}>
                            <td>{leaderboard1.rank}</td>
                            <td>{leaderboard1.firstname}</td>
                            <td>{leaderboard1.averageScore}</td>
                            <td>{leaderboard1.averageTime}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
            <h2>Leaderboard for 6 letters</h2>
            <table className="leaderboardTable">
                <thead>
                    <tr>
                        <th>Rank</th>
                        <th>Username</th>
                        <th>Average Score</th>
                        <th>Average Time(s)</th>
                    </tr>
                </thead>
                <tbody>
                    {leaderboard2.map((leaderboard2, index) => (
                        <tr key={index}>
                            <td>{leaderboard2.rank6}</td>
                            <td>{leaderboard2.firstname6}</td>
                            <td>{leaderboard2.averageScore6}</td>
                            <td>{leaderboard2.averageTime6}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
            <h3>Leaderboard for 7 letters</h3>
            <table className="leaderboardTable">
                <thead>
                    <tr>
                        <th>Rank</th>
                        <th>Username</th>
                        <th>Average Score</th>
                        <th>Average Time(s)</th>
                    </tr>
                </thead>
                <tbody>
                    {leaderboard3.map((leaderboard3, index) => (
                        <tr key={index}>
                            <td>{leaderboard3.rank7}</td>
                            <td>{leaderboard3.firstname7}</td>
                            <td>{leaderboard3.averageScore7}</td>
                            <td>{leaderboard3.averageTime7}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
            <h4>Leaderboard for 8 letters</h4>
            <table className="leaderboardTable">
                <thead>
                    <tr>
                        <th>Rank</th>
                        <th>Username</th>
                        <th>Average Score</th>
                        <th>Average Time(s)</th>
                    </tr>
                </thead>
                <tbody>
                    {leaderboard4.map((leaderboard4, index) => (
                        <tr key={index}>
                            <td>{leaderboard4.rank8}</td>
                            <td>{leaderboard4.firstname8}</td>
                            <td>{leaderboard4.averageScore8}</td>
                            <td>{leaderboard4.averageTime8}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

export default Leaderboard;
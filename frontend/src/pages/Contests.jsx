import { useState, useEffect } from "react";
import Header from "../components/Header";
import Navbar from "../components/Navbar";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

export default function Contests() {
    const [contests, setContests] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        fetch(`${API_BASE_URL}/contestList`)
            .then(res => {
                if (!res.ok) {
                    throw new Error("Failed to fetch");
                }
                return res.json();
            })
            .then(data => {
                setContests(data);
                setLoading(false);
            })
            .catch(err => {
                setError(err.message);
                setLoading(false);
            });
    }, []);

    if (loading) return <p>Loading contests...</p>;
    if (error) return <p>Error loading contests: {error}</p>;


    return (
        <div>
            <Header />
            <Navbar />
            <h1>Contests</h1>
            <table>
                <thead>
                    <tr>
                        <th>#</th>
                        <th>Name</th>
                        <th>Start</th>
                        <th>Duration</th>
                        <th>Action</th>
                    </tr>
                </thead>
                <tbody>
                    {contests.map((contest) => { 
                        const startTime = new Date(contest.start_time);
                        const endTime = new Date(startTime.getTime() + contest.duration * 60000);
                        const now = new Date();

                        console.log(`Contest ID: ${contest.id}, Start Time: ${startTime}, End Time: ${endTime}, Now: ${now}`);

                        return <tr key={contest.id}>
                            <td>{contest.id}</td>
                            <td>
                                {contest.title}

                                {contest.isInProgress && <span>(in progress)</span>}
                                {(() => {
                                    return now >= startTime && now <= endTime ? <span> (in progress)</span> : null;
                                })()}
                               
                            </td>
                            <td>{new Date(contest.start_time).toLocaleString()}</td>
                            <td>{contest.duration} minutes</td>
                            <td>
                                {
                                    (now > startTime) && 
                                    <a href={`/contest/${contest.id}/problems`}>Enter</a>
                                }
                            </td>
                        </tr>
                    })}
                </tbody>
            </table>
        </div>
    );
}

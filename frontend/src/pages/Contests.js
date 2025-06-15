import { useState, useEffect } from "react";
import Header from "../components/Header";
import Navbar from "../components/Navbar";

export default function Contests() {
    const [contests, setContests] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        fetch("http://127.0.0.1:5001/api/contestList")
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
                        <th>ID</th>
                        <th>Name</th>
                        <th>Start</th>
                        <th>Enter</th>
                    </tr>
                </thead>
                <tbody>
                    {contests.map(contest => (
                        <tr key={contest.id}>
                            <td>{contest.id}</td>
                            <td>{contest.title}</td>
                            <td>{new Date(contest.start_time).toLocaleString()}</td>
                            <td><a href={`/contest/${contest.id}/problems`}>Enter</a></td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}

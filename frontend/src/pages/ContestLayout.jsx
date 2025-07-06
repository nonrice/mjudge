import { Link, Outlet, useParams } from 'react-router-dom';
import Header from "../components/Header";
import Navbar from "../components/Navbar";
import { useState, useEffect } from "react";

import { use } from 'react';

import CountdownTimer from '../components/CountdownTimer';
import { calcOffset } from '../utils/contestTiming';
import useSWR from 'swr';
import { fetcher } from '../utils/fetcher';

export default function ContestLayout() {
    const { contestId } = useParams();

    const [ title, setTitle ] = useState("");
    const [ loading, setLoading ] = useState(true);
    const [ error, setError ] = useState(null);
    useEffect(() => {
        fetch(`http://127.0.0.1:5001/api/contest/${contestId}/title`).then(res => {
            if (!res.ok) {
                throw new Error("Failed to fetch contest title");
            }
            return res.json();
        }).then(data => {
            setTitle(data.title);
            setLoading(false);
        }).catch(err => {
            setError(err.message);
            setLoading(false);
        });
    }, [contestId]);

    
    const { data: timingData, error: timingError } = useSWR([`http://127.0.0.1:5001/api/contest/${contestId}/timing`, {}], fetcher);
    const offset = calcOffset();

    return (
    <div>
    <Header />
    <Navbar />
    <div style={{ textAlign: "center" }}>
        <h1>
            {title}<br></br>
            <code>{timingData && offset !== undefined && (
                <CountdownTimer timingData={timingData} offsetPromise={offset} />
            )}</code>
        </h1>
        <nav>
        <Link to={`/contest/${contestId}/problems`}>Problems</Link>
        <Link to={`/contest/${contestId}/standings`}>Standings</Link>
        <Link to={`/contest/${contestId}/mysubmissions`}>My Submissions</Link>
        </nav>
    </div>
    <br></br>
    <Outlet />
    </div>
    );
}
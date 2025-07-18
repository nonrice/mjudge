import { Link, Outlet, useParams } from 'react-router-dom';
import Header from "../components/Header";
import Navbar from "../components/Navbar";
import { useState, useEffect } from "react";

import { use } from 'react';

import CountdownTimer from '../components/CountdownTimer';
import { calcOffset } from '../utils/contestTiming';
import useSWR from 'swr';
import { fetcher } from '../utils/fetcher';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

export default function ContestLayout() {
    const { contestId } = useParams();

    const [ title, setTitle ] = useState("");
    const [ loading, setLoading ] = useState(true);
    const [ error, setError ] = useState(null);
    const [offset, setOffset] = useState();

    useEffect(() => {
        fetch(`${API_BASE_URL}/contest/${contestId}/title`).then(res => {
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

    useEffect(() => {
        calcOffset().then(setOffset);
    }, []);

    
    const { data: timingData, error: timingError } = useSWR([`${API_BASE_URL}/contest/${contestId}/timing`], fetcher, {
    });

    return (
    <div>
    <Header />
    <Navbar />
    <div style={{ textAlign: "center" }}>
        <h1>
            {title}<br></br>
            <code>{timingData && offset !== undefined && (
                <CountdownTimer timingData={timingData} offset={offset} />
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
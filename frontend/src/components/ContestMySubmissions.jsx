import { useParams } from 'react-router-dom';
import { useEffect, useState } from 'react';
import { getToken } from '../utils/auth'; // Adjust the import path as necessary

import { fetcher } from '../utils/fetcher'; // Adjust the import path as necessary
import useSWR from 'swr';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

export default function ContestMySubmissions() {
    const { contestId } = useParams();

    const token = getToken();
    const { data, error } = useSWR(
        [`${API_BASE_URL}/submissions/${contestId}`, { token }],
        fetcher,
        {
            refreshInterval: 3000,
            refreshWhenHidden: false
        }
    );
    if (!token) {
        return <div>Please log in to view your submissions.</div>;
    }
    if (error) {
        return <div>Error loading submissions: {error.message}</div>;
    }

    if (!data) {
        return <div>Loading...</div>;
    }

    const submissions = data;


    return (
        <div>
            <h2>My Submissions</h2>
            <table>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Letter</th>
                    <th>Language</th>
                    <th>Status</th>
                    <th>Detail</th>
                </tr>
            </thead>
            <tbody>
                {submissions.map(submission => (
                    <tr key={submission.id}>
                        <td>{submission.id}</td>
                        <td>{submission.letter}</td>
                        <td>{submission.language}</td>
                        {
                            (submission.status === "Accepted") ?
                                <td className="accepted">{submission.status}</td>
                            : (
                                (submission.status === "Waiting" || submission.status === "Running") ? 
                                    <td style={{color: "gray"}}>{submission.status}</td>
                                : (
                                    <td>{submission.status}</td>
                                )
                            )
                        }
                        <td>
                            <a href={`/submission/${submission.id}`} target="_blank" rel="noopener noreferrer">View</a>
                            {/* <a href={`/submission/${submission.id}`}>View</a> */}
                        </td>
                    </tr>
                ))}
            </tbody>
            </table>
        </div>
    );
}
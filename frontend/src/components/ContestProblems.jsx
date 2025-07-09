import { useParams } from 'react-router-dom';
import { useEffect, useState } from 'react';

import useSWR from 'swr';
import { fetcher } from '../utils/fetcher';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

export default function ContestProblems() {
    const { contestId } = useParams();

    const { data, error } = useSWR(
        [`${API_BASE_URL}/contest/${contestId}/problems`],
        fetcher
    );
    if (error) return <p>Error loading problems: {error.message}</p>;
    if (!data) return <p>Loading problems...</p>;

    return (
        <div>
            <h2>Problems</h2>
            <table>
                <thead>
                    <tr>
                        <th>#</th>
                        <th>Title</th>
                        <th>Action</th>
                    </tr>
                </thead>
                <tbody>
                    {data.map((problem) => (
                        <tr key={problem.id}>
                            <td>{problem.letter}</td>
                            <td>{problem.title}</td>
                            <td>
                                <a href={`/contest/${contestId}/problem/${problem.letter}`}>View</a>
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}
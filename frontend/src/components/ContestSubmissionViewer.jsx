import { Link, useParams } from 'react-router-dom';
import useSWR from 'swr';
import { getToken } from '../utils/auth';
import { fetcher } from '../utils/fetcher';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

export default function ContestSubmissionViewer({ showBackLink = false }) {
    const { submissionId } = useParams();

    const token = getToken();
    const { data, error } = useSWR(
        [`${API_BASE_URL}/submission/${submissionId}`, { token }],
        fetcher,
        {
            refreshInterval: 3000,
            refreshWhenHidden: false
        }
    );

    if (error) {
        return <div>Error loading submission: {error.message}</div>;
    }

    if (!data) {
        return <div>Loading...</div>;
    }

    const { id, contest_id, problem_letter, problem_name, code, language, status, feedback, timestamp, max_time, max_memory } = data;

    return (
        <div>
            <h1>Submission #{id}</h1>
            <p><strong>Submitted to: </strong><a href={`/contest/${contest_id}/problem/${problem_letter}`}>{contest_id}{problem_letter}. {problem_name}</a></p>
            <p><strong>Timestamp:</strong> {new Date(timestamp).toLocaleString()}</p>
            <p className={status === 'Accepted' ? 'accepted' : ''}><strong>Status:</strong> {status}</p>
            <p><strong>Runtime:</strong> {max_time} ms</p>
            <p><strong>Memory:</strong> {max_memory} KB</p>
            <p><strong>Language:</strong> {language}</p>
            <p><strong>Code:</strong></p>
            <pre><code>{code}</code></pre>
            <p><strong>Feedback:</strong></p>
            <pre><code>{feedback}</code></pre>
        </div>
    );
}
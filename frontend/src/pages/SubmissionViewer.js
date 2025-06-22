import Header from '../components/Header';
import Navbar from '../components/Navbar';

import { useParams } from 'react-router-dom';
import useSWR from 'swr';
import { getToken } from '../utils/auth';
import { fetcher } from '../utils/fetcher';


export default function SubmissionViewer() {
    const { submissionId } = useParams();

    const token = getToken();
    const { data, error } = useSWR(
        [`http://127.0.0.1:5001/api/submissions/${submissionId}`, { token }],
        fetcher
    );

    if (error) {
        return <div>Error loading submission: {error.message}</div>;
    }

    /*
return jsonify({
        "id": submission.id,
        "contest_id": submission.contest_id,
        "problem_letter": problem_letter,
        "code": submission.code,
        "language": submission.language,
        "status": submission.status,
        "feedback": submission.feedback,
        "timestamp": submission.timestamp.isoformat()
    }), 200
    */
    if (!data) {
        return <div>Loading...</div>;
    }

    const { id, contest_id, problem_letter, code, language, status, feedback, timestamp } = data;

    return (
        <div>
            <h2>Submission Details</h2>
            <p><strong>ID:</strong> {id}</p>
            <p><strong>Contest ID:</strong> {contest_id}</p>
            <p><strong>Problem Letter:</strong> {problem_letter}</p>
            <p><strong>Code:</strong></p>
            <pre>{code}</pre>
            <p><strong>Language:</strong> {language}</p>
            <p><strong>Status:</strong> {status}</p>
            <p><strong>Feedback:</strong> {feedback}</p>
            <p><strong>Timestamp:</strong> {new Date(timestamp).toLocaleString()}</p>
        </div>
    );
}
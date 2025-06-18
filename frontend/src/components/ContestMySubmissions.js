import { useParams } from 'react-router-dom';
import { useEffect, useState } from 'react';
import { getToken } from '../utils/auth.js'; // Adjust the import path as necessary


export default function ContestMySubmissions() {
  const { contestId } = useParams();

  const [submissions, setSubmissions] = useState([]);

  useEffect(() => {
    const fetchSubmissions = async () => {
      const token = getToken();
      const response = await fetch(`http://127.0.0.1:5001/api/submissions/${contestId}`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      });

      if (response.ok) {
        const data = await response.json();
        setSubmissions(data);
      } else {
        console.error('Failed to fetch submissions');
      }
    };

    fetchSubmissions();
  }, [contestId]);

  return (
    <div>
      <h2>My Submissions</h2>
      <table>
      <thead>
        <tr>
          <th>ID</th>
          <th>Problem ID</th>
          <th>Language</th>
          <th>Status</th>
        </tr>
      </thead>
      <tbody>
        {submissions.map(submission => (
          <tr key={submission.id}>
            <td>{submission.id}</td>
            <td>{submission.problem_id}</td>
            <td>{submission.language}</td>
            <td>{submission.status}</td>
          </tr>
        ))}
      </tbody>
      </table>
    </div>
  );
}
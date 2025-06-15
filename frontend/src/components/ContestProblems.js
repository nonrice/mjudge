import { useParams } from 'react-router-dom';
import { useEffect, useState } from 'react';

export default function ContestProblems() {
  const { contestId } = useParams();

  const [problems, setProblems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  useEffect(() => {
    fetch(`http://127.0.0.1:5001/api/contest/${contestId}/problems`).then(res => {
      if (!res.ok) {
        throw new Error('Failed to fetch problems');
      }
      return res.json();
    }).then(data => {
      setProblems(data);
      setLoading(false);
    }).catch(err => {
      setError(err.message);
      setLoading(false);
    });
  }, [contestId]);

  if (loading) return <p>Loading problems...</p>;
  if (error) return <p>Error loading problems: {error}</p>;

  return (
    <div>
      <h2>Problems</h2>
      <table>
        <thead>
          <tr>
            <th>#</th>
            <th>Title</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {problems.map((problem) => (
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
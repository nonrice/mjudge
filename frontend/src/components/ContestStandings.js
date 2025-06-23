import useSWR from "swr";
import { useParams } from "react-router-dom";
import { getToken } from "../utils/auth";
import { fetcher } from "../utils/fetcher";


export default function ContestStandings() {
  const { contestId } = useParams();
  const { data, error, isLoading } = useSWR(
    [`http://127.0.0.1:5001/api/contest/${contestId}/leaderboard`, {}],
    fetcher
  )

  if (isLoading) return <p>Loading standings...</p>;
  if (error) return <p>Error loading standings: {error.message}</p>;

  const sorted_legend = Object.keys(data.problem_legend)
    .sort((a, b) => data.problem_legend[a] - data.problem_legend[b]);

  return (
    <div>
      <h2>Standings</h2>
      <table>
        <thead>
          <tr>
            <th>Rank</th>
            <th>User</th>
            <th>Solved</th>
            <th>Score</th>
            {sorted_legend.map((problem, index) => (
            <th key={index}>{problem}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {data.entries.map((entry, index) => (
            <tr key={entry.user_id}>
              <td>{index + 1}</td>
              <td>{entry.username}</td>
              <td>{entry.solved.reduce((acc, curr) => acc + curr, 0)}</td>
              <td>{entry.score}</td>
              {sorted_legend.map((problem, problemIndex) => (
                <td key={problemIndex}>
                  {entry.attempts[problemIndex]}/{entry.solved[problemIndex] ? entry.times[problemIndex] : "--"}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
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
      <table style={{tableLayout: "fixed", width: "100%"}}>
        <colgroup>
          {/* First 4 columns: auto-fit content using minimal width */}
          <col />
          <col />
          <col />
          <col />

          {/* Remaining columns: take equal share of remaining width */}
          {Array.from({ length: sorted_legend.length }).map((_, i) => (
            <col key={i} style={{ width: `${70/ sorted_legend.length }%` }} />
          ))}
        </colgroup>
        <thead>
          <tr>
            <th style={{whiteSpace: "nowrap"}}>#</th>
            <th>User</th>
            <th>=</th>
            <th>*</th>
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
                <td
                  key={problemIndex}
                  className={entry.solved[problemIndex] ? 'accepted' : ''}
                >
                  {entry.attempts[problemIndex] > 0 ? (
                    `${entry.attempts[problemIndex]}/${entry.solved[problemIndex] ? entry.times[problemIndex] : "--"}`
                  ) : (
                    ""
                  )}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
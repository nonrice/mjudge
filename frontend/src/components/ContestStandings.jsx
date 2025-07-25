import useSWR from "swr";
import { useParams } from "react-router-dom";
import { getToken } from "../utils/auth";
import { fetcher } from "../utils/fetcher";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

export default function ContestStandings() {
    const { contestId } = useParams();
    const { data, error, isLoading } = useSWR(
        [`${API_BASE_URL}/contest/${contestId}/leaderboard`, {}],
        fetcher,
        {
            refreshInterval: 3000,
            refreshWhenHidden: false
        }
    )

    if (isLoading) return <p>Loading standings...</p>;
    if (error) return <p>Error loading standings: {error.message}</p>;

    const sorted_legend = Object.keys(data.problem_legend)
        .sort((a, b) => data.problem_legend[a] - data.problem_legend[b]);

    return (
        <div>
            <h2>Standings</h2>
            <table style={{tableLayout: "fixed"}}>
                <colgroup>
                    <col key="rankno" style={{ width: '4em' }} />
                    <col key="name" />
                    <col key="solved" style={{ width: '5em' }} />
                    <col key="score" style={{ width: '5em' }} />
                    {sorted_legend.map((_, index) => (
                        <col key={index} style={{ width: '6em'}} />
                    ))}
                </colgroup>
                <thead>
                    <tr>
                        <th>#</th>
                        <th>User</th>
                        <th>Solves</th>
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
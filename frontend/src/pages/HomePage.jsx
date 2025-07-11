import Header from "../components/Header";
import Navbar from "../components/Navbar";
import useSWR from "swr";
import { fetcher } from "../utils/fetcher";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

export default function HomePage() {

    const { data, error } = useSWR(
        [`${API_BASE_URL}/server_time`],
        fetcher
    );

    return (
        <div>
        <Header />
        <Navbar />
        <h1>Welcome to McLean Judge!</h1>
        <img src="/meow_best.gif" alt="Hi :)" style={{ width: "200px", height: "200px" }} />

        <p>
            Server time:&nbsp;

            <code>
                {
                    data ? new Date(data.now).toUTCString() : "Loading..."
                }
            </code>
        </p>
        <p>Happy coding! &mdash; Eric</p>
        </div>
    );
}
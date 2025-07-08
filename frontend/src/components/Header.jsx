import { getUserFromToken, isExpired, getToken } from "../utils/auth";

export default function Header() {
    const user = getUserFromToken();

    const token = getToken();
    if (token && isExpired(token)) {
        localStorage.removeItem("token");
        window.location.reload();
    }

    return (
        <header>
            <h2>
                McLean Judge
            </h2>
            <p>
                {user ? (
                    <i>
                        Welcome, {user.username}!
                    </i>
                ) : (
                    <i>
                        Not logged in.
                    </i>
                )}
            </p>
        </header>
    );
}
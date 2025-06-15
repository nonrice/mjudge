import { getUserFromToken } from "../utils/auth";

export default function Header() {
    const user = getUserFromToken();

    return (
        <header>
            <h2>McLean Judge</h2>
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
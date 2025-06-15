import { getUserFromToken } from "../utils/auth";

export default function Navbar() {
    const logout = () => {
        localStorage.removeItem("token");
    }

    return (
        <div>
            <nav>
                <a href="/">Home</a>
                <a href="/about">About</a>
                <a href="/contests">Contests</a>

                { !getUserFromToken() && <a href="/login">Login</a> }
                { !getUserFromToken() && <a href="/register">Register</a> }
                { getUserFromToken() && <a href="/" onClick={ logout }>Logout</a> }
            </nav>
        </div>
    );
}
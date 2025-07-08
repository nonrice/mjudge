import { useState } from "react";
import { useNavigate } from "react-router-dom";
import Header from "../components/Header";
import Navbar from "../components/Navbar";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

export default function Login() {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [message, setMessage] = useState("");
    const navigate = useNavigate();


    const handleSubmit = (e) => {
        e.preventDefault();

        fetch(`${API_BASE_URL}/login`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ username, password })
        })
        .then((res) => {
            if (!res.ok) {
                throw new Error("Login failed");
            }
            return res.json();
        })
        .then((data) => {
            localStorage.setItem("token", data.token);
            navigate("/"); // Redirect to home pag`
        })
        .catch((err) => {
            // alert("Login failed. Please check your credentials.");
            setMessage("Login failed. Please check your credentials.");
            console.error(err);
        });
    };


    return (
        <div>
            <Header />
            <Navbar />
            <h1>Login</h1>
            <form onSubmit={handleSubmit}>
                <label>
                    Username:
                    <input type="text" name="username" value={username} onChange = {(e) => setUsername(e.target.value)} />
                </label>
                <br />
                <label>
                    Password:
                    <input type="password" name="password" value={password} onChange={(e) => setPassword(e.target.value)} />
                </label>
                <br />
                <p>{message}</p>
                <button type="submit">Login</button>
            </form>
        </div>
    );
}
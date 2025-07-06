import Header from '../components/Header';
import Navbar from '../components/Navbar';

import { useState } from 'react';

export default function Register() {
    const [message, setMessage] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        const formData = new FormData(e.target);
        const data = {
            username: formData.get('username'),
            password: formData.get('password'),
            confirmPassword: formData.get('confirmPassword'),
        };

        if (!data.username || !data.password || !data.confirmPassword) {
            setMessage('All fields are required.');
            return;
        }
        if (data.password !== data.confirmPassword) {
            setMessage('Passwords do not match.');
            return;
        }

        try {
            const response = await fetch("http://127.0.0.1:5001/api/register", {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data),
            });

            if (response.ok) {
                alert('Registration successful!');
                setMessage('Registration successful! You can now log in.');
            } else {
                const errorData = await response.json();
                console.error('Error:', errorData);
                setMessage(errorData.error || 'Registration failed. Please try again.');
            }
        } catch (error) {
            console.error('Error:', error);
            setMessage(error.error || 'An error occurred. Please try again.');
            alert('An error occurred. Please try again.');
        }
    };

    return (
        <div>
            <Header />
            <Navbar />
            <h1>Register</h1>
            <form onSubmit={handleSubmit}>
                <label>
                    Username:
                    <input type="text" name="username" />
                </label>
                <br />
                <label>
                    Password:
                    <input type="password" name="password" />
                </label>
                <br />
                <label>
                    Confirm Password:
                    <input type="password" name="confirmPassword" />
                </label>
                <p>{ message }</p>
                <button type="submit">Register</button>
            </form>
        </div>
    );
}
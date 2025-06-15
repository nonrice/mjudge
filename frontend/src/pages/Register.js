import Header from '../components/Header';
import Navbar from '../components/Navbar';

export default function Register() {
    const handleSubmit = async (e) => {
        e.preventDefault();
        const formData = new FormData(e.target);
        const data = {
            username: formData.get('username'),
            password: formData.get('password'),
            confirmPassword: formData.get('confirmPassword'),
        };

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
                window.location.href = '/login';
            } else {
                alert('Registration failed. Please try again.');
            }
        } catch (error) {
            console.error('Error:', error);
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
                <br />
                <button type="submit">Signup</button>
            </form>
        </div>
    );
}
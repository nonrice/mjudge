import { jwtDecode } from "jwt-decode";

export function getUserFromToken() {
    const token = localStorage.getItem("token");
    if (!token) return null;
    try {
        return jwtDecode(token);
    } catch {
        return null;
    }
}

export function isExpired(token) {
    if (!token) return true;
    const decoded = jwtDecode(token);
    return decoded.exp * 1000 < Date.now();
}

export function getToken() {
    return localStorage.getItem("token");
}

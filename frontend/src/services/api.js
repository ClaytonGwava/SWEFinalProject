const API_URL = "http://127.0.0.1:8000";


export async function registerUser(userData) {
    const response = await fetch(
        `${API_URL}/auth/register`,
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(userData)
        }
    );

    const data = await response.json();

    if (!response.ok) {
        throw new Error(
            data.detail || "Registration failed"
        );
    }

    return data;
}


export async function loginUser(
    username,
    password
) {
    const formData = new URLSearchParams();

    formData.append(
        "username",
        username
    );

    formData.append(
        "password",
        password
    );

    const response = await fetch(
        `${API_URL}/auth/login`,
        {
            method: "POST",
            headers: {
                "Content-Type":
                    "application/x-www-form-urlencoded"
            },
            body: formData
        }
    );

    const data = await response.json();

    if (!response.ok) {
        throw new Error(
            data.detail || "Login failed"
        );
    }

    return data;
}


export async function getCurrentUser() {
    const token =
        localStorage.getItem("access_token");

    const response = await fetch(
        `${API_URL}/me`,
        {
            headers: {
                Authorization:
                    `Bearer ${token}`
            }
        }
    );

    const data = await response.json();

    if (!response.ok) {
        throw new Error(
            data.detail || "Authentication failed"
        );
    }

    return data;
}


export async function askQuestion(
    question
) {
    const token =
        localStorage.getItem("access_token");

    const response = await fetch(
        `${API_URL}/ask-rag`,
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                Authorization:
                    `Bearer ${token}`
            },
            body: JSON.stringify({
                question
            })
        }
    );

    const data = await response.json();

    if (!response.ok) {
        throw new Error(
            data.detail || "Question failed"
        );
    }

    return data;
}
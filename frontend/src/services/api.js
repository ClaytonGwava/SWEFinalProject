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
    question,
    courseId
) {

    const token =
        localStorage.getItem(
            "access_token"
        );

    const response = await fetch(
        `${API_URL}/ask-rag`,
        {
            method: "POST",

            headers: {
                "Content-Type":
                    "application/json",

                Authorization:
                    `Bearer ${token}`
            },

            body: JSON.stringify({
                question: question,
                course_id: Number(courseId)
            })
        }
    );

    const data =
        await response.json();

    if (!response.ok) {

        throw new Error(
            data.detail ||
            "Failed to ask EduAI"
        );
    }

    return data;
}

export async function getCourses() {

    const token =
        localStorage.getItem("access_token");

    const response = await fetch(
        `${API_URL}/courses/`,
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
            data.detail || "Failed to load courses"
        );
    }

    return data;
}


export async function getMyCourses() {

    const token =
        localStorage.getItem("access_token");

    const response = await fetch(
        `${API_URL}/courses/my-courses`,
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
            data.detail ||
            "Failed to load enrolled courses"
        );
    }

    return data;
}


export async function createCourse(courseData) {

    const token =
        localStorage.getItem("access_token");

    const response = await fetch(
        `${API_URL}/courses/`,
        {
            method: "POST",

            headers: {
                "Content-Type": "application/json",

                Authorization:
                    `Bearer ${token}`
            },

            body: JSON.stringify(courseData)
        }
    );

    const data = await response.json();

    if (!response.ok) {
        throw new Error(
            data.detail ||
            "Failed to create course"
        );
    }

    return data;
}


export async function enrollInCourse(
    courseId
) {

    const token =
        localStorage.getItem("access_token");

    const response = await fetch(
        `${API_URL}/courses/${courseId}/enroll`,
        {
            method: "POST",

            headers: {
                Authorization:
                    `Bearer ${token}`
            }
        }
    );

    const data = await response.json();

    if (!response.ok) {
        throw new Error(
            data.detail ||
            "Failed to enroll"
        );
    }

    return data;
}

export async function uploadCourseDocument(
    courseId,
    file
) {
    const token = localStorage.getItem(
        "access_token"
    );

    const formData = new FormData();

    formData.append("file", file);

    const response = await fetch(
        `${API_URL}/courses/${courseId}/documents`,
        {
            method: "POST",

            headers: {
                Authorization:
                    `Bearer ${token}`
            },

            body: formData
        }
    );

    const data = await response.json();

    if (!response.ok) {
        throw new Error(
            data.detail ||
            "Document upload failed"
        );
    }

    return data;
}

export async function getQuestionHistory() {

    const token =
        localStorage.getItem("access_token");

    const response = await fetch(
        `${API_URL}/questions/my-history`,
        {
            headers: {
                Authorization:
                    `Bearer ${token}`
            }
        }
    );

    const data =
        await response.json();

    if (!response.ok) {

        throw new Error(
            data.detail ||
            "Failed to load question history"
        );
    }

    return data;
}

export async function unenrollFromCourse(courseId) {

    const token =
        localStorage.getItem("access_token");

    const response = await fetch(
        `${API_URL}/courses/${courseId}/unenroll`,
        {
            method: "DELETE",
            headers: {
                Authorization:
                    `Bearer ${token}`
            }
        }
    );

    const data = await response.json();

    if (!response.ok) {
        throw new Error(
            data.detail ||
            "Failed to unenroll"
        );
    }

    return data;
}
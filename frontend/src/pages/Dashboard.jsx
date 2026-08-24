import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { Link } from "react-router-dom";

import {
    getCurrentUser,
    askQuestion,
    getCourses,
    getMyCourses,
    createCourse,
    enrollInCourse,
    unenrollFromCourse,
    getQuestionHistory
} from "../services/api";


function Dashboard() {

    const navigate = useNavigate();

    const [user, setUser] =
        useState(null);

    const [courses, setCourses] =
        useState([]);

    const [myCourses, setMyCourses] =
        useState([]);

    const [selectedCourse, setSelectedCourse] =
        useState("");

    const [question, setQuestion] =
        useState("");

    const [answer, setAnswer] =
        useState("");

    const [sources, setSources] =
        useState([]);

    const [history, setHistory] =
        useState([]);

    const [loading, setLoading] =
        useState(false);

    const [error, setError] =
        useState("");

    const [courseCode, setCourseCode] =
        useState("");

    const [courseName, setCourseName] =
        useState("");

    const [description, setDescription] =
        useState("");


    useEffect(() => {

        loadDashboard();

    }, []);


    async function loadDashboard() {

        try {

            const currentUser =
                await getCurrentUser();

            setUser(currentUser);

            const questionHistory =
                await getQuestionHistory();

            setHistory(questionHistory);

            const allCourses =
                await getCourses();

            setCourses(allCourses);

            if (
                currentUser.role === "student"
            ) {

                const enrolled =
                    await getMyCourses();

                setMyCourses(enrolled);

                if (enrolled.length > 0) {

                    setSelectedCourse(
                        enrolled[0].id
                    );
                }
            }

        } catch (error) {

            console.error(error);

            localStorage.removeItem(
                "access_token"
            );

            navigate("/");

        }
    }


    async function handleCreateCourse(
        event
    ) {

        event.preventDefault();

        setError("");

        try {

            await createCourse({
                course_code: courseCode,
                course_name: courseName,
                description: description
            });

            setCourseCode("");
            setCourseName("");
            setDescription("");

            const updatedCourses =
                await getCourses();

            setCourses(updatedCourses);

        } catch (error) {

            setError(
                error.message
            );
        }
    }


    async function handleEnroll(
        courseId
    ) {

        setError("");

        try {

            await enrollInCourse(
                courseId
            );

            const enrolled =
                await getMyCourses();

            setMyCourses(enrolled);

            setSelectedCourse(
                courseId
            );

        } catch (error) {

            setError(
                error.message
            );
        }
    }


    async function handleUnenroll(courseId) {

        setError("");

        try {

            await unenrollFromCourse(courseId);

            const enrolled =
                await getMyCourses();

            setMyCourses(enrolled);

            if (selectedCourse == courseId) {
                setSelectedCourse(
                    enrolled.length > 0
                        ? enrolled[0].id
                        : ""
                );
            }

        } catch (error) {

            setError(
                error.message
            );
        }
    }

    async function handleAsk(event) {

        event.preventDefault();

        if (!question.trim()) {
            return;
        }

        if (!selectedCourse) {

            setError(
                "Please select a course first."
            );

            return;
        }

        setLoading(true);
        setError("");
        setAnswer("");
        setSources([]);

        try {

            const data =
                await askQuestion(
                    question,
                    selectedCourse
                );

            console.log(
                "ASK-RAG RESPONSE:",
                data
            );

            console.log(
                "ANSWER:",
                data.answer
            );

            setAnswer(
                data.answer
            );

            setSources(data.sources || []);

            const updatedHistory =
                await getQuestionHistory();

            setHistory(updatedHistory);

        } catch (error) {

            setError(
                error.message
            );

        } finally {

            setLoading(false);
        }
    }


    function logout() {

        localStorage.removeItem(
            "access_token"
        );

        navigate("/");
    }


    if (!user) {

        return (
            <div className="loading">
                Loading...
            </div>
        );
    }


    return (

        <div className="dashboard">

            <header
                className="dashboard-header"
            >

                <div>

                    <h1>
                        EduAI
                    </h1>

                    <p>
                        AI-Powered Academic Assistant
                    </p>

                </div>


                <div className="user-section">

                    <span>
                        Welcome, {user.username}
                    </span>

                    <span>
                        Role: {user.role}
                    </span>

                    {user.role === "faculty" && (
                        <Link to="/faculty">
                            <button>
                                Faculty Dashboard
                            </button>
                        </Link>
                    )}

                    <button
                        onClick={logout}
                    >
                        Logout
                    </button>

                </div>

            </header>


            <main
                className="dashboard-content"
            >

                {error && (

                    <div className="error">
                        {error}
                    </div>

                )}


                {/* FACULTY */}

                {user.role === "faculty" && (

                    <section
                        className="question-card"
                    >

                        <h2>
                            Create Course
                        </h2>

                        <form
                            onSubmit={
                                handleCreateCourse
                            }
                        >

                            <label>
                                Course Code
                            </label>

                            <input
                                value={courseCode}
                                onChange={(event) =>
                                    setCourseCode(
                                        event.target.value
                                    )
                                }
                                placeholder="CS425"
                                required
                            />


                            <label>
                                Course Name
                            </label>

                            <input
                                value={courseName}
                                onChange={(event) =>
                                    setCourseName(
                                        event.target.value
                                    )
                                }
                                placeholder="Software Engineering"
                                required
                            />


                            <label>
                                Description
                            </label>

                            <textarea
                                value={description}
                                onChange={(event) =>
                                    setDescription(
                                        event.target.value
                                    )
                                }
                                placeholder="Course description"
                                rows="4"
                            />


                            <button
                                type="submit"
                            >
                                Create Course
                            </button>

                        </form>

                    </section>
                )}


                {/* COURSES */}

                <section
                    className="question-card"
                >

                    <h2>
                        Courses
                    </h2>


                    {courses.length === 0 ? (

                        <p>
                            No courses available.
                        </p>

                    ) : (

                        courses.map(
                            (course) => (

                                <div
                                    key={course.id}
                                    className="course-item"
                                >

                                    <div>

                                        <strong>
                                            {course.course_code}
                                        </strong>

                                        <p>
                                            {course.course_name}
                                        </p>

                                        <small>
                                            {course.description}
                                        </small>

                                    </div>


                                    {user.role ===
                                        "student" && (

                                        <button
                                            onClick={() =>
                                                handleEnroll(
                                                    course.id
                                                )
                                            }
                                        >
                                            Enroll
                                        </button>

                                    )}

                                </div>
                            )
                        )
                    )}

                </section>


                {/* STUDENT COURSES */}

                {user.role === "student" && (

                    <section
                        className="question-card"
                    >

                        <h2>
                            My Courses
                        </h2>

                        {myCourses.length === 0 ? (

                            <p>
                                You are not enrolled
                                in any courses yet.
                            </p>

                        ) : (

                            <>
                                <select
                                    value={selectedCourse}
                                    onChange={(event) =>
                                        setSelectedCourse(
                                            event.target.value
                                        )
                                    }
                                >

                                    {myCourses.map(
                                        (course) => (

                                            <option
                                                key={course.id}
                                                value={course.id}
                                            >
                                                {course.course_code}
                                                {" - "}
                                                {course.course_name}
                                            </option>

                                        )
                                    )}

                                </select>

                                <button
                                    onClick={() =>
                                        handleUnenroll(selectedCourse)
                                    }
                                    disabled={!selectedCourse}
                                >
                                    Unenroll
                                </button>
                            </>

                        )}

                    </section>
                )}


                {/* ASK EDUAI */}

                {user.role === "student" && (

                    <section
                        className="question-card"
                    >

                        <h2>
                            Ask EduAI
                        </h2>

                        <p>
                            Ask a question about
                            your selected course.
                        </p>


                        <form
                            onSubmit={handleAsk}
                        >

                            <textarea
                                value={question}
                                onChange={(event) =>
                                    setQuestion(
                                        event.target.value
                                    )
                                }
                                placeholder={
                                    "Ask your academic question..."
                                }
                                rows="5"
                            />


                            <button
                                type="submit"
                                disabled={loading}
                            >

                                {loading
                                    ? "Thinking..."
                                    : "Ask EduAI"}

                            </button>

                        </form>

                    </section>
                )}


                {/* ANSWER */}

                {answer && (

                    <section className="answer-card">

                        <h2>
                            EduAI Answer
                        </h2>

                        <div className="answer">
                            {answer}
                        </div>


                        {sources.length > 0 && (

                            <div
                                style={{
                                    marginTop: "30px",
                                    padding: "20px",
                                    border: "2px solid #ddd",
                                    borderRadius: "10px"
                                }}
                            >

                                <h3>
                                    Sources ({sources.length})
                                </h3>

                                {sources.map(
                                    (source, index) => (

                                        <div
                                            key={index}
                                            style={{
                                                marginTop: "15px",
                                                padding: "15px",
                                                background: "#f5f5f5",
                                                borderRadius: "8px"
                                            }}
                                        >

                                            <strong>
                                                {source.metadata?.source
                                                    ? source.metadata.source
                                                        .split(/[\\/]/)
                                                        .pop()
                                                    : "Course Material"
                                                }
                                            </strong>

                                            <p>
                                                {source.content}
                                            </p>

                                            {source.metadata?.page !== undefined && (

                                                <small>
                                                    Page {source.metadata.page + 1}
                                                </small>

                                            )}

                                        </div>

                                    )
                                )}

                            </div>

                        )}

                    </section>

                )}

                
                {/* QUESTION HISTORY */}

                {user.role === "student" && (

                    <section className="question-card">

                        <h2>
                            Recent Questions
                        </h2>

                        {history.length === 0 ? (

                            <p>
                                You have not asked any questions yet.
                            </p>

                        ) : (

                            <div className="history-list">

                                {history.map(
                                    (item) => (

                                        <div
                                            key={item.id}
                                            className="history-item"
                                        >

                                            <h3>
                                                {item.question}
                                            </h3>

                                            <p>
                                                {item.answer}
                                            </p>

                                            <small>
                                                Course ID: {item.course_id}
                                                {" | "}
                                                {new Date(
                                                    item.created_at
                                                ).toLocaleString()}
                                            </small>

                                        </div>

                                    )
                                )}

                            </div>

                        )}

                    </section>

                )}

            </main>

        </div>
    );
}


export default Dashboard;
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import {
    getCurrentUser,
    askQuestion
} from "../services/api";


function Dashboard() {

    const navigate = useNavigate();

    const [user, setUser] =
        useState(null);

    const [question, setQuestion] =
        useState("");

    const [answer, setAnswer] =
        useState("");

    const [loading, setLoading] =
        useState(false);

    const [error, setError] =
        useState("");


    useEffect(() => {

        async function loadUser() {

            try {

                const data =
                    await getCurrentUser();

                setUser(data);

            } catch {

                localStorage.removeItem(
                    "access_token"
                );

                navigate("/");

            }
        }

        loadUser();

    }, [navigate]);


    async function handleAsk(event) {

        event.preventDefault();

        if (!question.trim()) {
            return;
        }

        setLoading(true);
        setError("");
        setAnswer("");

        try {

            const data =
                await askQuestion(
                    question
                );

            setAnswer(
                data.answer
            );

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

            <header className="dashboard-header">

                <div>

                    <h1>EduAI</h1>

                    <p>
                        AI-Powered Academic Assistant
                    </p>

                </div>


                <div className="user-section">

                    <span>
                        Welcome, {user.username}
                    </span>

                    <button
                        onClick={logout}
                    >
                        Logout
                    </button>

                </div>

            </header>


            <main className="dashboard-content">

                <section className="question-card">

                    <h2>
                        Ask EduAI
                    </h2>

                    <p>
                        Ask a question about
                        your course material.
                    </p>


                    {error && (
                        <div className="error">
                            {error}
                        </div>
                    )}


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
                            placeholder="Ask your academic question..."
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


                {answer && (

                    <section className="answer-card">

                        <h2>
                            EduAI Answer
                        </h2>

                        <div className="answer">
                            {answer}
                        </div>

                    </section>

                )}

            </main>

        </div>
    );
}


export default Dashboard;
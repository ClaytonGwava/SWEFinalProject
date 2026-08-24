import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

import {
    getCourses,
    uploadCourseDocument
} from "../services/api";


function FacultyDashboard() {

    const [courses, setCourses] =
        useState([]);

    const [selectedCourse, setSelectedCourse] =
        useState(null);

    const [selectedFile, setSelectedFile] =
        useState(null);

    const [message, setMessage] =
        useState("");

    const [error, setError] =
        useState("");

    const [uploading, setUploading] =
        useState(false);


    useEffect(() => {

        loadCourses();

    }, []);


    async function loadCourses() {

        try {

            const data =
                await getCourses();

            setCourses(data);

        } catch (err) {

            setError(
                err.message ||
                "Failed to load courses"
            );
        }
    }


    function handleFileChange(event) {

        const file =
            event.target.files[0];

        setSelectedFile(file);

        setMessage("");
        setError("");
    }


    async function handleUpload() {

        if (!selectedCourse) {

            setError(
                "Please select a course."
            );

            return;
        }

        if (!selectedFile) {

            setError(
                "Please select a document."
            );

            return;
        }


        setUploading(true);
        setMessage("");
        setError("");


        try {

            const result =
                await uploadCourseDocument(
                    selectedCourse.id,
                    selectedFile
                );


            setMessage(
                `${result.filename} uploaded successfully. ` +
                `${result.chunks_created} chunks indexed.`
            );


            setSelectedFile(null);


            const fileInput =
                document.getElementById(
                    "document-file"
                );

            if (fileInput) {

                fileInput.value = "";

            }


        } catch (err) {

            setError(
                err.message ||
                "Document upload failed"
            );

        } finally {

            setUploading(false);

        }
    }


    return (

        <div className="dashboard">

            {/* HEADER */}

            <header
                className="dashboard-header"
            >

                <div>

                    <h1>
                        EduAI
                    </h1>

                    <p>
                        Faculty Dashboard
                    </p>

                </div>


                <div className="user-section">

                    <Link to="/dashboard">

                        <button>
                            Back to Dashboard
                        </button>

                    </Link>

                </div>

            </header>


            <main
                className="dashboard-content"
            >

                {/* INTRO */}

                <section
                    className="question-card"
                >

                    <h2>
                        Manage Course Materials
                    </h2>

                    <p>
                        Upload learning materials for
                        your courses. EduAI will process
                        the documents and use them as
                        sources for student questions.
                    </p>

                    <p>
                        Supported formats:
                        {" "}
                        <strong>
                            PDF, DOCX, PPTX
                        </strong>
                    </p>

                </section>


                {/* ERROR */}

                {error && (

                    <div className="error">
                        {error}
                    </div>

                )}


                {/* SUCCESS */}

                {message && (

                    <div className="success-message">

                        {message}

                    </div>

                )}


                {/* COURSES */}

                <section
                    className="question-card"
                >

                    <h2>
                        Your Courses
                    </h2>


                    {courses.length === 0 ? (

                        <p>
                            No courses available.
                        </p>

                    ) : (

                        <div>

                            {courses.map(
                                (course) => (

                                    <div
                                        key={course.id}
                                        className="course-item"
                                    >

                                        <div>

                                            <strong>
                                                {
                                                    course.course_code
                                                }
                                            </strong>

                                            <p>
                                                {
                                                    course.course_name
                                                }
                                            </p>

                                            <small>
                                                {
                                                    course.description
                                                }
                                            </small>

                                        </div>


                                        <button
                                            onClick={() =>
                                                setSelectedCourse(
                                                    course
                                                )
                                            }
                                        >
                                            Upload Material
                                        </button>

                                    </div>

                                )
                            )}

                        </div>

                    )}

                </section>


                {/* UPLOAD */}

                {selectedCourse && (

                    <section
                        className="question-card"
                    >

                        <h2>
                            Upload Course Material
                        </h2>


                        <p>

                            Selected Course:
                            {" "}

                            <strong>
                                {
                                    selectedCourse.course_code
                                }
                                {" - "}
                                {
                                    selectedCourse.course_name
                                }
                            </strong>

                        </p>


                        <input
                            id="document-file"
                            type="file"
                            accept=".pdf,.docx,.pptx"
                            onChange={
                                handleFileChange
                            }
                        />


                        {selectedFile && (

                            <p>

                                Selected file:
                                {" "}

                                <strong>
                                    {
                                        selectedFile.name
                                    }
                                </strong>

                            </p>

                        )}


                        <button
                            onClick={handleUpload}
                            disabled={uploading}
                        >

                            {uploading
                                ? "Uploading and indexing..."
                                : "Upload and Index"
                            }

                        </button>


                        <button
                            type="button"
                            onClick={() => {
                                setSelectedCourse(null);
                                setSelectedFile(null);
                                setMessage("");
                                setError("");

                                const fileInput =
                                    document.getElementById(
                                        "document-file"
                                    );

                                if (fileInput) {
                                    fileInput.value = "";
                                }
                            }}
                        >
                            Cancel
                        </button>

                    </section>

                )}

            </main>

        </div>

    );
}


export default FacultyDashboard;
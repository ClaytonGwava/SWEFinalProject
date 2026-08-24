import { Link, useNavigate } from "react-router-dom";


function Navbar() {

    const navigate = useNavigate();

    const token =
        localStorage.getItem("access_token");

    const role =
        localStorage.getItem("role");


    function handleLogout() {

        localStorage.removeItem(
            "access_token"
        );

        localStorage.removeItem(
            "role"
        );

        navigate("/");
    }


    // Don't show navbar when user isn't logged in
    if (!token) {
        return null;
    }


    return (

        <nav className="navbar">

            <div className="navbar-brand">

                <Link to="/dashboard">
                    EduAI
                </Link>

            </div>


            <div className="navbar-links">

                <Link to="/dashboard">
                    Dashboard
                </Link>


                {role === "faculty" && (

                    <Link to="/faculty">
                        Faculty Dashboard
                    </Link>

                )}


                <button
                    onClick={handleLogout}
                >
                    Logout
                </button>

            </div>

        </nav>
    );
}


export default Navbar;
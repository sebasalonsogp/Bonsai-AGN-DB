import { useState } from "react";
import QuerySearch from "../components/QuerySearch";

function Search() {
    const [validationText, setValidationText] = useState(""); // Input field state for password
    // Placeholder password - replace with secure backend authentication
    const placeholderPass = " "; 
    const placeholderValidate = () => { 
        // Basic client-side validation - REMOVE IN PRODUCTION 
        setAllowed(validationText === placeholderPass); 
    }
    const [allowed, setAllowed] = useState(false); // State to track if user is authenticated

    return (
        <div>
            {allowed ? 
                // Render search component if authenticated
                <div className="mx-[10%]">
                    <QuerySearch/>
                </div>
            :
                // Render password prompt if not authenticated
                <div className="flex flex-col items-center justify-center pt-10">
                    <div className="flex flex-col items-center gap-4 p-6 bg-white rounded-lg shadow-md border border-gray-200 w-full max-w-md">
                         <h2 className="text-lg font-semibold text-gray-700">Enter Password</h2>
                         <p className="text-sm text-gray-500 mb-4 text-center">Please enter the password to access the search functionality.</p>
                        <div className="flex flex-row gap-2 items-center">
                            <textarea
                                className="bg-gray-50 border border-gray-300 inline-block p-2 resize-none rounded-md focus:ring-blue-500 focus:border-blue-500"
                                placeholder="Password"
                                value={validationText}
                                onChange={(e) => setValidationText(e.target.value)}
                                rows={1}
                            />
                            <button
                                className="bg-blue-500 text-center h-10 flex items-center px-4 rounded-md cursor-pointer hover:bg-blue-600 text-white font-medium transition-colors"
                                onClick={placeholderValidate}
                            >
                                Validate
                            </button>
                        </div>
                    </div>
                </div>
            }
        </div>
    );
}

export default Search;
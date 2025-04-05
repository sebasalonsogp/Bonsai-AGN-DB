import { useState } from "react";
import QuerySearch from "../components/QuerySearch";

function Search() {
    const [validationText, setValidationText] = useState(""); // Used of keep trak of the string in the textarea
    const placeholderPass = " "; // Placeholder password and function for validation, should be done in backend for security
    const placeholderValidate = () => {console.log("validating..."); setAllowed(validationText === placeholderPass); }
    const [allowed, setAllowed] = useState(false);

    return (
        <div>
            {allowed ? 
            <div className="mx-[10%]">
                <div>
                    <QuerySearch/>
                </div>
            </div> 
            :
            <div className="absolute bg-gray-500/50 w-full h-screen pointer-events-none top-0">
                <div className="absolute top-1/4 left-1/2 -translate-x-1/2 -translate-y-1/2 pointer-events-auto flex flex-row gap-2 items-center drop-shadow-2xl">
                    <textarea
                        className="bg-white inline-block p-2 resize-none w-sm"
                        placeholder="Enter the password to access this page"
                        value={validationText}
                        onChange={(e) => setValidationText(e.target.value)}
                    />
                    <div className="bg-red-500 text-center h-12 flex items-center p-4 rounded cursor-pointer hover:bg-red-600 text-white" onClick={placeholderValidate}>
                        Validate
                    </div>
                </div>
            </div>}

        </div>
    );

}


export default Search;
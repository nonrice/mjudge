import { useParams } from 'react-router-dom';
import { useEffect, useState } from 'react';
import ReactMarkdown from 'react-markdown';
import "katex/dist/katex.min.css";
import remarkMath from "remark-math";
import rehypeKatex from "rehype-katex";
import { fetcher, postData } from '../utils/fetcher';
import useSWR from 'swr';

import AceEditor from 'react-ace';
import "ace-builds/src-noconflict/mode-python"
import "ace-builds/src-noconflict/mode-c_cpp"
import "ace-builds/src-noconflict/mode-java"
import "ace-builds/src-noconflict/theme-tomorrow"
import "ace-builds/src-noconflict/theme-tomorrow_night";
import "ace-builds/src-noconflict/ext-language_tools"
import "ace-builds/esm-resolver"; 



import { getToken, getUserFromToken } from '../utils/auth';


const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

export default function ContestProblemView() {
    const { contestId } = useParams();
    const { problemLetter } = useParams();
    const [language, setLanguage] = useState('python');
    const [isDarkMode, setIsDarkMode] = useState(false);
    const [message, setMessage] = useState("");

    useEffect(() => {
        const darkModeQuery = window.matchMedia('(prefers-color-scheme: dark)');
        setIsDarkMode(darkModeQuery.matches);

        const handleChange = (e) => setIsDarkMode(e.matches);
        darkModeQuery.addEventListener('change', handleChange);

        return () => darkModeQuery.removeEventListener('change', handleChange);
    }, []);


    const handleLanguageChange = (event) => {
        if (event.target.value === 'python3') {
            setLanguage('python');
        } else if (event.target.value === 'cpp') {
            setLanguage('c_cpp');
        } else if (event.target.value === 'java') {
            setLanguage('java');
        }
    };

    const { data: problem, error } = useSWR(
        [`${API_BASE_URL}/contest/${contestId}/problem/${problemLetter}`],
        fetcher
    )


    const storageKey = `code_${contestId}_${problemLetter}`;
    const [code, setCode] = useState("");
    useEffect(() => {
        const savedCode = localStorage.getItem(storageKey);
        if (savedCode !== null) {
            setCode(savedCode);
        }
    }, [storageKey]);


    const handleSubmit = (event) => {
        event.preventDefault();
        const submitButton = event.target.querySelector('input[type="submit"]');
        submitButton.disabled = true;
        const formData = new FormData(event.target);
        const solutionData = {
            code: code, 
            language: formData.get('language'),
            problem_letter: problemLetter,
            contest_id: contestId,
        };

        fetch(`${API_BASE_URL}/submit`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${ getToken() }`,
            },
            body: JSON.stringify(solutionData),
        })
        .then(res => {
            if (!res.ok) {
                throw new Error('Failed to submit solution');
            }
            return res.json();
        })
        .then(data => {
            window.location.href = `/contest/${contestId}/mysubmissions`;
            //alert('Solution submitted successfully! Submission ID: ' + data.submission_id);
            setMessage("Solution submitted successfully!");
            // Handle successful submission (e.g., redirect or update UI)
        })
        .catch(err => {
            // alert('Error submitting solution: ' + err.message);
            setMessage("Error submitting solution. Try again later.");
        });
        submitButton.disabled = false;
    };

    if (error) return <p>Error loading problem: {error}</p>;
    if (!problem) return <p>Loading problem...</p>;

    return (
        <div>
            <h1>{problemLetter}. {problem.title}</h1>
            <ReactMarkdown
                remarkPlugins={[remarkMath]}
                rehypePlugins={[rehypeKatex]}
            >{problem.statement}</ReactMarkdown>

            <hr></hr>
            <h2>Submit</h2>

            { getUserFromToken() ? (
                <form onSubmit={handleSubmit}>
                    <label htmlFor="language">Language:</label><br />
                    <select id="language" name="language" onChange={handleLanguageChange}>
                        <option value="python3">Python3</option>
                        <option value="cpp">C++</option>
                        <option value="java">Java</option>
                    </select><br />
                    <label htmlFor="code">Solution:</label><br />
                    <AceEditor
                        name="code"
                        mode={language}
                        theme={isDarkMode ? "tomorrow_night" : "tomorrow"}
                        fontSize={14}
                        width="100%"
                        height="300px"
                        editorProps={{ $blockScrolling: true }}
                        onChange={(newCode) => {
                            setCode(newCode);
                            localStorage.setItem(storageKey, newCode);
                        }}
                        value={code}
                    />
                    <p>{message || message}</p>
                    <input type="submit" value="Submit" />
                </form>
            ) : (
                <p>You need to be logged in to submit a solution.</p>
            )}
                
        </div>
    );
}
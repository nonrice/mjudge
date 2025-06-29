import { useParams } from 'react-router-dom';
import { useEffect, useState } from 'react';
import ReactMarkdown from 'react-markdown';
import "katex/dist/katex.min.css";
import remarkMath from "remark-math";
import rehypeKatex from "rehype-katex";
import AceEditor from 'react-ace';

import "ace-builds/src-noconflict/mode-python"
import "ace-builds/src-noconflict/mode-c_cpp"
import "ace-builds/src-noconflict/mode-java"
import "ace-builds/src-noconflict/theme-tomorrow"
import "ace-builds/src-noconflict/ext-language_tools"
import "ace-builds/webpack-resolver"



import { getToken, getUserFromToken } from '../utils/auth';

export default function ContestProblemView() {
    const { contestId } = useParams();
    const { problemLetter } = useParams();

    const [language, setLanguage] = useState('python');

    const handleLanguageChange = (event) => {
        if (event.target.value === 'python3') {
            setLanguage('python');
        } else if (event.target.value === 'cpp') {
            setLanguage('c_cpp');
        } else if (event.target.value === 'java') {
            setLanguage('java');
        }
    };

    const [problem, setProblem] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [code, setCode] = useState("");
    useEffect(() => {
        fetch(`http://127.0.0.1:5001/api/contest/${contestId}/problem/${problemLetter}`).then(res => {
            if (!res.ok) {
                throw new Error('Failed to fetch problem');
            }
            return res.json();
        }).then(data => {
            setProblem(data)
            setLoading(false);
        }).catch(err => {
            setError(err.message);
            setLoading(false);
        });
    }, [contestId, problemLetter]);

    if (loading) return <p>Loading problem...</p>;
    if (error) return <p>Error loading problem: {error}</p>;


    const handleSubmit = (event) => {
        event.preventDefault();
        const formData = new FormData(event.target);
        const solutionData = {
            code: code, 
            language: formData.get('language'),
            problem_letter: problemLetter,
            contest_id: contestId,
        };

        fetch(`http://127.0.0.1:5001/api/submit`, {
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
            alert('Solution submitted successfully! Submission ID: ' + data.submission_id);
            // Handle successful submission (e.g., redirect or update UI)
        })
        .catch(err => {
            alert('Error submitting solution: ' + err.message);
        });
    };


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
                    <label htmlFor="code">Solution:</label><br />
                    <label htmlFor="language">Language:</label><br />
                    <select id="language" name="language" onChange={handleLanguageChange}>
                        <option value="python3">Python3</option>
                        <option value="cpp">C++</option>
                        <option value="java">Java</option>
                    </select><br />
                    <AceEditor
                        name="code"
                        mode={language}
                        theme="tomorrow"
                        fontSize={14}
                        width="100%"
                        height="300px"
                        editorProps={{ $blockScrolling: true }}
                        onChange={(newCode) => setCode(newCode)}
                        value={code}
                    />
                    <input type="submit" value="Submit" />
                </form>
            ) : (
                <p>You need to be logged in to submit a solution.</p>
            )}
                
        </div>
    );
}
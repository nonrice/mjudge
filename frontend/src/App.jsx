import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import HomePage from './pages/HomePage';
import About from './pages/About';
import Contests from './pages/Contests';
import ContestLayout from './pages/ContestLayout';
import ContestProblems from './components/ContestProblems';
import ContestProblemView from './components/ContestProblemView';
import ContestStandings from './components/ContestStandings';
import ContestMySubmissions from './components/ContestMySubmissions';
import ContestSubmissionViewer from './components/ContestSubmissionViewer';
import Login from './pages/Login';
import Register from './pages/Register';
import SubmissionViewer from './pages/SubmissionViewer';

function App() {
    return (
        <div className="App">
        <BrowserRouter>
            <Routes>
                <Route path="/" element={<HomePage />} />
                <Route path="/about" element={<About />} />
                <Route path="/contests" element={<Contests />} />
                <Route path="/login" element={<Login />} />
                <Route path="/register" element={<Register />} />
                <Route path="/contest/:contestId" element={<ContestLayout />}>
                    <Route index element={<Navigate to="problems" replace />} />
                    <Route path="problems" element={<ContestProblems />} />
                    <Route path="problem/:problemLetter" element={<ContestProblemView />} />
                    <Route path="standings" element={<ContestStandings />} />
                    <Route path="mysubmissions" element={<ContestMySubmissions />} />
                    <Route path="submission/:submissionId" element = {<ContestSubmissionViewer showBackLink={true} />}/>
                </Route>
                <Route path="/submission/:submissionId" element = {<SubmissionViewer />}/>
            </Routes>
        </BrowserRouter>
        </div>
    );
}

export default App;

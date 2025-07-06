import Header from "../components/Header";
import Navbar from "../components/Navbar";

export default function About() {
    return (
        <div>
        <Header />
        <Navbar />
        <h1>About</h1>
        <h2>Introduction</h2>
        <p>Competitive programming is a mind sport where contestants write code to solve provided problemsets under given specifications. Competitions are held on "online judges". You might have heard of LeetCode&mdash;probably the most infamous example of one. As a sport, though, competitive programming becomes much more fun once you lose the "interview grind" mindset.</p>

        <p>In fact, many high schools that excel in STEM competitions have their own competition programming teams. How do these teams practice? That's a question I faced with my school team as well. We initially resorted to using popular online judges. But to make a long story short, growing restrictions on usage (spurred by anti-AI crawling measures) eventually made it too inconvenient for us to do so.</p>

        <p>Some school clubs I know developed their own online judges. However, to my knowledge, they are often very proprietary, or are not designed for frequent practice contests. My goal for McLean Judge (as it is called now, I may change its name later) is to solve both of these problems&mdash;to make a lightweight and easy-to-use platform which can be set up without trouble, endure frequent usage, and streamline problemsetting.</p>

        <h2>How to Use</h2>
        <p>First, register for an account. Then go to the contests tab. Click on problems to view their statements, and submit your code at the bottom of the problem page. It's advised to write code and test it on your own local editor, and just paste it into the website to submit. Upon submission you'll be directed to a list displaying all your submissions for the contest. There, you can observe the status and details of your submission.</p>

        <p>The contest leaderboards are arranged following the <a href="https://www.csc.kth.se/contest/nwerc/2006/results/scoring.html">ACM-ICPC scoring system</a>.</p>

        <h2>Judging Details</h2>
        <p>Three languages are supported at the moment:</p>
        <ul>
            <li>Python 3 (Python 3.11)</li>
            <li>C++ (C++17)</li>
            <li>Java (Java 17)</li>
        </ul>
        <p>Note for Java users: Title your class "Main" (case sensitive).</p>

        <p>Your program should only read and print from standard input and output, respectively. Do not try to destabilize the judging system!</p>

        <p>After your submission is graded, the status will update. A status of "accepted" means you solved the problem. All other statuses indicate an error.</p>
        <ul>
            <li>Wrong Answer: Your program printed the wrong answer for a testcase.</li>
            <li>Time Limit Exceeded: Your program took too long to run. Think of a more efficient solution.</li>
            <li>Memory Limit Exceeded: Your program used too much memory. Find a way to use less of it.</li>
            <li>Runtime Error: Your program crashed during execution. This could be due to an out-of-bounds access, division by zero, or other runtime errors.</li>
            <li>Compilation Error: Your program failed to compile.</li>
        </ul>
        </div>
    );
}
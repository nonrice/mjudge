# McLean Judge

McLean Judge (mjudge) is an online competitive programming judge. It is designed to be easily deployable and suitable for frequent practice contests.

## About
As of May 2025, many popular competitive programming sites put in place various restrictions to combat AI scraping. McLean Competitive Programming historically hosted practice contests using a 3rd-party proxy site, which, as a consequence, has become very inconvenient to use. McLean Judge was made to 1) remove McLean Competitive Programming's reliance on outside resources and 2) to improve freedom in problem setting for practice contests.

## Deployment
You can deploy very quickly on pretty much any VPS.

Clone the repo and make a `.env` in the top level. Here's an example.
```
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=judgedb
POSTGRES_HOST=db
POSTGRES_PORT=5432
PGADMIN_DEFAULT_EMAIL=admin@example.com
PGADMIN_DEFAULT_PASSWORD=admin
VITE_API_BASE_URL=http://localhost:5001/api
POLL_INTERVAL=10
MAX_WORKERS=2
CORS_ORIGINS=http://127.0.0.1:3000,http://167.71.87.138
JWT_SECRET_KEY=some_secret_key
```

Then start the containers with `docker compose up --build`.

## Management
Direct database access can suffice to operate the judge, but a more user-friendly administration interface is being worked on. 

For uploading problems there's a special endpoint `/api/admin/upload_prob`. Once authenticated with an administrator account, `POST` a `.zip` file there to automatically populate the DB tables.

Archive format:
```
some_problem
├── checker.language
├── info.json
├── solution.language
├── statement.md
└── tests
    ├── 1.txt
    ├── 2.txt
    └── ...
```

The checker should receive three runtime arguments, which are filepaths, in the order:
1. File containing user code output
2. File containing solution code output
3. File containing the testcase

For the checker to indicate a correct answer, exit normally with code `0`. Otherwise, exit with a nonzero code. Standard output and standard error will be copied into the feedback.

`info.json` format:
```json
{
    "title": "Exciting Problem",
    "time_limit": 2000,
    "memory_limit": 256,
    "solution_lang": "cpp",
    "checker_lang": "python3",
    "samples": [1, 2]
}
```
The `"samples"` entry determines the testcase numbers, which, upon failing, will not hide feedback from users during a contest.

## Development
There are development Docker configurations. Use them by including `-f docker-compose.dev.yml` in calls to compose.

McLean Judge uses a React frontend with Vite tooling, Flask backend, and Postgres database.

# McLean Judge

McLean Judge (mjudge) is an online competitive programming judge. It is designed to be easily deployable and suitable for frequent practice contests.

## About
[Here's the source for the default about page.](frontend/src/pages/About.jsx)

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

You might need to quit and run it again. There seem to be some dependency issues that only happen on the first run, since that's when the databases is initialized.

## Management
I haven't implemented much admin stuff yet. You can directly modify the tables on pgAdmin.

For uploading problems there's a special endpoint `/api/admin/upload_prob`. `POST` a `.zip` file there to automatically populate the DB tables. To be considered an admin, your token must be of an account named `eric`.

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

The checker should receive three runtime arguments, which are filepaths:
- File containing user code output
- File containing solution code output
- File containing the testcase

For the checker indicate a correct answer, exit normally with code `0`. Otherwise, exit with a nonzero code. Standard output and standard error will be copied into the feedback.

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

The grading infrastructure is written in Python. A grading container polls the submissions table for waiting submissions and spawns individual, ephemeral worker containers to run them. Sandboxing is done through containerizing with Docker and privilege removal.


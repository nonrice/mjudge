import time
import docker
from sqlalchemy import create_engine, Table, MetaData, select, update
from sqlalchemy.exc import SQLAlchemyError
import os

# CONFIG
# DATABASE_URL = "postgresql://postgres:postgres@db:5432/judgedb"
DATABASE_URL = os.getenv("DATABASE_URL")
POLL_INTERVAL = int(os.getenv("POLL_INTERVAL", 10))  # seconds
MAX_WORKERS = int(os.getenv("MAX_WORKERS", 1))  # Maximum number of concurrent worker containers
KEEP_CONTAINERS = os.getenv("KEEP_CONTAINERS", "false").lower() == "true"  # Whether to keep containers after execution

# Initialize Docker and DB clients
docker_client = docker.from_env()
engine = create_engine(DATABASE_URL)
metadata = MetaData()

def main():
    submissions = Table("submissions", metadata, autoload_with=engine)

    print("Grading poller started.")
    while True:
        try:
            with engine.connect() as conn:
                # Find one ungraded submission
                stmt = select(submissions).where(submissions.c.status == "Waiting").limit(1)
                result = conn.execute(stmt).fetchone()

                if result:
                    print(f"Found submission ID {result.id}")

                    # Mark as running
                    # upd = (
                    #     update(submissions)
                    #     .where(submissions.c.id == result.id)
                    #     .values(status="Running")
                    # )
                    # conn.execute(upd)
                    # conn.commit()

                    # Spawn worker container
                    spawn_worker(submission_id=result.id)
                else:
                    print("No submissions to grade.")
        except SQLAlchemyError as e:
            print("DB error:", e)

        time.sleep(POLL_INTERVAL)

def spawn_worker(submission_id):
    running_workers = [
        c for c in docker_client.containers.list(filters={"ancestor": "mclean-judge-worker"})
    ]
    print(f"Currently running workers: {len(running_workers)}")
    if len(running_workers) >= MAX_WORKERS:
        print("Maximum number of workers reached, ignoring launch.")
        return

    print(f"Spawning worker for submission {submission_id}")
    try:
        docker_client.containers.run(
            "mclean-judge-worker",  # Your worker image
            command=[str(submission_id)],
            detach=True,
            network="mclean-judge_default",
            auto_remove=not KEEP_CONTAINERS,  # Clean up container after exit if desired
            cap_drop=["ALL"],                  # Drop all Linux capabilities
            pids_limit=32,                   # Limit number of threads/processes
            security_opt=["no-new-privileges"],  # Prevent privilege escalation
            mem_limit="4069m",                # Memory limit
            volumes={},                      # No volume mounts for strict isolation
            read_only=True,
            tmpfs={"/tmp": "exec"},
            environment={
                "DATABASE_URL": DATABASE_URL,
            }
        )
    except docker.errors.DockerException as e:
        print("Docker error:", e)

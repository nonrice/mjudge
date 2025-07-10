import time
import docker
from sqlalchemy import create_engine, Table, MetaData, select, update
from sqlalchemy.exc import SQLAlchemyError
import os

# CONFIG
DATABASE_URL = os.getenv("DATABASE_URL")
POLL_INTERVAL = int(os.getenv("POLL_INTERVAL", 10))  # seconds
MAX_WORKERS = int(
    os.getenv("MAX_WORKERS", 1)
)
KEEP_CONTAINERS = (
    os.getenv("KEEP_CONTAINERS", "false").lower() == "true"
)

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
                stmt = (
                    select(submissions)
                    .where(submissions.c.status == "Waiting")
                    .limit(1)
                )
                result = conn.execute(stmt).fetchone()

                if result:
                    print(f"Found submission ID {result.id}")

                    spawn_worker(submission_id=result.id)
        except SQLAlchemyError as e:
            print("DB error:", e)

        time.sleep(POLL_INTERVAL)


def spawn_worker(submission_id):
    running_workers = [
        c
        for c in docker_client.containers.list(
            filters={"ancestor": "mclean-judge-worker"}
        )
    ]
    print(f"Currently running workers: {len(running_workers)}")
    if len(running_workers) >= MAX_WORKERS:
        print("Maximum number of workers reached, ignoring launch.")
        return

    print(f"Spawning worker for submission {submission_id}")
    try:
        docker_client.containers.run(
            "mclean-judge-worker",
            command=[str(submission_id)],
            detach=True,
            network="mclean-judge_default",
            auto_remove=not KEEP_CONTAINERS, 
            # cap_drop=["ALL"],                  # Actually we need this for dropping caps
            pids_limit=32,
            # security_opt=["no-new-privileges"],  # Same here
            mem_limit="4069m",  # Memory limit
            volumes={},
            read_only=True, # It's still read write exec for root but not nobody
            tmpfs={"/tmp": "rw,nosuid,nodev,exec"},
            environment={
                "DATABASE_URL": DATABASE_URL,
            },
            user="0:0",
        )
    except docker.errors.DockerException as e:
        print("Docker error:", e)

import time
import docker
from sqlalchemy import create_engine, Table, MetaData, select, update
from sqlalchemy.exc import SQLAlchemyError

# CONFIG
DATABASE_URL = "postgresql://postgres:postgres@db:5432/judgedb"
POLL_INTERVAL = 10  # seconds

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
    print(f"Spawning worker for submission {submission_id}")
    try:
        docker_client.containers.run(
            "mclean-judge-worker",  # Change to the actual image name you use for your worker
            command=[str(submission_id)],
            detach=True,
            network="mclean-judge_default",  # Match the docker-compose network if needed
        )
    except docker.errors.DockerException as e:
        print("Docker error:", e)


import os
import subprocess
import time
import psycopg2


def wait_for_db(host, db, user, password, port=5432, retries=24, delay=5):
    for attempt in range(1, retries + 1):
        try:
            conn = psycopg2.connect(
                host=host,
                database=db,
                user=user,
                password=password,
                port=port,
            )
            conn.close()
            print("Postgres is ready")
            return
        except Exception as exc:
            print(f"Waiting for Postgres... attempt {attempt}/{retries}: {exc}")
            time.sleep(delay)

    raise RuntimeError("Postgres not ready")


def run_script(script_name):
    subprocess.run(["python", script_name], check=True)


if __name__ == "__main__":
    db_config = {
        "host": os.getenv("DB_HOST", "db"),
        "db": os.getenv("DB_NAME", "weatherdb"),
        "user": os.getenv("DB_USER", "postgres"),
        "password": os.getenv("DB_PASSWORD", "postgres"),
    }

    wait_for_db(**db_config)
    run_script("extract.py")
    run_script("transform.py")
    run_script("load.py")
    print("ETL pipeline completed successfully")

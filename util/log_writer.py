import os
import random
import time
from datetime import datetime, timezone

LOG_FILE = os.environ.get("LOG_FILE", "/var/log/access.log")

seed = int(os.environ.get("RAND_SEED", 42))
random.seed(seed)

USERS = ["james", "jill", "frank", "mary"]
ENDPOINTS = [
    "/report",
    "/settings",
    "/profile",
    "/pages/create",
    "/pages/update",
    "/pages/delete",
    "/pages/edit",
    "/api/user",
    "/api/pages",
]
RESPONSE_CODES = [200, 201, 301, 404, 500]
TIMESTAMP_FORMAT = "%d/%b/%Y:%H:%M:%S %z"
MAX_LINES = 10_000


def reset_log(logfile):
    open(logfile, "w+").close()


def generate_entry():
    ip = "127.0.0.1"
    user = random.choice(USERS)
    endpoint = random.choice(ENDPOINTS)
    status = random.choice(RESPONSE_CODES)
    time = datetime.now(tz=timezone.utc).strftime(TIMESTAMP_FORMAT)
    size = random.randint(100, 500)
    return f'{ip} - {user} [{time}] "GET {endpoint} HTTP/1.0" {status} {size}'


def write_entry_to_log(entry, logfile):
    with open(logfile, "a") as f:
        print(entry)
        print(entry, file=f, end="\n")


def random_sleep():
    request_time_in_seconds = round(random.uniform(0.1, 1.5), 2)
    time.sleep(request_time_in_seconds)


if __name__ == "__main__":
    try:
        reset_log(LOG_FILE)

        for _ in range(MAX_LINES):
            random_sleep()
            entry = generate_entry()
            write_entry_to_log(entry, LOG_FILE)

    except PermissionError as err:
        print(f"Root permissions required to write to log file: {err}")
    except KeyboardInterrupt:
        print("\nta for now!")

import base64
import getpass
import hashlib
import json
import os
import secrets
from pathlib import Path


PASSWORD_HASH_ITERATIONS = 310_000
TEACHERS_FILE = Path(os.environ.get(
    "TEACHERS_FILE", Path.home() / ".config" / "mergington" / "teachers.json"
))


def main():
    username = input("Teacher username: ").strip()
    if not username:
        raise SystemExit("Username cannot be empty")

    password = getpass.getpass("Teacher password: ")
    if not password:
        raise SystemExit("Password cannot be empty")
    if password != getpass.getpass("Confirm password: "):
        raise SystemExit("Passwords do not match")

    try:
        teacher_data = json.loads(TEACHERS_FILE.read_text(encoding="utf-8"))
    except FileNotFoundError:
        teacher_data = {"teachers": []}
    except (OSError, ValueError) as error:
        raise SystemExit(f"Could not read {TEACHERS_FILE}: {error}") from error

    salt = secrets.token_bytes(16)
    password_hash = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt, PASSWORD_HASH_ITERATIONS
    )
    record = {
        "username": username,
        "salt": base64.urlsafe_b64encode(salt).decode("ascii"),
        "password_hash": base64.urlsafe_b64encode(password_hash).decode("ascii"),
        "iterations": PASSWORD_HASH_ITERATIONS,
    }
    teachers = teacher_data.setdefault("teachers", [])
    teachers[:] = [teacher for teacher in teachers if teacher.get("username") != username]
    teachers.append(record)

    TEACHERS_FILE.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    TEACHERS_FILE.write_text(json.dumps(teacher_data, indent=2) + "\n", encoding="utf-8")
    TEACHERS_FILE.chmod(0o600)
    print(f"Teacher credentials saved to {TEACHERS_FILE}")


if __name__ == "__main__":
    main()
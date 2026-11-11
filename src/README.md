# Mergington High School Activities API

A super simple FastAPI application that allows students to view and sign up for extracurricular activities.

## Features

- View all available extracurricular activities
- Teachers can register and unregister students after logging in
- Visitors can view activity rosters without logging in

## Getting Started

1. Install the dependencies:

   ```
   pip install fastapi uvicorn
   ```

2. Run the application:

   ```
   export SESSION_SECRET="$(python -c 'import secrets; print(secrets.token_urlsafe(32))')"
   python -m uvicorn src.app:app --reload
   ```

Before logging in, create a teacher account in another terminal:

```sh
python src/create_teacher.py
```

The command prompts for a username and password, then stores a salted password hash in `~/.config/mergington/teachers.json`. The account file is not stored in the repository. Set `TEACHERS_FILE` to use a different path. Set `COOKIE_SECURE=true` when serving the app over HTTPS.

3. Open your browser and go to:
   - API documentation: http://localhost:8000/docs
   - Alternative documentation: http://localhost:8000/redoc

## API Endpoints

| Method | Endpoint                                                          | Description                                                         |
| ------ | ----------------------------------------------------------------- | ------------------------------------------------------------------- |
| GET    | `/activities`                                                     | Get all activities with their details and current participant count |
| POST   | `/auth/login`                                                      | Log in as a teacher                                                 |
| GET    | `/auth/session`                                                    | Check whether a teacher is logged in                                |
| POST   | `/auth/logout`                                                     | Log out                                                             |
| POST   | `/activities/{activity_name}/signup?email=student@mergington.edu` | Register a student (teacher login required)                        |
| DELETE | `/activities/{activity_name}/unregister?email=student@mergington.edu` | Unregister a student (teacher login required)                    |

## Data Model

The application uses a simple data model with meaningful identifiers:

1. **Activities** - Uses activity name as identifier:

   - Description
   - Schedule
   - Maximum number of participants allowed
   - List of student emails who are signed up

2. **Students** - Uses email as identifier:
   - Name
   - Grade level

All data is stored in memory, which means data will be reset when the server restarts.

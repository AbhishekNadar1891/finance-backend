# Finance Backend

A FastAPI backend for personal finance tracking with JWT authentication, PostgreSQL, role-based access control, filtering, pagination, and dashboard summary APIs.

## Requirements

- Python 3.10+
- PostgreSQL

## Setup

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root using `.env.example`.
4. Set valid PostgreSQL credentials in `.env`.
5. Make sure PostgreSQL is running and the `finance_db` database exists.

Example `.env`:

```env
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/finance_db
SECRET_KEY=your_secret_key
```

## Run the Application

```bash
uvicorn app.main:app --reload
```

The application creates tables on startup using SQLAlchemy metadata.

## Fix PostgreSQL Password Issue

If you get:

`password authentication failed for user "postgres"`

Run:

```bash
psql -U postgres
```

Then:

```sql
ALTER USER postgres WITH PASSWORD '1234';
```

Then update `.env`:

```env
DATABASE_URL=postgresql://postgres:1234@localhost:5432/finance_db
```

## API Overview

### Authentication

- `POST /auth/login`

Use OAuth2 form fields:

- `username`: user email
- `password`: user password

### Users

- `POST /users/` to register a new user
- `GET /users/me` to fetch the current authenticated user

### Records

- `POST /records/` to create a financial record
- `GET /records/` to list records for the current user
- `GET /records/summary` to fetch dashboard totals for the current user
- `DELETE /records/{record_id}` to delete a record

## Notes

- `viewer` can create and list records.
- `admin` can create, list, view summary, and delete records.
- Inactive users cannot access protected routes.

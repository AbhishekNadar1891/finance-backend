import subprocess

print("Attempting to reset PostgreSQL password...")

print("\nSTEP 1: Open psql manually:")
print("Run this in terminal:")
print("psql -U postgres")

print("\nSTEP 2: Inside psql, run:")
print("ALTER USER postgres WITH PASSWORD '1234';")

print("\nSTEP 3: Update your .env file:")
print("DATABASE_URL=postgresql://postgres:1234@localhost:5432/finance_db")

print("\nSTEP 4: Restart server:")
print("uvicorn app.main:app --reload")

print("\nDone.")

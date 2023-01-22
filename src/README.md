# Menu App

## Getting started:
* Create a virtual environment and install all dependencies
```bash
python -m venv .venv
pip install -r requirements.txt
```
* Copy the file `example.env` as `.env` and fill in the environment variables
```bash
DB_USER="<login for database connection>"
DB_PASS="<password for database connection>"
DB_HOST="<database server host>"
DB_NAME="<database name>"
```
* Run initial migration to database
```bash
alembic upgrade head
```
* Run server application
```bash
uvicorn src.main:app
```

# Deployment Instructions for Render

This document provides instructions for deploying the QR code generation app to Render.

## Database Initialization

The app includes an automatic database initialization script that checks for the `qrs` table and creates it if it doesn't exist.

### Files

- **[init_db.py](init_db.py)**: Python script that checks if the `qrs` table exists in the database and creates it if missing
- **[build.sh](build.sh)**: Build script for Render that installs dependencies and initializes the database

## Render Configuration

### 1. Build Command

Set the build command in your Render service settings:

```bash
./build.sh
```

### 2. Start Command

The start command is already configured in the [Procfile](Procfile):

```bash
uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-5000}
```

### 3. Environment Variables

Make sure to set the `DATABASE_URL` environment variable in Render:

- **For SQLite** (development/small apps):
  ```
  DATABASE_URL=sqlite+aiosqlite:///./local.db
  ```

- **For PostgreSQL** (recommended for production):
  ```
  DATABASE_URL=postgresql+asyncpg://user:password@host:port/database
  ```

## What Happens During Deployment

1. Render runs `./build.sh`
2. The build script installs all Python dependencies from `requirements.txt`
3. The build script runs `init_db.py` which:
   - Connects to the database using the `DATABASE_URL` environment variable
   - Checks if the `qrs` table exists
   - Creates the table if it doesn't exist
   - Verifies the table structure
4. Render starts the application using the command in the Procfile

## Testing Locally

You can test the initialization script locally:

```bash
# With your virtual environment activated
python init_db.py

# Or with a specific database URL
DATABASE_URL="sqlite+aiosqlite:///./test.db" python init_db.py
```

## Database Schema

The `qrs` table has the following structure:

| Column        | Type     | Constraints           |
|---------------|----------|-----------------------|
| id            | Integer  | Primary Key           |
| short_code    | String   | Unique, Indexed       |
| url           | String   |                       |
| title         | String   | Nullable              |
| total_clicks  | Integer  | Default: 0            |
| unique_clicks | Integer  | Default: 0            |
| created_at    | DateTime | Default: now()        |

## Troubleshooting

If deployment fails:

1. Check Render logs for error messages
2. Verify that the `DATABASE_URL` environment variable is set correctly
3. For PostgreSQL, ensure the database exists and credentials are correct
4. Test the `init_db.py` script locally with your database settings

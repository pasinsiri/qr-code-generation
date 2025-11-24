# QR Code Generator & URL Shortener

A modern web application that generates QR codes for URLs with built-in link shortening and analytics tracking. Built with FastAPI and deployed on Render.

## Features

- **QR Code Generation**: Create QR codes for any URL instantly
- **URL Shortening**: Generate short, shareable links for your QR codes
- **Click Analytics**: Track total clicks and unique visitors for each QR code
- **Custom Titles**: Add descriptive titles to your QR codes
- **Statistics Dashboard**: View detailed analytics for each QR code
- **PNG Export**: Download QR codes as high-quality PNG images

## Live Demo

The application is deployed and running on Render

## Tech Stack

- **Backend**: FastAPI (Python)
- **Database**: SQLite (with support for PostgreSQL)
- **QR Generation**: Segno
- **Frontend**: Jinja2 Templates, HTML/CSS
- **Deployment**: Render

## Project Structure

```
qr-code-generation/
├── app/
│   ├── __init__.py
│   ├── main.py           # FastAPI application and routes
│   ├── database.py       # Database configuration
│   ├── models.py         # SQLAlchemy models
│   ├── crud.py           # Database operations
│   └── templates/        # HTML templates
│       ├── index.html    # Home page
│       ├── created.html  # QR code creation result
│       └── stats.html    # Analytics dashboard
├── static/
│   └── qr/              # Generated QR code images
├── init_db.py           # Database initialization script
├── build.sh             # Render build script
├── requirements.txt     # Python dependencies
├── Procfile            # Render start command
└── DEPLOYMENT.md       # Deployment documentation
```

## API Endpoints

### Web Interface

- `GET /` - Home page with QR code creation form
- `POST /create` - Create a new QR code
- `GET /{short_code}` - Redirect to the original URL (tracks clicks)
- `GET /stats/{short_code}` - View analytics for a QR code

## Database Schema

The application uses a single `qrs` table:

| Column        | Type     | Description                    |
|---------------|----------|--------------------------------|
| id            | Integer  | Primary key                    |
| short_code    | String   | Unique short code for the URL  |
| url           | String   | Original URL                   |
| title         | String   | User-defined title             |
| total_clicks  | Integer  | Total number of clicks         |
| unique_clicks | Integer  | Number of unique visitors      |
| created_at    | DateTime | Creation timestamp             |

## Local Development

### Prerequisites

- Python 3.11+
- pip

### Setup

1. Clone the repository:
   ```bash
   git clone <your-repo-url>
   cd qr-code-generation
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Initialize the database:
   ```bash
   python init_db.py
   ```

5. Run the application:
   ```bash
   uvicorn app.main:app --reload
   ```

6. Open your browser to `http://localhost:8000`

## Environment Variables

- `DATABASE_URL` - Database connection string (default: `sqlite+aiosqlite:///./local.db`)
- `PORT` - Server port (default: 5000 for Render, 8000 for local development)

## Deployment on Render

This application is deployed on Render with automatic database initialization.

### Deployment Configuration

**Build Command:**
```bash
./build.sh
```

**Start Command:**
```bash
uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-5000}
```

For detailed deployment instructions, see [DEPLOYMENT.md](DEPLOYMENT.md).

## How It Works

1. **Create a QR Code**: Enter a URL and optional title on the home page
2. **Get Your Short Link**: Receive a shortened URL and QR code image
3. **Share**: Share the short link or QR code with others
4. **Track Analytics**: View click statistics for any QR code via the stats page
5. **Automatic Tracking**: Each scan/click is automatically tracked with unique visitor detection

## Dependencies

Key dependencies include:

- `fastapi` - Modern web framework
- `uvicorn` - ASGI server
- `sqlalchemy` - SQL toolkit and ORM
- `databases` - Async database support
- `aiosqlite` - Async SQLite driver
- `segno` - QR code generation
- `shortuuid` - Short unique ID generation
- `jinja2` - Template engine
- `python-multipart` - Form data parsing

See [requirements.txt](requirements.txt) for the complete list.

## Features in Detail

### QR Code Generation

QR codes are generated using the Segno library at high quality (scale=10) and saved as PNG files in the `static/qr/` directory.

### Click Tracking

The application tracks:
- **Total Clicks**: Every time someone accesses the short link
- **Unique Clicks**: Based on IP address to identify unique visitors

### URL Shortening

Short codes are generated using `shortuuid`, creating 8-character unique identifiers for each URL.

## License

MIT License

## Author

Built and deployed by pasinsiri
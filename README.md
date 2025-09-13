# Judge Service

A Django-based judging service application.

## Deploying to Vercel

This project is configured for deployment on Vercel. Follow these steps to deploy:

### Prerequisites

1. A [Vercel](https://vercel.com) account
2. [Vercel CLI](https://vercel.com/docs/cli) installed (optional, for local testing)

### Deployment Steps

1. **Clone the repository**
   ```
   git clone <repository-url>
   cd JudgeService
   ```

2. **Login to Vercel**
   ```
   vercel login
   ```

3. **Deploy to Vercel**
   ```
   vercel
   ```

   Or deploy directly from the Vercel dashboard:
   - Connect your GitHub/GitLab/Bitbucket account
   - Import this repository
   - Vercel will automatically detect the configuration and deploy

### Configuration Files

The following files are used for Vercel deployment:

- `vercel.json`: Main configuration file for Vercel
- `build_files.sh`: Script to build the project and collect static files
- `requirements.txt`: Python dependencies
- `runtime.txt`: Python version specification

### Environment Variables

For production deployment, set these environment variables in the Vercel dashboard:

- `SECRET_KEY`: A secure Django secret key
- `DEBUG`: Set to 'False' for production
- `DATABASE_URL`: Connection string for your database (see below)

### Database Configuration

This project is now configured to use a PostgreSQL database in production via the DATABASE_URL environment variable, with a fallback to SQLite for local development.

For production on Vercel, you should use:

- Vercel Postgres: Set `DATABASE_URL` to the connection string provided by Vercel
- Other database services: Set `DATABASE_URL` to the appropriate connection string format:
  - PostgreSQL: `postgres://user:password@host:port/database`
  - MySQL: `mysql://user:password@host:port/database`
  - SQLite: `sqlite:///path/to/db.sqlite3` (not recommended for production)

The application will automatically use the database specified in the DATABASE_URL environment variable.

### Static Files

Static files are handled by WhiteNoise and configured to be served efficiently in production.

## Local Development

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Run migrations:
   ```
   python manage.py migrate
   ```

3. Start the development server:
   ```
   python manage.py runserver
   ```

## License

[Specify your license here]

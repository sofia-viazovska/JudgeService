# Judge Service

A Django-based judging service application for evaluating team projects.

## Table of Contents

1. [Project Overview](#project-overview)
2. [Judge This Team Module](#judge-this-team-module)
   - [User Roles](#user-roles)
   - [Service Vectors](#service-vectors)
   - [Criteria](#criteria)
   - [How to Use](#how-to-use)
   - [Technical Details](#technical-details)
   - [Troubleshooting](#troubleshooting)
3. [Password Instructions](#password-instructions)
   - [New Password Format](#new-password-format)
   - [For Judges](#for-judges)
   - [For Administrators](#for-administrators)
4. [Deployment](#deployment)
   - [Deploying to Vercel](#deploying-to-vercel)
   - [Configuration Files](#configuration-files)
   - [Environment Variables](#environment-variables)
   - [Database Configuration](#database-configuration)
   - [Static Files](#static-files)
5. [Local Development](#local-development)
6. [License](#license)

## Project Overview

Judge Service is a Django-based application designed for evaluating team projects. It provides a structured system for judges to score teams based on predefined criteria, with support for different user roles and dynamic criteria loading.

## Judge This Team Module

The Judge This Team module has been updated to support different user roles (Admin and Jury) and implement a service vector selection system with dynamic criteria loading based on the selected vector.

### User Roles

#### Admin Role
- Can see all main criteria
- Can select the project Service (technology vector) for each team via a dropdown
- Can save the selected vector for each team

#### Jury Role
- Can see all main criteria (same for all teams)
- Can see only the additional (bonus) criteria that match the team's selected vector (the one set by the Admin)
- Cannot change the selected vector; instead, the selected vector name is displayed as read-only text

### Service Vectors

There are three service vectors available:
- A – Mobile App
- B – Web App
- C – Telegram Bot

Each vector has its own set of additional (bonus) criteria that are displayed dynamically based on the selected vector.

### Criteria

#### Main Criteria (same for all teams)

##### Main functionality:
- Google OAuth works reliably – 5 points
- Profile is saved and restored – 5 points
- CV builder with field validation – 5 points
- CV preview with at least two templates – 4 points
- Export CV to clean PDF – 3.5 points
- Interview module (5–8 questions, timer, summary report) – 5 points
- Dashboard and "delete data" function – 2.5 points

##### UI/UX and stability:
- Clean interface, contrast, readability – 5 points
- Adaptive or native look for target platform – 5 points

##### Engineering quality:
- Code structure, modularity, conciseness – 4 points
- Data model, validation, error handling – 3 points
- Data security – 5 points
- README and artifacts – 3 points

##### Project explanation:
- Understanding and ability to explain key parts – 10 points

#### Additional (Bonus) Criteria

##### Vector A – Mobile App:
- Export CV to formats other than PDF – 3 points
- Multilingual UI – 3 points
- CV change history with timestamps – 3 points
- CI/CD build artifact – 4.5 points
- Static analysis and strict quality rules – 1.5 points

##### Vector B – Web App:
- Use TypeScript instead of JavaScript – 1.5 points
- Desktop build with Tauri/Electron – 4.5 points
- DOCX export (client or server side) – 3 points
- Multilingual UI – 3 points
- CV change history with rollback – 3 points

##### Vector C – Telegram Bot:
- Export CV to PDF directly in chat – 3 points
- Multilingual /lang (uk/en) – 3 points
- CV change history with /history log – 3 points
- Telegram WebApp for CV/dashboard preview – 4.5 points
- DOCX export and delivery to chat – 1.5 points

### How to Use

#### For Admins:
1. Log in with an admin account
2. Navigate to the team list page
3. Select a team to judge
4. On the team's judging page, you'll see a dropdown to select the service vector
5. Select the appropriate vector and click "Save Service"
6. The page will reload with the appropriate bonus criteria for the selected vector
7. Check the criteria that the team has fulfilled
8. The total score will be calculated automatically
9. Click "Submit Scores" to save your evaluation

#### For Jury:
1. Log in with a jury account
2. Navigate to the team list page
3. Select a team to judge
4. On the team's judging page, you'll see the service vector selected by the admin (if any)
5. You'll see the main criteria and the bonus criteria for the selected vector
6. Check the criteria that the team has fulfilled
7. The total score will be calculated automatically
8. Click "Submit Scores" to save your evaluation

### Technical Details

#### Database Schema
- Team model: Added a service field to store the selected vector
- Criteria model: Added type, service, and points fields
- Score model: Changed from numeric scoring to checkbox-based scoring

#### Scoring System
- Each criterion has a fixed point value
- When a criterion is checked, its points are added to the total score
- The total score is calculated in real-time using JavaScript
- The system shows separate totals for main criteria and bonus criteria, as well as a grand total

#### Installation
1. Apply migrations: `python manage.py migrate`
2. Populate criteria: `python manage.py populate_criteria`

### Troubleshooting

If you encounter any issues:
1. Make sure you've applied all migrations
2. Make sure you've populated the criteria using the management command
3. Check that you're logged in with the appropriate role (Admin or Jury)
4. If criteria are not displaying correctly, check that the team has a service vector selected (for bonus criteria)

## Password Instructions

### New Password Format

All user passwords now follow a consistent format:

```
username_password
```

#### Examples

- For user with username `tkachenko_i`, the password is `tkachenko_i_password`
- For user with username `yosypenko_o`, the password is `yosypenko_o_password`
- For user with username `chernikov_s`, the password is `chernikov_s_password`

### For Judges

If you're having trouble logging in, please use the format described above. If you still can't log in, please contact the administrator.

### For Administrators

If users are having trouble logging in, you can run the following command to update all passwords to the new format:

```bash
python manage.py update_passwords
```

This will update all non-superuser users' passwords to follow the consistent format.

## Deployment

### Deploying to Vercel

This project is configured for deployment on Vercel. Follow these steps to deploy:

#### Prerequisites

1. A [Vercel](https://vercel.com) account
2. [Vercel CLI](https://vercel.com/docs/cli) installed (optional, for local testing)

#### Deployment Steps

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

3. Populate criteria:
   ```
   python manage.py populate_criteria
   ```

4. Start the development server:
   ```
   python manage.py runserver
   ```

## License

[Specify your license here]

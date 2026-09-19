# Career Readiness Navigator

Hackathon MVP built with Django that helps students assess their skills,
discover matching careers, and follow a personalized roadmap to readiness.

## Core Flow

Student Register/Login → Skill Assessment → Select Career → Skill Gap Analysis →
Career Readiness Score → Personalized Roadmap → Progress Tracking

## Stack

- Python + Django
- Django Templates
- Custom modern CSS (no CDN, works offline)
- Vanilla JavaScript
- SQLite for development, PostgreSQL-ready via `DATABASE_URL`

## Project Structure

```
career_navigator/
├── config/          # Project settings, root URLs
├── accounts/        # Custom User, registration, login/logout, profile
├── skills/          # Skill catalog, self-assessment
├── careers/         # Career catalog, skill gap analysis, readiness score, dashboard
├── roadmaps/        # Personalized roadmaps + progress tracking
├── templates/       # Base + landing templates
└── static/          # CSS
```

## Setup

```bash
# 1. Create and activate a virtual environment
python -m venv venv
.\venv\Scripts\activate        # Windows
# source venv/bin/activate     # macOS/Linux

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run migrations
python manage.py migrate

# 4. Seed sample skills and careers
python manage.py seed_data

# 5. (Optional) create a superuser for the admin
python manage.py createsuperuser

# 6. Run the dev server
python manage.py runserver
```

Visit http://127.0.0.1:8000/, register, complete the assessment, and generate a
roadmap.

## PostgreSQL (optional)

Set the `DATABASE_URL` environment variable, e.g.:

```
DATABASE_URL=postgresql://user:password@localhost:5432/career_navigator
```

The app uses SQLite automatically when `DATABASE_URL` is not set.

## Tests

```bash
python manage.py test
```

## Environment Variables

| Variable            | Default                            | Purpose                          |
| ------------------- | ---------------------------------- | -------------------------------- |
| `DJANGO_SECRET_KEY` | dev-only value                     | Django secret key                |
| `DJANGO_DEBUG`      | `True`                             | Debug mode toggle                |
| `DJANGO_ALLOWED_HOSTS` | `localhost,127.0.0.1,testserver` | Allowed hosts                    |
| `DATABASE_URL`      | SQLite `db.sqlite3`                | DB connection string (PostgreSQL)|

## Design Notes

- **Models** are split across focused apps: `accounts.User`, `skills.Skill` /
  `SkillAssessment` / `SkillRating`, `careers.Career` / `CareerSkill`, and
  `roadmaps.Roadmap` / `RoadmapStep`.
- **Gap analysis** lives in `careers/services.py`. A skill is a gap when the
  user's self-rating (1-5) is below the target proficiency of 4. The readiness
  score is a weighted average using each career skill's importance.
- Each roadmap generates one step per skill gap; completing steps drives the
  progress percentage.
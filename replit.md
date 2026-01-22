# MindMetric AI

## Overview

MindMetric AI is a mental wellness platform that provides psychological assessments and personalized insights. Users complete a 15-question assessment, receive stress scores calculated via machine learning, and get AI-generated psychological summaries from Google Gemini. The platform also allows users to book sessions with a licensed psychologist, with optional WhatsApp and email notifications.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Backend Framework
- **Flask** serves as the web framework with Jinja2 templating
- **SQLAlchemy ORM** handles database operations with a declarative base pattern
- **Flask-Migrate** manages database schema migrations via Alembic
- **Flask-Login** provides session-based user authentication

### Database Design
- **PostgreSQL** in production (with SSL required), configured via `DATABASE_URL` environment variable
- Three main tables:
  - `User`: Profile info (name, age, address, email, password hash)
  - `Assessment`: Quiz responses stored as JSON, stress scores, ML predictions, Gemini summaries
  - `Booking`: Session appointments with consultation type, contact info, notification status

### AI/ML Services
- **Google Gemini AI** (`gemini-2.5-flash` model): Generates personalized psychological summaries based on assessment responses
- **Scikit-learn ML model**: Predicts recommended content types based on stress patterns (loads from `model.pkl` and `encoders.pkl` files)
- Both services include fallback mechanisms when external services are unavailable

### Frontend Architecture
- **Bootstrap 5** with dark theme for responsive UI
- **Vanilla JavaScript** for interactive features (quiz progress tracking, form validation, date restrictions)
- Custom CSS with animated gradient backgrounds and floating shapes for visual appeal

### Notification System
- **Twilio** for WhatsApp notifications on booking confirmations
- **SendGrid** for email notifications
- Both are optional and gracefully degrade when credentials aren't configured

## External Dependencies

### Required Services
- **PostgreSQL Database**: Connection string via `DATABASE_URL` environment variable (handles `postgres://` to `postgresql://` conversion automatically)
- **Google Gemini API**: Requires `GEMINI_API_KEY` for psychological summary generation

### Optional Services
- **Twilio**: `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`, `TWILIO_PHONE_NUMBER` for WhatsApp notifications
- **SendGrid**: `SENDGRID_API_KEY` for email notifications

### Key Python Packages
- `flask`, `flask-sqlalchemy`, `flask-migrate`, `flask-login` for web framework
- `google-genai` for Gemini AI integration
- `scikit-learn`, `pandas`, `numpy` for ML predictions
- `twilio`, `sendgrid` for notifications
- `psycopg2-binary` for PostgreSQL connectivity
- `xhtml2pdf` for PDF generation capabilities
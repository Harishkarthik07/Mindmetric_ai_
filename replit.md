# MindMetric AI - Mental Wellness Platform

## Overview

MindMetric AI is a comprehensive mental wellness platform that combines machine learning predictions with AI-powered psychological insights. The application provides users with personalized mental health assessments, stress scoring, and the ability to book sessions with licensed psychologists. The platform integrates Google Gemini AI for generating detailed psychological summaries and uses machine learning models for content type predictions.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Backend Architecture
- **Framework**: Flask (Python web framework)
- **Database**: SQLAlchemy ORM with support for SQLite (default) and PostgreSQL
- **Authentication**: Flask-Login for session management
- **AI Integration**: Google Gemini AI for psychological analysis
- **ML Component**: Scikit-learn based machine learning models for predictions

### Frontend Architecture
- **Template Engine**: Jinja2 (Flask's default)
- **CSS Framework**: Bootstrap 5 with dark theme
- **Icons**: Bootstrap Icons
- **JavaScript**: Vanilla JavaScript for interactive features
- **Responsive Design**: Mobile-first approach with Bootstrap grid system

### Database Schema
- **User**: Stores user profile information (name, age, address, email, password)
- **Assessment**: Stores quiz responses, stress scores, ML predictions, and AI summaries
- **Booking**: Manages psychology session appointments

## Key Components

### Authentication System
- User registration and login functionality
- Password hashing using Werkzeug security
- Session management with Flask-Login
- Protected routes requiring authentication

### Assessment Engine
- 15-question psychological assessment
- Two-part questionnaire: personality/stress indicators (10 questions) and stress levels (5 questions)
- Real-time progress tracking
- Response validation and submission

### AI Integration Services
- **Gemini Service**: Generates personalized psychological summaries using Google's Gemini AI
- **ML Service**: Provides stress score calculations and content type predictions
- **Fallback Mechanisms**: Handles cases where AI services are unavailable

### Booking System
- Session scheduling with licensed psychologist
- Date and time selection with validation
- Booking confirmation and management
- Session notes and status tracking

## Data Flow

1. **User Registration**: New users create accounts with personal information
2. **Assessment Process**: Users complete 15-question psychological assessment
3. **Data Processing**: 
   - Responses are processed to calculate stress scores
   - ML model generates content type predictions
   - Gemini AI creates personalized psychological summaries
4. **Results Display**: Combined insights presented to user
5. **Booking Flow**: Users can schedule psychology sessions based on results
6. **Data Persistence**: All data stored in relational database with proper relationships

## External Dependencies

### AI Services
- **Google Gemini AI**: For generating detailed psychological summaries and personalized insights
- **Scikit-learn**: For machine learning model predictions (stored as pickle files)

### Third-party Libraries
- **Flask ecosystem**: Flask, Flask-SQLAlchemy, Flask-Login
- **Security**: Werkzeug for password hashing
- **Data processing**: Pandas, NumPy for ML operations
- **Frontend**: Bootstrap 5, Bootstrap Icons

### Environment Variables
- `GEMINI_API_KEY`: Google Gemini AI API key
- `DATABASE_URL`: Database connection string
- `SESSION_SECRET`: Flask session secret key

## Deployment Strategy

### Application Structure
- **Entry Point**: `main.py` runs the Flask application
- **Configuration**: Environment-based configuration with fallback defaults
- **Static Assets**: CSS, JavaScript, and other static files served by Flask
- **Database**: SQLAlchemy with automatic table creation on startup

### Production Considerations
- **Proxy Support**: ProxyFix middleware for handling reverse proxy headers
- **Database Pooling**: Connection pooling with recycle and pre-ping options
- **Error Handling**: Comprehensive error handling for AI services and database operations
- **Logging**: Debug-level logging for development, configurable for production

### Security Features
- **Session Management**: Secure session handling with configurable secret keys
- **Password Security**: Hashed passwords using Werkzeug
- **Input Validation**: Form validation and sanitization
- **Authentication**: Login required decorators for protected routes

The application follows a traditional MVC pattern with clear separation of concerns, making it maintainable and scalable for mental health service delivery.
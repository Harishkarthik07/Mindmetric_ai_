from app import db
from flask_login import UserMixin
from datetime import datetime

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    address = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    assessments = db.relationship('Assessment', backref='user', lazy=True)
    bookings = db.relationship('Booking', backref='user', lazy=True)

class Assessment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    stress_score = db.Column(db.Float, nullable=False)
    ml_prediction = db.Column(db.String(100), nullable=False)
    gemini_summary = db.Column(db.Text, nullable=True)
    responses = db.Column(db.Text, nullable=False)  # JSON string of all responses
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    session_date = db.Column(db.Date, nullable=False)
    session_time = db.Column(db.Time, nullable=False)
    consultation_type = db.Column(db.String(50), nullable=False, default='video')  # 'video' or 'in-person'
    phone_number = db.Column(db.String(20), nullable=False)
    emergency_contact = db.Column(db.String(100), nullable=True)
    status = db.Column(db.String(20), default='confirmed')
    notes = db.Column(db.Text, nullable=True)
    notification_sent = db.Column(db.Boolean, default=False)
    psychologist_notified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

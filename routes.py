from flask import render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app import app, db
from models import User, Assessment, Booking
from ml_service import predict_content_type, calculate_stress_score
from gemini_service import generate_psychological_summary
import json
import csv
import os
from datetime import datetime, date, time

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('quiz'))
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        address = request.form['address']
        email = request.form['email']
        password = request.form['password']
        
        # Check if user already exists
        if User.query.filter_by(email=email).first():
            flash('Email already exists. Please use a different email or login.', 'error')
            return render_template('signup.html')
        
        # Create new user
        user = User(
            name=name,
            age=int(age),
            address=address,
            email=email,
            password_hash=generate_password_hash(password)
        )
        
        db.session.add(user)
        db.session.commit()
        
        login_user(user)
        flash('Account created successfully!', 'success')
        return redirect(url_for('quiz'))
    
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        user = User.query.filter_by(email=email).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('quiz'))
        else:
            flash('Invalid email or password.', 'error')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/quiz')
@login_required
def quiz():
    return render_template('quiz.html')

@app.route('/submit_quiz', methods=['POST'])
@login_required
def submit_quiz():
    try:
        # Collect all form responses
        responses = {}
        
        # Personality/stress questions (Q1-Q10)
        for i in range(1, 11):
            responses[f'q{i}'] = request.form.get(f'q{i}')
        
        # Stress level questions (Q11-Q15)
        stress_responses = []
        for i in range(11, 16):
            stress_level = request.form.get(f'q{i}')
            if stress_level == 'Low':
                stress_responses.append(1)
            elif stress_level == 'Medium':
                stress_responses.append(2)
            elif stress_level == 'High':
                stress_responses.append(3)
            responses[f'q{i}'] = stress_level
        
        # Calculate stress score (0-10)
        stress_score = calculate_stress_score(stress_responses)
        
        # Get ML prediction
        ml_prediction = predict_content_type(responses, stress_score)
        
        # Generate Gemini summary
        gemini_summary = generate_psychological_summary(responses, stress_score, current_user.age)
        
        # Save assessment to database
        assessment = Assessment(
            user_id=current_user.id,
            stress_score=stress_score,
            ml_prediction=ml_prediction,
            gemini_summary=gemini_summary,
            responses=json.dumps(responses)
        )
        db.session.add(assessment)
        db.session.commit()
        
        # Log to CSV
        log_to_csv(current_user.email, stress_score, ml_prediction, gemini_summary)
        
        return redirect(url_for('result', assessment_id=assessment.id))
        
    except Exception as e:
        app.logger.error(f"Error processing quiz: {str(e)}")
        flash('An error occurred while processing your quiz. Please try again.', 'error')
        return redirect(url_for('quiz'))

@app.route('/result/<int:assessment_id>')
@login_required
def result(assessment_id):
    assessment = Assessment.query.get_or_404(assessment_id)
    
    # Ensure user can only view their own assessments
    if assessment.user_id != current_user.id:
        flash('Access denied.', 'error')
        return redirect(url_for('quiz'))
    
    return render_template('result.html', assessment=assessment)

@app.route('/book')
@login_required
def booking():
    from datetime import datetime, timedelta
    return render_template('booking.html', datetime=datetime, timedelta=timedelta)

@app.route('/submit_booking', methods=['POST'])
@login_required
def submit_booking():
    try:
        # Get form data
        session_date = datetime.strptime(request.form['date'], '%Y-%m-%d').date()
        session_time = datetime.strptime(request.form['time'], '%H:%M').time()
        consultation_type = request.form.get('consultation_type', 'video')
        phone_number = request.form.get('phone', '')
        emergency_contact = request.form.get('emergency_contact', '')
        notes = request.form.get('notes', '')
        
        # Validate required fields
        if not phone_number:
            flash('Phone number is required for booking confirmation.', 'error')
            return redirect(url_for('booking'))
        
        # Check if slot is already booked
        existing_booking = Booking.query.filter_by(
            session_date=session_date,
            session_time=session_time
        ).first()
        
        if existing_booking:
            flash('This time slot is already booked. Please choose another time.', 'error')
            return redirect(url_for('booking'))
        
        # Create new booking
        booking = Booking(
            user_id=current_user.id,
            session_date=session_date,
            session_time=session_time,
            consultation_type=consultation_type,
            phone_number=phone_number,
            emergency_contact=emergency_contact,
            notes=notes
        )
        
        db.session.add(booking)
        db.session.commit()
        
        # Send notifications
        try:
            from notification_service import send_booking_notifications
            notification_results = send_booking_notifications(booking, current_user)
            
            # Update booking notification status
            booking.notification_sent = notification_results['whatsapp'] or notification_results['email']
            booking.psychologist_notified = notification_results['psychologist']
            db.session.commit()
            
            # Flash success message based on notification results
            success_msg = 'Your session has been booked successfully!'
            if notification_results['whatsapp']:
                success_msg += ' WhatsApp confirmation sent.'
            if notification_results['email']:
                success_msg += ' Email confirmation sent.'
            
            flash(success_msg, 'success')
            
        except Exception as notification_error:
            app.logger.error(f"Notification error: {notification_error}")
            flash('Your session has been booked successfully! Confirmation notifications may be delayed.', 'warning')
        
        return redirect(url_for('booking_confirmation', booking_id=booking.id))
        
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Error processing booking: {str(e)}")
        flash('An error occurred while booking your session. Please try again.', 'error')
        return redirect(url_for('booking'))

@app.route('/booking_confirmation/<int:booking_id>')
@login_required
def booking_confirmation(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    
    # Ensure user can only view their own bookings
    if booking.user_id != current_user.id:
        flash('Access denied.', 'error')
        return redirect(url_for('booking'))
    
    return render_template('booking_confirmation.html', booking=booking)

def log_to_csv(email, stress_score, ml_prediction, gemini_summary):
    """Log assessment results to CSV file"""
    csv_file = 'assessment_logs.csv'
    file_exists = os.path.isfile(csv_file)
    
    with open(csv_file, 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        
        # Write header if file is new
        if not file_exists:
            writer.writerow(['Timestamp', 'Email', 'Stress Score', 'ML Prediction', 'Gemini Summary'])
        
        # Write data
        writer.writerow([
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            email,
            stress_score,
            ml_prediction,
            gemini_summary.replace('\n', ' ').replace('\r', ' ')[:500]  # Limit summary length
        ])

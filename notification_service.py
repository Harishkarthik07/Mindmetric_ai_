"""
Notification Service for MindMetric AI
Handles WhatsApp and Email notifications for booking confirmations
"""
import os
import logging
from datetime import datetime
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from twilio.rest import Client

# Configuration
TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.environ.get("TWILIO_PHONE_NUMBER")
SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY")

def send_whatsapp_notification(to_phone, user_name, session_date, session_time, consultation_type):
    """Send WhatsApp notification for booking confirmation"""
    try:
        if not all([TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER]):
            logging.warning("Twilio credentials not configured")
            return False
            
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        
        # Format message
        message_body = f"""
🌟 *MindMetric AI - Booking Confirmed* 🌟

Hello {user_name}! Your psychology session has been successfully booked.

📅 *Date:* {session_date.strftime('%B %d, %Y')}
🕐 *Time:* {session_time.strftime('%I:%M %p')}
💬 *Type:* {consultation_type.title()}
👩‍⚕️ *Psychologist:* Meghana KS

{"📞 *Meeting:* Video call link will be sent 30 minutes before session" if consultation_type == 'video' else "🏥 *Location:* MindMetric AI Clinic, Bangalore"}

*Important Notes:*
• Please arrive 5 minutes early
• Bring any relevant documents
• Contact us if you need to reschedule

Thank you for choosing MindMetric AI for your mental wellness journey! 💚

_This is an automated message. Reply STOP to opt out._
        """.strip()
        
        # Send WhatsApp message
        message = client.messages.create(
            body=message_body,
            from_=f'whatsapp:{TWILIO_PHONE_NUMBER}',
            to=f'whatsapp:{to_phone}'
        )
        
        logging.info(f"WhatsApp notification sent successfully. SID: {message.sid}")
        return True
        
    except Exception as e:
        logging.error(f"Failed to send WhatsApp notification: {e}")
        return False

def send_email_notification(to_email, user_name, session_date, session_time, consultation_type):
    """Send email notification for booking confirmation"""
    try:
        if not SENDGRID_API_KEY:
            logging.warning("SendGrid API key not configured")
            return False
            
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        
        # HTML email template
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; }}
                .header {{ background: linear-gradient(135deg, #667eea, #764ba2); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                .content {{ padding: 30px; background: #f8f9fa; }}
                .booking-details {{ background: white; padding: 20px; border-radius: 10px; margin: 20px 0; border-left: 5px solid #667eea; }}
                .detail-item {{ margin: 10px 0; }}
                .label {{ font-weight: bold; color: #2c3e50; }}
                .value {{ color: #495057; }}
                .footer {{ background: #2c3e50; color: white; padding: 20px; text-align: center; border-radius: 0 0 10px 10px; }}
                .highlight {{ background: linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1)); padding: 15px; border-radius: 8px; margin: 15px 0; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🌟 Booking Confirmed!</h1>
                <p>Your psychology session at MindMetric AI</p>
            </div>
            
            <div class="content">
                <p>Dear {user_name},</p>
                <p>Thank you for booking your psychology session with MindMetric AI. We're excited to support you on your mental wellness journey!</p>
                
                <div class="booking-details">
                    <h3>📋 Session Details</h3>
                    <div class="detail-item">
                        <span class="label">📅 Date:</span>
                        <span class="value">{session_date.strftime('%A, %B %d, %Y')}</span>
                    </div>
                    <div class="detail-item">
                        <span class="label">🕐 Time:</span>
                        <span class="value">{session_time.strftime('%I:%M %p')}</span>
                    </div>
                    <div class="detail-item">
                        <span class="label">💬 Consultation Type:</span>
                        <span class="value">{consultation_type.title()}</span>
                    </div>
                    <div class="detail-item">
                        <span class="label">👩‍⚕️ Psychologist:</span>
                        <span class="value">Meghana KS, Licensed Clinical Psychologist</span>
                    </div>
                </div>
                
                <div class="highlight">
                    {"<h4>📞 Video Call Instructions</h4><p>You will receive a secure video call link 30 minutes before your session. Please ensure you have a stable internet connection and a quiet environment.</p>" if consultation_type == 'video' else "<h4>🏥 In-Person Session</h4><p><strong>Location:</strong> MindMetric AI Clinic<br>Bangalore, India<br><br>Please arrive 5 minutes early for check-in.</p>"}
                </div>
                
                <h4>📝 Important Reminders:</h4>
                <ul>
                    <li>Please arrive 5 minutes early</li>
                    <li>Bring any relevant documents or previous assessments</li>
                    <li>Contact us at least 24 hours in advance if you need to reschedule</li>
                    <li>Ensure privacy and minimal distractions during the session</li>
                </ul>
                
                <p>If you have any questions or need to make changes to your appointment, please contact us immediately.</p>
                
                <p>We look forward to supporting your mental wellness journey!</p>
                
                <p>Warm regards,<br>
                <strong>The MindMetric AI Team</strong></p>
            </div>
            
            <div class="footer">
                <p>MindMetric AI - Your Mental Wellness Partner</p>
                <p>This is an automated confirmation email.</p>
            </div>
        </body>
        </html>
        """
        
        # Plain text version
        text_content = f"""
        MindMetric AI - Booking Confirmed!
        
        Dear {user_name},
        
        Your psychology session has been successfully booked:
        
        Date: {session_date.strftime('%A, %B %d, %Y')}
        Time: {session_time.strftime('%I:%M %p')}
        Type: {consultation_type.title()}
        Psychologist: Meghana KS
        
        {"Video call link will be sent 30 minutes before your session." if consultation_type == 'video' else "Location: MindMetric AI Clinic, Bangalore"}
        
        Important reminders:
        - Arrive 5 minutes early
        - Bring relevant documents
        - Contact us for rescheduling
        
        Thank you for choosing MindMetric AI!
        
        Best regards,
        The MindMetric AI Team
        """
        
        message = Mail(
            from_email='noreply@mindmetric.ai',
            to_emails=to_email,
            subject=f'Booking Confirmed - {session_date.strftime("%B %d, %Y")} at {session_time.strftime("%I:%M %p")}',
            html_content=html_content,
            plain_text_content=text_content
        )
        
        response = sg.send(message)
        logging.info(f"Email notification sent successfully. Status: {response.status_code}")
        return True
        
    except Exception as e:
        logging.error(f"Failed to send email notification: {e}")
        return False

def notify_psychologist(booking_data):
    """Send notification to psychologist about new booking"""
    try:
        if not SENDGRID_API_KEY:
            logging.warning("SendGrid API key not configured")
            return False
            
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .header {{ background: #2c3e50; color: white; padding: 20px; text-align: center; }}
                .content {{ padding: 20px; }}
                .booking-info {{ background: #f8f9fa; padding: 15px; border-radius: 5px; margin: 15px 0; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h2>New Booking Alert - MindMetric AI</h2>
            </div>
            <div class="content">
                <p>Dear Meghana,</p>
                <p>A new psychology session has been booked through MindMetric AI.</p>
                
                <div class="booking-info">
                    <h3>Booking Details:</h3>
                    <p><strong>Patient:</strong> {booking_data['user_name']}</p>
                    <p><strong>Email:</strong> {booking_data['user_email']}</p>
                    <p><strong>Phone:</strong> {booking_data['phone_number']}</p>
                    <p><strong>Date:</strong> {booking_data['session_date'].strftime('%A, %B %d, %Y')}</p>
                    <p><strong>Time:</strong> {booking_data['session_time'].strftime('%I:%M %p')}</p>
                    <p><strong>Type:</strong> {booking_data['consultation_type'].title()}</p>
                    <p><strong>Booking ID:</strong> #{booking_data['booking_id']}</p>
                </div>
                
                <p>Please prepare for the session and confirm your availability.</p>
                
                <p>Best regards,<br>MindMetric AI System</p>
            </div>
        </body>
        </html>
        """
        
        message = Mail(
            from_email='system@mindmetric.ai',
            to_emails='meghana@mindmetric.ai',  # Psychologist's email
            subject=f'New Booking Alert - {booking_data["session_date"].strftime("%B %d, %Y")}',
            html_content=html_content
        )
        
        response = sg.send(message)
        logging.info(f"Psychologist notification sent successfully. Status: {response.status_code}")
        return True
        
    except Exception as e:
        logging.error(f"Failed to send psychologist notification: {e}")
        return False

def send_booking_notifications(booking, user):
    """Send all booking notifications (WhatsApp, Email, Psychologist)"""
    results = {
        'whatsapp': False,
        'email': False,
        'psychologist': False
    }
    
    # Send WhatsApp notification to user
    if booking.phone_number:
        results['whatsapp'] = send_whatsapp_notification(
            booking.phone_number,
            user.name,
            booking.session_date,
            booking.session_time,
            booking.consultation_type
        )
    
    # Send email notification to user
    results['email'] = send_email_notification(
        user.email,
        user.name,
        booking.session_date,
        booking.session_time,
        booking.consultation_type
    )
    
    # Send notification to psychologist
    booking_data = {
        'user_name': user.name,
        'user_email': user.email,
        'phone_number': booking.phone_number,
        'session_date': booking.session_date,
        'session_time': booking.session_time,
        'consultation_type': booking.consultation_type,
        'booking_id': booking.id
    }
    results['psychologist'] = notify_psychologist(booking_data)
    
    return results
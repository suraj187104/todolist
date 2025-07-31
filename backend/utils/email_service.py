from flask_mail import Mail, Message
from flask import current_app
import threading

mail = Mail()

def send_async_email(app, msg):
    """Send email asynchronously"""
    with app.app_context():
        try:
            mail.send(msg)
            print(f"Email sent successfully to {msg.recipients}")
        except Exception as e:
            print(f"Failed to send email: {e}")

def send_email(subject, recipients, text_body=None, html_body=None):
    """Send email with both text and HTML body"""
    try:
        msg = Message(
            subject=subject,
            recipients=recipients if isinstance(recipients, list) else [recipients],
            body=text_body,
            html=html_body
        )
        
        # Send email in background thread
        thread = threading.Thread(
            target=send_async_email,
            args=(current_app._get_current_object(), msg)
        )
        thread.start()
        return True
    except Exception as e:
        print(f"Error preparing email: {e}")
        return False

def send_todo_notification(user_email, user_name, todo_title, todo_description=None):
    """Send email notification when a new TODO is created"""
    subject = f"New TODO Created: {todo_title}"
    
    # Text version
    text_body = f"""
    Hi {user_name},
    
    You've successfully created a new TODO item:
    
    Title: {todo_title}
    {f'Description: {todo_description}' if todo_description else ''}
    
    You can manage your TODOs by logging into your account.
    
    Best regards,
    TODO App Team
    """
    
    # HTML version
    html_body = f"""
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
            <h2 style="color: #4CAF50;">New TODO Created! 📝</h2>
            
            <p>Hi <strong>{user_name}</strong>,</p>
            
            <p>You've successfully created a new TODO item:</p>
            
            <div style="background-color: #f5f5f5; padding: 15px; border-radius: 5px; margin: 20px 0;">
                <h3 style="margin-top: 0; color: #333;">📌 {todo_title}</h3>
                {f'<p style="margin-bottom: 0;"><strong>Description:</strong> {todo_description}</p>' if todo_description else ''}
            </div>
            
            <p>You can manage your TODOs by logging into your account.</p>
            
            <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #eee;">
                <p style="color: #666; font-size: 14px;">
                    Best regards,<br>
                    TODO App Team
                </p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return send_email(subject, user_email, text_body, html_body)

def send_welcome_email(user_email, user_name):
    """Send welcome email to new users"""
    subject = "Welcome to TODO App! 🎉"
    
    text_body = f"""
    Hi {user_name},
    
    Welcome to TODO App! We're excited to have you on board.
    
    You can now:
    - Create and manage your TODO items
    - Set priorities and due dates
    - Get email notifications for new TODOs
    
    Start organizing your tasks today!
    
    Best regards,
    TODO App Team
    """
    
    html_body = f"""
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
            <h2 style="color: #4CAF50;">Welcome to TODO App! 🎉</h2>
            
            <p>Hi <strong>{user_name}</strong>,</p>
            
            <p>Welcome to TODO App! We're excited to have you on board.</p>
            
            <div style="background-color: #f0f8ff; padding: 20px; border-radius: 5px; margin: 20px 0;">
                <h3 style="margin-top: 0; color: #333;">What you can do:</h3>
                <ul style="padding-left: 20px;">
                    <li>✅ Create and manage your TODO items</li>
                    <li>🎯 Set priorities and due dates</li>
                    <li>📧 Get email notifications for new TODOs</li>
                    <li>📱 Access from anywhere</li>
                </ul>
            </div>
            
            <p style="text-align: center;">
                <a href="#" style="background-color: #4CAF50; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; display: inline-block;">
                    Start Managing Your TODOs
                </a>
            </p>
            
            <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #eee;">
                <p style="color: #666; font-size: 14px;">
                    Best regards,<br>
                    TODO App Team
                </p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return send_email(subject, user_email, text_body, html_body)

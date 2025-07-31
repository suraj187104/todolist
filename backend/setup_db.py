#!/usr/bin/env python3
"""
Database setup and initialization script
"""
import os
import sys
from app import create_app
from models.models import db, User, Todo

def setup_database():
    """Create database tables and add sample data"""
    app = create_app()
    
    with app.app_context():
        print("Creating database tables...")
        db.create_all()
        print("✅ Database tables created successfully!")
        
        # Check if we should add sample data
        if len(sys.argv) > 1 and sys.argv[1] == '--sample-data':
            print("\nAdding sample data...")
            add_sample_data()
        
        print("\n🎉 Database setup complete!")

def add_sample_data():
    """Add sample users and todos for testing"""
    try:
        # Create sample user
        sample_user = User(
            email='test@example.com',
            first_name='Test',
            last_name='User',
            password='password123'
        )
        
        db.session.add(sample_user)
        db.session.commit()
        
        # Create sample todos
        sample_todos = [
            Todo(
                title='Complete TODO App',
                description='Finish building the full-stack TODO application for internship',
                priority='high',
                user_id=sample_user.id
            ),
            Todo(
                title='Set up PostgreSQL',
                description='Install and configure PostgreSQL database',
                priority='medium',
                user_id=sample_user.id
            ),
            Todo(
                title='Deploy to Render',
                description='Deploy both frontend and backend to Render hosting',
                priority='medium',
                user_id=sample_user.id
            )
        ]
        
        for todo in sample_todos:
            db.session.add(todo)
        
        db.session.commit()
        print("✅ Sample data added successfully!")
        print(f"Sample user: test@example.com / password123")
        
    except Exception as e:
        print(f"❌ Error adding sample data: {e}")
        db.session.rollback()

def reset_database():
    """Drop all tables and recreate them"""
    app = create_app()
    
    with app.app_context():
        print("Dropping all database tables...")
        db.drop_all()
        print("Creating database tables...")
        db.create_all()
        print("✅ Database reset complete!")

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--reset':
        reset_database()
    else:
        setup_database()

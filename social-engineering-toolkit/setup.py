#!/usr/bin/env python3
"""
Social Engineering Toolkit Setup Script
This script sets up the database and creates initial demo accounts.
"""

import sqlite3
import sys
import os
from werkzeug.security import generate_password_hash

def create_database():
    """Create the SQLite database and tables"""
    if not os.path.exists('data'):
        os.makedirs('data')
    
    conn = sqlite3.connect('data/setoolkit.db')
    cursor = conn.cursor()
    
    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            department TEXT,
            password_hash TEXT NOT NULL,
            is_admin BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Campaigns table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS campaigns (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            type TEXT NOT NULL,
            description TEXT,
            template_id INTEGER,
            created_by INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status TEXT DEFAULT 'draft'
        )
    ''')
    
    # Campaign results table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS campaign_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            campaign_id INTEGER,
            user_id INTEGER,
            clicked BOOLEAN DEFAULT FALSE,
            submitted_data BOOLEAN DEFAULT FALSE,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            ip_address TEXT,
            user_agent TEXT
        )
    ''')
    
    # Training modules table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS training_modules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            content TEXT,
            quiz_questions TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # User training progress table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_training_progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            module_id INTEGER,
            completed BOOLEAN DEFAULT FALSE,
            score INTEGER,
            completed_at TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (module_id) REFERENCES training_modules (id)
        )
    ''')
    
    conn.commit()
    print("✓ Database tables created successfully")
    return conn

def create_demo_users(conn):
    """Create demo user accounts"""
    cursor = conn.cursor()
    
    # Admin user
    admin_password = generate_password_hash('admin123')
    cursor.execute('''
        INSERT OR IGNORE INTO users (email, name, department, password_hash, is_admin)
        VALUES (?, ?, ?, ?, ?)
    ''', ('admin@company.com', 'System Administrator', 'IT', admin_password, True))
    
    # Regular user
    user_password = generate_password_hash('user123')
    cursor.execute('''
        INSERT OR IGNORE INTO users (email, name, department, password_hash, is_admin)
        VALUES (?, ?, ?, ?, ?)
    ''', ('user@company.com', 'John Doe', 'Sales', user_password, False))
    
    # Additional demo users
    demo_users = [
        ('jane.smith@company.com', 'Jane Smith', 'HR', 'demo123', False),
        ('mike.jones@company.com', 'Mike Jones', 'Finance', 'demo123', False),
        ('sarah.wilson@company.com', 'Sarah Wilson', 'Marketing', 'demo123', False),
    ]
    
    for email, name, dept, password, is_admin in demo_users:
        password_hash = generate_password_hash(password)
        cursor.execute('''
            INSERT OR IGNORE INTO users (email, name, department, password_hash, is_admin)
            VALUES (?, ?, ?, ?, ?)
        ''', (email, name, dept, password_hash, is_admin))
    
    conn.commit()
    print("✓ Demo user accounts created")

def create_training_modules(conn):
    """Create sample training modules"""
    cursor = conn.cursor()
    
    modules = [
        (
            'Phishing Awareness 101',
            'Learn to identify and avoid phishing attacks',
            '''<h3>Understanding Phishing</h3>
            <p>Phishing is a cybercrime where attackers impersonate legitimate organizations to steal sensitive information.</p>
            <h4>Common Red Flags:</h4>
            <ul>
                <li>Urgent or threatening language</li>
                <li>Generic greetings</li>
                <li>Suspicious sender addresses</li>
                <li>Unexpected attachments or links</li>
                <li>Poor grammar and spelling</li>
            </ul>'''
        ),
        (
            'Password Security',
            'Best practices for creating and managing secure passwords',
            '''<h3>Strong Password Guidelines</h3>
            <p>Your password is your first line of defense against unauthorized access.</p>
            <h4>Password Requirements:</h4>
            <ul>
                <li>At least 12 characters long</li>
                <li>Mix of uppercase, lowercase, numbers, and symbols</li>
                <li>Avoid personal information</li>
                <li>Unique for each account</li>
                <li>Use a password manager</li>
            </ul>'''
        ),
        (
            'Social Engineering Defense',
            'Recognize and defend against social engineering tactics',
            '''<h3>Social Engineering Tactics</h3>
            <p>Social engineering exploits human psychology to manipulate people.</p>
            <h4>Common Techniques:</h4>
            <ul>
                <li>Pretexting - Creating false scenarios</li>
                <li>Authority - Impersonating figures of authority</li>
                <li>Urgency - Creating time pressure</li>
                <li>Familiarity - Using personal information</li>
            </ul>'''
        )
    ]
    
    for title, description, content in modules:
        cursor.execute('''
            INSERT OR IGNORE INTO training_modules (title, description, content)
            VALUES (?, ?, ?)
        ''', (title, description, content))
    
    conn.commit()
    print("✓ Training modules created")

def create_sample_campaigns(conn):
    """Create sample campaigns for demonstration"""
    cursor = conn.cursor()
    
    # Get admin user ID
    cursor.execute('SELECT id FROM users WHERE is_admin = 1 LIMIT 1')
    admin_user = cursor.fetchone()
    if not admin_user:
        print("⚠ No admin user found, skipping sample campaigns")
        return
    
    admin_id = admin_user[0]
    
    campaigns = [
        ('Q1 Phishing Assessment', 'phishing', 'Quarterly phishing awareness test for all employees', admin_id, 'completed'),
        ('Banking Alert Simulation', 'phishing', 'Simulated banking security alert campaign', admin_id, 'active'),
        ('IT Support Vishing Test', 'vishing', 'Voice-based social engineering test', admin_id, 'draft'),
    ]
    
    for name, campaign_type, description, created_by, status in campaigns:
        cursor.execute('''
            INSERT OR IGNORE INTO campaigns (name, type, description, created_by, status)
            VALUES (?, ?, ?, ?, ?)
        ''', (name, campaign_type, description, created_by, status))
    
    conn.commit()
    print("✓ Sample campaigns created")

def main():
    """Main setup function"""
    print("Social Engineering Toolkit - Setup")
    print("=" * 40)
    
    try:
        # Create database and tables
        conn = create_database()
        
        # Create demo data
        create_demo_users(conn)
        create_training_modules(conn)
        create_sample_campaigns(conn)
        
        conn.close()
        
        print("\n✓ Setup completed successfully!")
        print("\nDemo Login Credentials:")
        print("Admin: admin@company.com / admin123")
        print("User:  user@company.com / user123")
        print("\nTo start the application, run:")
        print("cd src && python app.py")
        
    except Exception as e:
        print(f"\n✗ Setup failed: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()


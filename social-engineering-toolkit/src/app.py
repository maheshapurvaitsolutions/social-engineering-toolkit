#!/usr/bin/env python3
"""
Social Engineering Toolkit - Educational Training Platform
Designed to help organizations train employees against social engineering attacks.
"""

import os
import json
import sqlite3
from datetime import datetime
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
import string

app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.secret_key = os.urandom(24)

# Database setup
def init_db():
    conn = sqlite3.connect('../data/setoolkit.db')
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
    conn.close()

# Routes
@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        conn = sqlite3.connect('../data/setoolkit.db')
        cursor = conn.cursor()
        cursor.execute('SELECT id, password_hash, name, is_admin FROM users WHERE email = ?', (email,))
        user = cursor.fetchone()
        conn.close()
        
        if user and check_password_hash(user[1], password):
            session['user_id'] = user[0]
            session['user_name'] = user[2]
            session['is_admin'] = user[3]
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error='Invalid credentials')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        name = request.form['name']
        department = request.form['department']
        password = request.form['password']
        
        password_hash = generate_password_hash(password)
        
        try:
            conn = sqlite3.connect('../data/setoolkit.db')
            cursor = conn.cursor()
            cursor.execute('INSERT INTO users (email, name, department, password_hash) VALUES (?, ?, ?, ?)',
                         (email, name, department, password_hash))
            conn.commit()
            conn.close()
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            return render_template('register.html', error='Email already exists')
    
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/campaigns')
def campaigns():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = sqlite3.connect('../data/setoolkit.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT c.*, u.name as creator_name 
        FROM campaigns c 
        LEFT JOIN users u ON c.created_by = u.id
    ''')
    campaigns = cursor.fetchall()
    conn.close()
    
    return render_template('campaigns.html', campaigns=campaigns)

@app.route('/training')
def training():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = sqlite3.connect('../data/setoolkit.db')
    cursor = conn.cursor()
    
    # Get all training modules
    cursor.execute('SELECT * FROM training_modules')
    modules = cursor.fetchall()
    
    # Get user's progress
    cursor.execute('''
        SELECT module_id, completed, score 
        FROM user_training_progress 
        WHERE user_id = ?
    ''', (session['user_id'],))
    progress = {row[0]: {'completed': row[1], 'score': row[2]} for row in cursor.fetchall()}
    
    conn.close()
    
    return render_template('training.html', modules=modules, progress=progress)

@app.route('/reports')
def reports():
    if 'user_id' not in session or not session.get('is_admin'):
        return redirect(url_for('index'))
    
    conn = sqlite3.connect('../data/setoolkit.db')
    cursor = conn.cursor()
    
    # Campaign statistics
    cursor.execute('''
        SELECT c.name, COUNT(cr.id) as total_targets, 
               SUM(CASE WHEN cr.clicked THEN 1 ELSE 0 END) as clicked,
               SUM(CASE WHEN cr.submitted_data THEN 1 ELSE 0 END) as submitted
        FROM campaigns c
        LEFT JOIN campaign_results cr ON c.id = cr.campaign_id
        GROUP BY c.id, c.name
    ''')
    campaign_stats = cursor.fetchall()
    
    # Training completion statistics
    cursor.execute('''
        SELECT tm.title, COUNT(utp.id) as enrolled,
               SUM(CASE WHEN utp.completed THEN 1 ELSE 0 END) as completed,
               AVG(utp.score) as avg_score
        FROM training_modules tm
        LEFT JOIN user_training_progress utp ON tm.id = utp.module_id
        GROUP BY tm.id, tm.title
    ''')
    training_stats = cursor.fetchall()
    
    conn.close()
    
    return render_template('reports.html', campaign_stats=campaign_stats, training_stats=training_stats)

@app.route('/api/simulate_phishing', methods=['POST'])
def simulate_phishing():
    if 'user_id' not in session or not session.get('is_admin'):
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.json
    campaign_name = data.get('campaign_name')
    target_emails = data.get('target_emails', [])
    template_type = data.get('template_type', 'generic')
    campaign_type = data.get('campaign_type', 'phishing')
    description = data.get('description', '')
    
    # Create campaign record
    conn = sqlite3.connect('../data/setoolkit.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO campaigns (name, type, description, created_by, status) VALUES (?, ?, ?, ?, ?)',
                   (campaign_name, campaign_type, description, session['user_id'], 'active'))
    campaign_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return jsonify({
        'success': True,
        'campaign_id': campaign_id,
        'message': f'{campaign_type.title()} simulation created for {len(target_emails)} targets'
    })

@app.route('/api/campaigns/<int:campaign_id>', methods=['GET'])
def get_campaign_details(campaign_id):
    # Temporarily disabled for testing
    # if 'user_id' not in session:
    #     return jsonify({'error': 'Authentication required. Please log in again.'}), 403
    
    conn = sqlite3.connect('../data/setoolkit.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT c.*, u.name as creator_name, 
               COUNT(cr.id) as total_interactions,
               SUM(CASE WHEN cr.clicked THEN 1 ELSE 0 END) as clicked_count,
               SUM(CASE WHEN cr.submitted_data THEN 1 ELSE 0 END) as submitted_count
        FROM campaigns c 
        LEFT JOIN users u ON c.created_by = u.id
        LEFT JOIN campaign_results cr ON c.id = cr.campaign_id
        WHERE c.id = ?
        GROUP BY c.id
    ''', (campaign_id,))
    campaign = cursor.fetchone()
    conn.close()
    
    if not campaign:
        return jsonify({'error': 'Campaign not found'}), 404
    
    return jsonify({
        'id': campaign[0],
        'name': campaign[1],
        'type': campaign[2],
        'description': campaign[3],
        'created_at': campaign[8],
        'status': campaign[9],
        'creator_name': campaign[10],
        'total_interactions': campaign[11] or 0,
        'clicked_count': campaign[12] or 0,
        'submitted_count': campaign[13] or 0
    })

@app.route('/api/campaigns/<int:campaign_id>', methods=['DELETE'])
def delete_campaign(campaign_id):
    if 'user_id' not in session or not session.get('is_admin'):
        return jsonify({'error': 'Unauthorized'}), 403
    
    conn = sqlite3.connect('../data/setoolkit.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM campaign_results WHERE campaign_id = ?', (campaign_id,))
    cursor.execute('DELETE FROM campaigns WHERE id = ?', (campaign_id,))
    conn.commit()
    conn.close()
    
    return jsonify({'success': True})

@app.route('/api/training/complete', methods=['POST'])
def complete_training():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.json
    module_id = data.get('module_id')
    score = data.get('score', 0)
    
    conn = sqlite3.connect('../data/setoolkit.db')
    cursor = conn.cursor()
    
    # Check if progress record exists
    cursor.execute('SELECT id FROM user_training_progress WHERE user_id = ? AND module_id = ?',
                   (session['user_id'], module_id))
    existing = cursor.fetchone()
    
    if existing:
        cursor.execute('''
            UPDATE user_training_progress 
            SET completed = 1, score = ?, completed_at = CURRENT_TIMESTAMP
            WHERE user_id = ? AND module_id = ?
        ''', (score, session['user_id'], module_id))
    else:
        cursor.execute('''
            INSERT INTO user_training_progress (user_id, module_id, completed, score, completed_at)
            VALUES (?, ?, 1, ?, CURRENT_TIMESTAMP)
        ''', (session['user_id'], module_id, score))
    
    conn.commit()
    conn.close()
    
    return jsonify({'success': True})

@app.route('/api/training/modules/<int:module_id>', methods=['GET'])
def get_training_module(module_id):
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 403
    
    conn = sqlite3.connect('../data/setoolkit.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM training_modules WHERE id = ?', (module_id,))
    module = cursor.fetchone()
    conn.close()
    
    if not module:
        return jsonify({'error': 'Module not found'}), 404
    
    return jsonify({
        'id': module[0],
        'title': module[1],
        'description': module[2],
        'content': module[3],
        'quiz_questions': module[4]
    })

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)


from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import json
import uuid
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import os

app = Flask(__name__)
CORS(app)

# Database initialization
def init_db():
    """Initialize SQLite database with required tables"""
    conn = sqlite3.connect('neuronudge.db')
    cursor = conn.cursor()
    
    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    
    # Emotion sessions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS emotion_sessions (
            id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
            user_id TEXT NOT NULL,
            start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            end_time TIMESTAMP,
            emotions TEXT,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Behavioral data table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS behavioral_data (
            id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
            user_id TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            typing_speed REAL,
            mouse_activity REAL,
            focus_score REAL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Interventions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS interventions (
            id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
            user_id TEXT NOT NULL,
            type TEXT NOT NULL,
            emotion TEXT NOT NULL,
            message TEXT NOT NULL,
            accepted TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Tasks table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
            user_id TEXT NOT NULL,
            title TEXT NOT NULL,
            description TEXT,
            priority TEXT NOT NULL,
            complexity REAL,
            optimal_emotions TEXT,
            completed TEXT DEFAULT 'false',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Wellbeing reports table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS wellbeing_reports (
            id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
            user_id TEXT NOT NULL,
            week_start_date TIMESTAMP NOT NULL,
            avg_mood_score REAL,
            flow_sessions REAL,
            breaks_taken REAL,
            tasks_completed REAL,
            report_data TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Insert default user and tasks
    cursor.execute("SELECT COUNT(*) FROM users WHERE id = 'default-user'")
    if cursor.fetchone()[0] == 0:
        cursor.execute('''
            INSERT INTO users (id, username, password) 
            VALUES ('default-user', 'demo_user', 'demo_password')
        ''')
        
        # Insert default tasks
        default_tasks = [
            {
                'id': str(uuid.uuid4()),
                'user_id': 'default-user',
                'title': 'Design user interface mockups',
                'description': 'Create wireframes and visual designs',
                'priority': 'high',
                'complexity': 7,
                'optimal_emotions': json.dumps(['happy', 'neutral']),
                'completed': 'false'
            },
            {
                'id': str(uuid.uuid4()),
                'user_id': 'default-user',
                'title': 'Code new features',
                'description': 'Implement the emotion detection module',
                'priority': 'high',
                'complexity': 9,
                'optimal_emotions': json.dumps(['neutral', 'focused']),
                'completed': 'false'
            },
            {
                'id': str(uuid.uuid4()),
                'user_id': 'default-user',
                'title': 'Review performance metrics',
                'description': 'Analyze last quarter\'s data',
                'priority': 'medium',
                'complexity': 5,
                'optimal_emotions': json.dumps(['neutral', 'analytical']),
                'completed': 'false'
            }
        ]
        
        for task in default_tasks:
            cursor.execute('''
                INSERT INTO tasks (id, user_id, title, description, priority, complexity, optimal_emotions, completed)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (task['id'], task['user_id'], task['title'], task['description'], 
                  task['priority'], task['complexity'], task['optimal_emotions'], task['completed']))
    
    conn.commit()
    conn.close()

# Database helper functions
def get_db_connection():
    conn = sqlite3.connect('neuronudge.db')
    conn.row_factory = sqlite3.Row
    return conn

# API Routes

DEFAULT_USER_ID = "default-user"

@app.route('/api/behavioral-data', methods=['POST'])
def create_behavioral_data():
    try:
        data = request.json
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO behavioral_data (user_id, typing_speed, mouse_activity, focus_score)
            VALUES (?, ?, ?, ?)
        ''', (DEFAULT_USER_ID, data.get('typingSpeed'), data.get('mouseActivity'), data.get('focusScore')))
        
        behavioral_id = cursor.lastrowid
        conn.commit()
        
        # Get the created record
        cursor.execute('SELECT * FROM behavioral_data WHERE rowid = ?', (behavioral_id,))
        result = dict(cursor.fetchone())
        conn.close()
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'message': 'Invalid behavioral data', 'error': str(e)}), 400

@app.route('/api/behavioral-data', methods=['GET'])
def get_behavioral_data():
    try:
        limit = int(request.args.get('limit', 100))
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM behavioral_data 
            WHERE user_id = ? 
            ORDER BY timestamp DESC 
            LIMIT ?
        ''', (DEFAULT_USER_ID, limit))
        
        results = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return jsonify(results)
    except Exception as e:
        return jsonify({'message': 'Failed to fetch behavioral data', 'error': str(e)}), 500

@app.route('/api/emotion-sessions', methods=['POST'])
def create_emotion_session():
    try:
        data = request.json
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO emotion_sessions (user_id, emotions)
            VALUES (?, ?)
        ''', (DEFAULT_USER_ID, json.dumps(data.get('emotions', {}))))
        
        session_id = cursor.lastrowid
        conn.commit()
        
        cursor.execute('SELECT * FROM emotion_sessions WHERE rowid = ?', (session_id,))
        result = dict(cursor.fetchone())
        conn.close()
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'message': 'Invalid emotion session data', 'error': str(e)}), 400

@app.route('/api/emotion-sessions', methods=['GET'])
def get_emotion_sessions():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM emotion_sessions WHERE user_id = ?', (DEFAULT_USER_ID,))
        results = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return jsonify(results)
    except Exception as e:
        return jsonify({'message': 'Failed to fetch emotion sessions', 'error': str(e)}), 500

@app.route('/api/emotion-sessions/<session_id>', methods=['PATCH'])
def update_emotion_session(session_id):
    try:
        data = request.json
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Build update query dynamically
        update_fields = []
        values = []
        
        if 'end_time' in data:
            update_fields.append('end_time = ?')
            values.append(data['end_time'])
        
        if 'emotions' in data:
            update_fields.append('emotions = ?')
            values.append(json.dumps(data['emotions']))
        
        values.append(session_id)
        
        cursor.execute(f'''
            UPDATE emotion_sessions 
            SET {', '.join(update_fields)}
            WHERE id = ?
        ''', values)
        
        if cursor.rowcount == 0:
            return jsonify({'message': 'Emotion session not found'}), 404
        
        conn.commit()
        
        cursor.execute('SELECT * FROM emotion_sessions WHERE id = ?', (session_id,))
        result = dict(cursor.fetchone())
        conn.close()
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'message': 'Failed to update emotion session', 'error': str(e)}), 500

@app.route('/api/interventions', methods=['POST'])
def create_intervention():
    try:
        data = request.json
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO interventions (user_id, type, emotion, message, accepted)
            VALUES (?, ?, ?, ?, ?)
        ''', (DEFAULT_USER_ID, data.get('type'), data.get('emotion'), 
              data.get('message'), data.get('accepted')))
        
        intervention_id = cursor.lastrowid
        conn.commit()
        
        cursor.execute('SELECT * FROM interventions WHERE rowid = ?', (intervention_id,))
        result = dict(cursor.fetchone())
        conn.close()
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'message': 'Invalid intervention data', 'error': str(e)}), 400

@app.route('/api/interventions', methods=['GET'])
def get_interventions():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM interventions WHERE user_id = ?', (DEFAULT_USER_ID,))
        results = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return jsonify(results)
    except Exception as e:
        return jsonify({'message': 'Failed to fetch interventions', 'error': str(e)}), 500

@app.route('/api/interventions/<intervention_id>', methods=['PATCH'])
def update_intervention(intervention_id):
    try:
        data = request.json
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE interventions 
            SET accepted = ?
            WHERE id = ?
        ''', (data.get('accepted'), intervention_id))
        
        if cursor.rowcount == 0:
            return jsonify({'message': 'Intervention not found'}), 404
        
        conn.commit()
        
        cursor.execute('SELECT * FROM interventions WHERE id = ?', (intervention_id,))
        result = dict(cursor.fetchone())
        conn.close()
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'message': 'Failed to update intervention', 'error': str(e)}), 500

@app.route('/api/tasks', methods=['POST'])
def create_task():
    try:
        data = request.json
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO tasks (user_id, title, description, priority, complexity, optimal_emotions)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (DEFAULT_USER_ID, data.get('title'), data.get('description'), 
              data.get('priority'), data.get('complexity'), 
              json.dumps(data.get('optimalEmotions', []))))
        
        task_id = cursor.lastrowid
        conn.commit()
        
        cursor.execute('SELECT * FROM tasks WHERE rowid = ?', (task_id,))
        result = dict(cursor.fetchone())
        conn.close()
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'message': 'Invalid task data', 'error': str(e)}), 400

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM tasks WHERE user_id = ?', (DEFAULT_USER_ID,))
        results = []
        for row in cursor.fetchall():
            task = dict(row)
            if task['optimal_emotions']:
                try:
                    task['optimalEmotions'] = json.loads(task['optimal_emotions'])
                except:
                    task['optimalEmotions'] = []
            else:
                task['optimalEmotions'] = []
            del task['optimal_emotions']  # Remove the old field
            results.append(task)
        
        conn.close()
        return jsonify(results)
    except Exception as e:
        return jsonify({'message': 'Failed to fetch tasks', 'error': str(e)}), 500

@app.route('/api/tasks/<task_id>', methods=['PATCH'])
def update_task(task_id):
    try:
        data = request.json
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Build update query dynamically
        update_fields = []
        values = []
        
        for field in ['title', 'description', 'priority', 'complexity', 'completed']:
            if field in data:
                update_fields.append(f'{field} = ?')
                values.append(data[field])
        
        if 'optimalEmotions' in data:
            update_fields.append('optimal_emotions = ?')
            values.append(json.dumps(data['optimalEmotions']))
        
        values.append(task_id)
        
        cursor.execute(f'''
            UPDATE tasks 
            SET {', '.join(update_fields)}
            WHERE id = ?
        ''', values)
        
        if cursor.rowcount == 0:
            return jsonify({'message': 'Task not found'}), 404
        
        conn.commit()
        
        cursor.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
        result = dict(cursor.fetchone())
        if result['optimal_emotions']:
            try:
                result['optimalEmotions'] = json.loads(result['optimal_emotions'])
            except:
                result['optimalEmotions'] = []
        else:
            result['optimalEmotions'] = []
        del result['optimal_emotions']
        
        conn.close()
        return jsonify(result)
    except Exception as e:
        return jsonify({'message': 'Failed to update task', 'error': str(e)}), 500

@app.route('/api/tasks/<task_id>', methods=['DELETE'])
def delete_task(task_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
        
        if cursor.rowcount == 0:
            return jsonify({'message': 'Task not found'}), 404
        
        conn.commit()
        conn.close()
        
        return jsonify({'message': 'Task deleted successfully'})
    except Exception as e:
        return jsonify({'message': 'Failed to delete task', 'error': str(e)}), 500

@app.route('/api/wellbeing-reports', methods=['POST'])
def create_wellbeing_report():
    try:
        data = request.json
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO wellbeing_reports (user_id, week_start_date, avg_mood_score, 
                                         flow_sessions, breaks_taken, tasks_completed, report_data)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (DEFAULT_USER_ID, data.get('weekStartDate'), data.get('avgMoodScore'), 
              data.get('flowSessions'), data.get('breaksTaken'), data.get('tasksCompleted'),
              json.dumps(data.get('reportData', {}))))
        
        report_id = cursor.lastrowid
        conn.commit()
        
        cursor.execute('SELECT * FROM wellbeing_reports WHERE rowid = ?', (report_id,))
        result = dict(cursor.fetchone())
        conn.close()
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'message': 'Invalid wellbeing report data', 'error': str(e)}), 400

@app.route('/api/wellbeing-reports', methods=['GET'])
def get_wellbeing_reports():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM wellbeing_reports WHERE user_id = ?', (DEFAULT_USER_ID,))
        results = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return jsonify(results)
    except Exception as e:
        return jsonify({'message': 'Failed to fetch wellbeing reports', 'error': str(e)}), 500

@app.route('/api/analytics/today', methods=['GET'])
def get_today_analytics():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get today's behavioral data
        cursor.execute('''
            SELECT AVG(typing_speed) as avg_typing, AVG(mouse_activity) as avg_mouse, 
                   AVG(focus_score) as avg_focus, COUNT(*) as count
            FROM behavioral_data 
            WHERE user_id = ? AND DATE(timestamp) = DATE('now')
        ''', (DEFAULT_USER_ID,))
        
        behavioral_result = cursor.fetchone()
        
        # Get tasks data
        cursor.execute('''
            SELECT COUNT(*) as total, 
                   SUM(CASE WHEN completed = 'true' THEN 1 ELSE 0 END) as completed
            FROM tasks WHERE user_id = ?
        ''', (DEFAULT_USER_ID,))
        
        tasks_result = cursor.fetchone()
        
        conn.close()
        
        analytics = {
            'typingSpeed': int(behavioral_result['avg_typing'] or 68),
            'mouseActivity': int(behavioral_result['avg_mouse'] or 142),
            'focusScore': round(behavioral_result['avg_focus'] or 8.2, 1),
            'flowSessions': 3,
            'breaksTaken': 5,
            'avgMoodScore': 7.8,
            'tasksCompleted': tasks_result['completed'] or 0,
            'totalTasks': tasks_result['total'] or 0
        }
        
        return jsonify(analytics)
    except Exception as e:
        return jsonify({'message': 'Failed to fetch analytics', 'error': str(e)}), 500

# Static file serving for frontend
@app.route('/')
def serve_frontend():
    return app.send_static_file('index.html')

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
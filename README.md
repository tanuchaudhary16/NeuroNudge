# NeuroNudge Python Backend

This is the Python Flask backend for the NeuroNudge emotion-aware productivity application.

## Features

- **Flask REST API** - Complete RESTful endpoints for all functionality
- **SQLite Database** - Local database storage with automatic initialization
- **CORS Support** - Cross-origin requests enabled for frontend integration
- **Emotion Tracking** - Store and retrieve emotion detection data
- **Behavioral Analytics** - Track typing speed, mouse activity, and focus scores
- **Task Management** - AI-optimized task handling based on emotional states
- **Intervention System** - Smart suggestions and mood-based interventions

## Quick Start

1. **Install Python Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Application**
   ```bash
   python run.py
   ```

3. **Access the API**
   - Server runs on `http://localhost:5000`
   - Database auto-initializes on first run
   - Default demo user and tasks are created automatically

## API Endpoints

### Behavioral Data
- `POST /api/behavioral-data` - Record behavioral metrics
- `GET /api/behavioral-data` - Retrieve behavioral history

### Emotion Sessions  
- `POST /api/emotion-sessions` - Create emotion tracking session
- `GET /api/emotion-sessions` - Get emotion history
- `PATCH /api/emotion-sessions/<id>` - Update emotion session

### Tasks
- `GET /api/tasks` - Get all tasks
- `POST /api/tasks` - Create new task
- `PATCH /api/tasks/<id>` - Update task
- `DELETE /api/tasks/<id>` - Delete task

### Interventions
- `GET /api/interventions` - Get intervention history
- `POST /api/interventions` - Record intervention
- `PATCH /api/interventions/<id>` - Update intervention response

### Analytics
- `GET /api/analytics/today` - Get today's productivity analytics

### Wellbeing Reports
- `GET /api/wellbeing-reports` - Get wellbeing reports
- `POST /api/wellbeing-reports` - Create wellbeing report

## Database

Uses SQLite with the following tables:
- `users` - User accounts
- `emotion_sessions` - Emotion detection history  
- `behavioral_data` - Typing/mouse activity metrics
- `interventions` - AI suggestions and responses
- `tasks` - Task management with emotion optimization
- `wellbeing_reports` - Weekly wellness summaries

## Integration

This Python backend is designed to work with the React frontend. The frontend should be configured to make requests to `http://localhost:5000/api/` for all backend operations.
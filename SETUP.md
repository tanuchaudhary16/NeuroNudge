# NeuroNudge - Python Backend Setup

Welcome to **NeuroNudge**, an emotion-aware AI productivity assistant with webcam emotion detection!

## Quick Start

### Prerequisites
- **Python 3.7+** (with pip)
- **Node.js 18+** (with npm) 
- **Modern web browser** with webcam access

### Installation & Running

1. **Extract the files** and navigate to the directory:
   ```bash
   cd neuronudge-python/
   ```

2. **Install all dependencies** and start both services:
   ```bash
   npm run start
   ```

   This will:
   - Install Python dependencies (`pip install -r requirements.txt`)
   - Install Node.js dependencies (`npm install`) 
   - Start the Python Flask backend (port 5000)
   - Start the React frontend (port 5173)

3. **Open your browser** to `http://localhost:5173`

### Manual Setup (Alternative)

If the automatic setup doesn't work:

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Install Node.js dependencies:**
   ```bash
   npm install
   ```

3. **Start backend (Terminal 1):**
   ```bash
   python3 run.py
   ```

4. **Start frontend (Terminal 2):**
   ```bash
   npm run dev
   ```

## Features

🧠 **Real-time Emotion Detection** - Uses webcam and face-api.js
📊 **Behavioral Analytics** - Tracks typing speed, mouse activity, focus
💡 **Smart Interventions** - AI suggestions based on your emotional state  
📝 **Adaptive Task Management** - Reorders tasks to match your mood
🎨 **Beautiful UI** - Dynamic colors that adapt to your emotions
🌙 **Ambient Controls** - Environment optimization for productivity

## Architecture

- **Frontend**: React + TypeScript + Tailwind CSS (Port 5173)
- **Backend**: Python Flask + SQLite (Port 5000)
- **Database**: SQLite (`neuronudge.db` auto-created)
- **Models**: Face-api.js for emotion detection

## API Endpoints

The Python backend provides REST API endpoints:
- `/api/behavioral-data` - Behavioral metrics
- `/api/emotion-sessions` - Emotion tracking
- `/api/tasks` - Task management
- `/api/interventions` - AI interventions
- `/api/analytics/today` - Daily analytics

## Troubleshooting

**Webcam not working?**
- Grant camera permissions when prompted
- Check browser console for errors
- Try refreshing the page

**Backend connection issues?**
- Ensure Python Flask server is running on port 5000
- Check `python3 run.py` output for errors

**Dependencies not installing?**
- Update pip: `pip install --upgrade pip`
- Update npm: `npm install -g npm@latest`

Enjoy using NeuroNudge! 🚀
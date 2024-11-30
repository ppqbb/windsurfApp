# Job Portal System

A LinkedIn-like job portal system built with Django and React.

## Project Structure
```
midyaf/
├── backend/           # Django backend
├── frontend/          # React frontend for job seekers
└── admin-panel/      # React admin panel for companies
```

## Setup Instructions

### Backend Setup
1. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run migrations:
```bash
python manage.py migrate
```

4. Start the server:
```bash
python manage.py runserver
```

### Frontend Setup (Job Seekers Portal)
1. Install dependencies:
```bash
cd frontend
npm install
```

2. Start development server:
```bash
npm start
```

### Admin Panel Setup
1. Install dependencies:
```bash
cd admin-panel
npm install
```

2. Start development server:
```bash
npm start
```
"# windsurfApp" 

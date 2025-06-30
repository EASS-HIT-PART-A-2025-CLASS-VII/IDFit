## 🚀 IDFit - Your Way to the Army BEGIN

![logo](https://github.com/user-attachments/assets/d4cb7426-6704-4372-b2dd-11922b5b7394)

## 🌟 About IDFit
IDFit is an AI-powered system that analyzes personal traits and qualifications to recommend the most suitable military roles in the IDF.  
It uses natural language processing and structured role data to match users with optimal positions based on skills, personality, and physical profile.

## 🎥 Project Presentaion

https://www.youtube.com/watch?v=W519Fs55UTI&ab_channel=YuvalBenzaquen

## 🏗️ Architecture

![ארכיטקטורה](https://raw.githubusercontent.com/EASS-HIT-PART-A-2025-CLASS-VII/IDFit/main/frontend/public/architecture.png)


### 🔙 Backend
- FastAPI (Python)
- MongoDB
- Resend API (Emails)
- OpenRouter API (LLM - LLaMA 3)

### 🎨 Frontend
- React + Vite + TypeScript
- TailwindCSS

### 🐳 DevOps
- Docker
- Docker Compose

## 📁 Project Structure

```plaintext
IDFit/
├── Backend/                        # FastAPI backend
│   ├── app/
│   │   ├── config.py              # App configuration
│   │   ├── database.py            # MongoDB connection logic
│   │   ├── db_instance.py         # DB client instance
│   │   ├── email.py               # Email sending logic (Resend)
│   │   ├── main.py                # FastAPI app entry point
│   │   ├── repositories.py        # Business/data access logic
│   │   ├── schemas.py             # Pydantic schemas
│   │   ├── services.py            # Role recommendation logic
│   │   ├── translations.py        # Trait translation handler (with fallback)
│   │   └── unit_tests.py          # Backend tests
│   ├── tests/
│   │   └── mongo_test.py          # MongoDB-related test
│   ├── roles.json                 # Role database (IDF positions)
│   ├── Dockerfile                 # Backend container config
│   ├── requirements.txt           # Python dependencies
│   ├── pytest.ini                 # Pytest config
│   └── conftest.py                # Test fixtures and setup
│
├── frontend/                      # React + Vite frontend (TypeScript + TailwindCSS)
│   ├── public/                    # Static assets (images, video)
│   ├── src/
│   │   ├── assets/                # Icons and images
│   │   ├── hooks/                 # Custom React hooks
│   │   ├── App.tsx               # Root app structure
│   │   ├── index.css              # Global styles
│   │   ├── index.tsx              # React entry point
│   │   ├── main.tsx               # Main render logic
│   │   ├── Welcome.tsx           # Welcome screen
│   │   └── SidebarIcons.tsx      # Sidebar icon component
│   ├── index.html                 # HTML entry template
│   ├── tailwind.config.js        # Tailwind CSS config
│   ├── vite.config.ts            # Vite config file
│   ├── package.json              # Project dependencies
│   ├── tsconfig.json             # TypeScript config
│   └── Dockerfile                # Frontend container config
│
├── scripts/                       # Auxiliary scripts
└── docker-compose.yml            # Orchestration for backend, frontend, and MongoDB
```

## 🚀 Getting Started

### Prerequisites
- Docker & Docker Compose installed
- Python 3.10+ (if running locally)
- Node.js 18+ (if running frontend locally without Docker)


### Clone the repo
```plaintext
git clone https://github.com/EASS-HIT-PART-A-2025-CLASS-VII/IDFit
cd IDFit
```

### 🔑 Environment Variables
```plaintext
MONGODB_URL=mongodb://localhost:27017
DB_NAME=my_database
OPENROUTER_API_KEY=secret-key
RESEND_API_KEY=secret-key
```

### Run with Docker Compose
```plaintext
docker compose up --build
Backend will be available at: http://localhost:8000
Frontend will be available at: http://localhost:3000
```

## ⚙️ Run Manually
### Backend
```plaintext
cd Backend
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r Backend/app/requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Frontend
```plaintext
cd frontend
npm install
npm run build
npm install -g serve
serve -s dist -l 3000
```
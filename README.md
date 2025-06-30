## 🚀 IDFit - Your Way to the Army BEGIN

![logo](https://github.com/user-attachments/assets/d4cb7426-6704-4372-b2dd-11922b5b7394)

## 🌟 About Task It
IDFit is an AI-powered system that analyzes personal traits and qualifications to recommend the most suitable military roles in the IDF.  
It uses natural language processing and structured role data to match users with optimal positions based on skills, personality, and physical profile.

## 🎥 Project Presentaion

https://www.youtube.com/watch?v=nmV89fs3zts&ab_channel=YuvalBenzaquen

## 🏗️ Architecture

![ארכיטקטורה](https://github.com/user-attachments/assets/1c03ddc8-e47b-4d55-ac7d-1c116464743d)

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

IDFit/
├── Backend/                        # FastAPI backend
│   ├── app/
│   │   ├── config.py              # App configuration
│   │   ├── database.py            # MongoDB connection logic
│   │   ├── db_instance.py         # DB client instance
│   │   ├── email.py               # Email sending logic (e.g., Resend)
│   │   ├── main.py                # FastAPI app entry point
│   │   ├── repositories.py        # Business/data access logic
│   │   ├── schemas.py             # Pydantic schemas
│   │   ├── services.py            # Role recommendation logic
│   │   └── translations.py        # Trait translation handler (with fallback)
│   ├── tests/
│   │   └── mongo_test.py          # MongoDB-related test
│   ├── roles.json                 # Role database (IDF positions)
│   ├── Dockerfile                 # Backend container config
│   ├── requirements.txt           # Python dependencies
│   ├── pytest.ini                 # Pytest config
│   └── conftest.py                # Test fixtures and setup
│
├── frontend/                      # React + Vite frontend (TypeScript + TailwindCSS)
│   ├── node_modules/              # Node dependencies
│   ├── public/                    # Static assets
│   ├── src/
│   │   ├── assets/                # Icons and images
│   │   ├── hooks/                 # Custom React hooks
│   │   ├── App.tsx               # Root app structure
│   │   ├── index.css              # Global styles
│   │   ├── index.tsx             # React entry point
│   │   ├── main.tsx              # Main render logic
│   │   ├── Welcome.tsx           # Welcome screen
│   │   └── SidebarIcons.jsx      # Sidebar icon component
│   ├── index.html                 # HTML entry template
│   ├── tailwind.config.js        # Tailwind CSS config
│   ├── vite.config.ts            # Vite config file
│   ├── package.json              # Project dependencies
│   ├── tsconfig.json             # TypeScript config
│   └── Dockerfile                # Frontend container config
│
└── docker-compose.yml            # Orchestration for backend, frontend, and MongoDB

## 🚀 Getting Started

### Prerequisites
- Docker & Docker Compose installed
- Python 3.10+ (if running locally)

### Clone the repo
```bash
git clone https://github.com/EASS-HIT-PART-A-2025-CLASS-VII/IDFit
cd IDFit

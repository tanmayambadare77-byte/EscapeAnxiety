# Escape Anxiety — Backend (FastAPI + scikit-learn)

This repository contains a backend implementation for the "Escape Anxiety" mobile app using:
- FastAPI (REST API)
- SQLAlchemy (ORM; works with SQLite or MySQL)
- scikit-learn (simple mood prediction model)
- JWT authentication

Features:
- User registration, login (JWT), profiles
- Stress-relief activities, motivational content, simple games endpoints
- Progress tracking (activity completions, mood entries)
- Mood prediction API endpoint (trained scikit-learn model)
- Configurable DATABASE_URL via environment variable

Quickstart (local / development)
1. Create virtualenv and install dependencies:
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt

2. Copy .env.example to .env and edit if needed:
   SECRET_KEY (random), DATABASE_URL (default sqlite:///./escape_anxiety.db), JWT_EXPIRATION_MINUTES.

3. Start server:
   uvicorn app.main:app --reload

4. Create DB tables (first run):
   from a Python shell:
   >>> from app.database import Base, engine
   >>> Base.metadata.create_all(bind=engine)

   Or the app will create them automatically at startup if configured.

5. Train the ML model:
   python -m app.ml.train_model
   (This script trains a mood model from DB mood entries or sample data and writes a model file app/ml/mood_model.pkl)

6. Swagger UI:
   Visit http://127.0.0.1:8000/docs

Notes:
- Database: the default is SQLite for convenience. To use MySQL, set DATABASE_URL in .env (example for MySQL):
  mysql+pymysql://user:password@host:3306/dbname

- Training the mood model requires mood-labeled text entries. The training script uses sample data if DB has no entries.

- Replace SECRET_KEY with a secure random string in production.

File overview:
- app/main.py - FastAPI app, include routers
- app/config.py - config via pydantic settings
- app/database.py - SQLAlchemy engine & session
- app/models.py - ORM models
- app/schemas.py - Pydantic schemas
- app/auth.py - password hashing and JWT token utilities
- app/crud.py - DB operations
- app/routers/* - router modules: users, activities, content, games, ml
- app/ml/train_model.py - script to train the mood model
- app/ml/mood_model.py - inference & helper functions
- requirements.txt - required packages
- .env.example - environment variables example

If you want, I can:
- Add Alembic migrations
- Make async endpoints using async SQLAlchemy/Databases
- Add background tasks for training or periodic data collection
- Add unit tests / CI config

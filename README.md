# Mental Health Text Classifier Web App
A simple Streamlit web application that classifies mental health related text using machine learning.

## Features
- Classify text using a machine learning model
- View history of previous classifications
- User-friendly interface

## Notes
┌──────────────────┐      HTTPS/JSON      ┌───────────────────────┐
│  React + TS FE   │ ◀──────────────────▶│  Python inference API │
│  (Vite / Vercel) │                      │  (FastAPI + Uvicorn)  │
└──────────────────┘                      └────────┬──────────────┘
                                                 Docker
                                                   │
                                        Cloud Run / Render / Railway

# Katsina NYSC Married Corps Members Zonal Tracking System

A full-stack backend application built with Flask, SQLAlchemy, Pandas, and ReportLab designed for tracking married corps members across the four operational zones in Katsina State (Katsina, Daura, Dutsinma, and Funtua) and exporting official PDF posting schedules.

## Local Development & Setup

1. **Install Python 3.9+**
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the application:**
   ```bash
   python app.py
   ```

## Deployment on Render

1. Create a new **Web Service** on [Render](https://render.com/).
2. Connect your GitHub repository containing these files.
3. Render will automatically detect `render.yaml` or use:
   - **Environment:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
4. Attach a **PostgreSQL Database** on Render and link its connection string to the `DATABASE_URL` environment variable.

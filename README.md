# 🚛 ELD Trip Planner

## 🎬 Demo Video
[Watch Demo on Loom](https://www.loom.com/share/784f953813a347998f0c0069d1eef517)

## Live Demo
- **App:** [https://eld-trip-planner-brown.vercel.app/](https://eld-trip-planner-brown.vercel.app/)
- **API:** [https://eld-trip-planner-mx8r.onrender.com/api/health/](https://eld-trip-planner-mx8r.onrender.com/api/health/)

## About
A full-stack HOS (Hours of Service) compliant trip planning app for truck drivers.
Takes trip details as input and generates route instructions and ELD daily log sheets.

## Features
- Interactive map with route visualization (Leaflet + OpenStreetMap)
- HOS compliant trip planning (70hrs/8days, property-carrying driver)
- Automatic rest breaks (30min after 8hrs driving, 10hr daily reset)
- Fuel stops every 1,000 miles
- ELD Daily Log Sheets drawn on canvas
- 1 hour for pickup and dropoff

## Tech Stack
**Frontend:** React, Vite, Leaflet.js, OpenStreetMap  
**Backend:** Django, Django REST Framework, PostgreSQL  
**Routing:** OSRM (Open Source Routing Machine)  
**Geocoding:** Nominatim  
**Hosting:** Vercel (frontend) + Render.com (backend)

## Local Setup

### Backend
1. `cd backend`
2. `python -m venv venv`
3. `source venv/bin/activate`  # On Windows use `venv\Scripts\activate`
4. `pip install -r requirements.txt`
5. `python manage.py migrate`
6. `python manage.py runserver`

### Frontend
1. `cd frontend`
2. `npm install`
3. `npm run dev`

## API Endpoints
- **POST /api/trips/** — Create trip and calculate route + ELD logs
- **GET /api/trips/{id}/** — Get trip details
- **GET /api/health/** — Health check

## HOS Rules Implemented
- 11 hours max driving per day
- 14 hour on-duty window
- 30 min break after 8 hours continuous driving
- 10 hour rest between shifts
- 70 hours / 8 days cycle limit
- 34 hour restart

## Health Check Response Example

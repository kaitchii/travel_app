# Travel App 🌍

A mobile travel recommendation application built with Flet (Python cross-platform UI) and FastAPI backend.

## Features

- **User Authentication** - Login system with user_travel database
- **Travel Recommendations** - Browse travel destinations by category
- **Transportation Options** - View and compare transportation methods with costs and time
- **Search & Filter** - Search places and filter by travel style (nature, beach, temple, cafe, culture, city)
- **Budget Planning** - Calculate total travel costs including accommodation and transportation
- **Rating System** - View place ratings and detailed information

## Tech Stack

**Frontend:**
- Flet (Python cross-platform mobile UI)
- iPhone ratio locked (390×844)
- Real-time API integration

**Backend:**
- FastAPI (Python REST API)
- MariaDB database
- CORS enabled for cross-origin requests

**Database:**
- Tables: user_travel, rec_travel, transportation, budget, style_travel

## Project Structure

```
travelapp_api/
├── travel_app.py       # FastAPI backend server
├── mobile_app.py       # Flet mobile frontend
├── env/               # Python virtual environment
├── .gitignore
└── README.md
```

## Setup Instructions

### Prerequisites
- Python 3.8+
- MariaDB running on 192.168.100.40
- Network access to database server

### Backend Setup

1. Create virtual environment:
```bash
python -m venv env
```

2. Activate environment:
```bash
# Windows PowerShell
.\env\Scripts\Activate.ps1
# macOS/Linux
source env/bin/activate
```

3. Install dependencies:
```bash
pip install fastapi uvicorn pymysql pydantic python-dotenv pyyaml
```

4. Configure database in `travel_app.py`:
```python
DB_HOST = "192.168.100.40"
DB_USER = "root"
DB_PASSWORD = "P@ssw0rd"
DB_NAME = "travel"
```

5. Run the server:
```bash
python -m uvicorn travel_app:app --host 0.0.0.0 --port 3500 --reload
```

### Frontend Setup

1. Install Flet:
```bash
pip install flet
```

2. Update `API_BASE_URL` in `mobile_app.py`:
```python
API_BASE_URL = "http://192.168.100.40:3500"
```

3. Run the mobile app:
```bash
flet run mobile_app.py
```

## API Endpoints

- `POST /login` - User authentication
- `GET /styles` - Fetch travel style categories
- `GET /places` - Fetch all places
- `GET /places?style_id={id}` - Filter places by style
- `GET /travel-cost/{place_id}` - Get travel cost details
- `GET /transportation-options/{place_id}` - Get transportation options

## Database Schema

**user_travel**: user_id, username, password
**rec_travel**: place_id, place_name, place_descript, place_image, rating, openning_hr, style_id
**transportation**: tran_id, tran_name, tran_cost, tran_time, place_id
**budget**: budget_id, min_budget, max_budget, place_id
**style_travel**: style_id, style_name

## Default Credentials

```
Username: nil      Password: 1234
Username: pui      Password: eiei
Username: aus      Password: hahaha
Username: kait     Password: password
```

## Mobile View

The app is optimized for iPhone SE 2020 (390×844) and includes:
- Centered login page with form validation
- Category-based place browsing
- Detailed place information with transportation costs
- Real-time search and filtering

## Deployment

### iPhone Access
Open Safari on your iPhone and navigate to:
```
http://[DEV_MACHINE_IP]:3500
```

To find your development machine IP, run:
```bash
ipconfig
```

## Development Notes

- Window is locked to phone aspect ratio (390×844) for testing
- uvicorn with `--reload` for hot-reloading during development
- All API responses include JSON with proper error handling
- Whitespace handling in authentication (TRIM in SQL, strip() in Python)

## Color Scheme

- Primary: #FF5F3D (Orange)
- Dark text: #1a1a1a
- Light background: #f5f5f5
- Category colors mapped by style

## Future Enhancements

- User profile management
- Save favorite places
- Real payment integration
- Push notifications
- Offline mode support
- Multi-language support

## License

This project is open source and available under the MIT License.

---

**Author:** Travel App Development Team  
**Last Updated:** March 2026

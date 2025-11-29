# AirIQ PMS5003 Air Quality Monitor

A real-time web dashboard for monitoring PMS5003 particulate matter sensor data.

## Features

- **Real-time Dashboard**: Live metrics for PM1.0, PM2.5, and PM10
- **Interactive Chart**: 24-hour historical data visualization with Chart.js
- **Clean UI**: Professional blue sidebar with responsive design
- **Auto-refresh**: Updates every 5 seconds with smooth animations
- **Sensor Data Logging**: Console output of sensor readings

## Project Structure

```
.
├── run_server.py          # HTTP server (runs on port 8000)
├── templates/
│   └── index.html         # Dashboard UI
├── logo/
│   └── logo.jpg           # AirIQ logo
├── pms5003_reader.py      # PMS5003 sensor reader
├── pms5003_test.py        # Sensor tests
└── README.md              # This file
```

## Setup & Installation

### Requirements

- Python 3.6+
- No external dependencies (uses built-in libraries only)

### Running the Dashboard

```bash
# Navigate to project directory
cd /home/prabinpie/Desktop/SeniorDesign

# Start the server
python3 run_server.py 8000

# Open browser
# http://localhost:8000
```

### API Endpoints

- `GET /` - Dashboard UI
- `GET /api/data` - Current sensor readings (JSON)
- `GET /api/history` - 24-hour historical data (JSON)

## Current Data Format

```json
{
  "pm1": 3.2,
  "pm25": 12.4,
  "pm10": 18.7,
  "timestamp": "2025-11-28 17:45:51"
}
```

## Integration with Real Sensor

To use real PMS5003 data:

1. Update the `/api/history` endpoint in `run_server.py` to read from `pms5003_reader.py`
2. Replace mock data generation with actual sensor readings
3. Store historical data (database or file)

## Troubleshooting

### Server won't start
```bash
# Kill any process on port 8000
lsof -i :8000 | grep -v COMMAND | awk '{print $2}' | xargs kill -9

# Try again
python3 run_server.py 8000
```

### Dashboard not updating
- Check browser console for errors (F12)
- Verify `/logo/logo.jpg` exists
- Ensure server is running (`http://localhost:8000`)

## Default Mock Data

The server currently uses mock sensor data with realistic ranges:
- PM1.0: 2.5 ± 0.5 µg/m³
- PM2.5: 10 ± 2.5 µg/m³  
- PM10: 16 ± 4 µg/m³

## License

Senior Design Project - AirIQ Team

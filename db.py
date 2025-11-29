"""SQLite database for AirIQ sensor readings"""
import sqlite3
import os
from datetime import datetime, timedelta

DB_PATH = os.path.join(os.path.dirname(__file__), 'airiq.db')

def init_db():
    """Initialize database with readings table"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS readings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            pm1 REAL,
            pm25 REAL,
            pm10 REAL
        )
    ''')
    conn.commit()
    conn.close()

def insert_reading(pm1, pm25, pm10):
    """Insert a new sensor reading"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('INSERT INTO readings (timestamp, pm1, pm25, pm10) VALUES (?, ?, ?, ?)',
              (datetime.now(), pm1, pm25, pm10))
    conn.commit()
    conn.close()

def get_latest_reading():
    """Get the most recent sensor reading"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT pm1, pm25, pm10, timestamp FROM readings ORDER BY timestamp DESC LIMIT 1')
    row = c.fetchone()
    conn.close()
    if row:
        return {'pm1': row[0], 'pm25': row[1], 'pm10': row[2], 'timestamp': row[3]}
    return None

def get_history_24h():
    """Get last 24 hours of readings with all data points"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Get all data from last 24 hours
    c.execute('''
        SELECT 
            strftime('%H:%M', timestamp) as time,
            pm25,
            pm10
        FROM readings
        WHERE timestamp > datetime('now', '-24 hours')
        ORDER BY timestamp
    ''')
    
    rows = c.fetchall()
    conn.close()
    
    history = [{'time': row[0], 'pm25': row[1], 'pm10': row[2]} for row in rows]
    
    # If no data, return placeholder with current time
    if not history:
        now = datetime.now()
        history = [{'time': (now - timedelta(hours=i)).strftime('%H:%M'), 'pm25': 0, 'pm10': 0} 
                   for i in range(24)][::-1]
    
    return history

def get_all_records():
    """Get all sensor readings from database"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT timestamp, pm1, pm25, pm10 FROM readings ORDER BY timestamp DESC')
    rows = c.fetchall()
    conn.close()
    
    records = [{'timestamp': row[0], 'pm1': row[1], 'pm25': row[2], 'pm10': row[3]} 
               for row in rows]
    return records

def clear_old_data(days=30):
    """Remove readings older than specified days"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('DELETE FROM readings WHERE timestamp < datetime("now", "-" || ? || " days")',
              (days,))
    conn.commit()
    conn.close()

# Initialize on import
init_db()

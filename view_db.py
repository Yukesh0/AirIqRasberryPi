#!/usr/bin/env python3
"""View AirIQ database contents"""
import sqlite3
import sys

DB_PATH = 'airiq.db'

def view_latest(limit=20):
    """View latest readings"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT id, timestamp, pm1, pm25, pm10 FROM readings ORDER BY timestamp DESC LIMIT ?', (limit,))
    rows = c.fetchall()
    conn.close()
    
    if not rows:
        print("No data in database")
        return
    
    print(f"\n{'ID':<5} {'TIMESTAMP':<20} {'PM1':<8} {'PM2.5':<8} {'PM10':<8}")
    print("-" * 60)
    for row in rows:
        print(f"{row[0]:<5} {row[1]:<20} {row[2]:<8.2f} {row[3]:<8.2f} {row[4]:<8.2f}")
    print()

def stats():
    """Show database statistics"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute('SELECT COUNT(*) FROM readings')
    count = c.fetchone()[0]
    
    c.execute('SELECT AVG(pm25), MIN(pm25), MAX(pm25) FROM readings')
    avg_pm25, min_pm25, max_pm25 = c.fetchone()
    
    c.execute('SELECT AVG(pm10), MIN(pm10), MAX(pm10) FROM readings')
    avg_pm10, min_pm10, max_pm10 = c.fetchone()
    
    conn.close()
    
    print("\n=== Database Statistics ===")
    print(f"Total readings: {count}")
    print(f"\nPM2.5:")
    print(f"  Average: {avg_pm25:.2f} µg/m³")
    print(f"  Min: {min_pm25:.2f} µg/m³")
    print(f"  Max: {max_pm25:.2f} µg/m³")
    print(f"\nPM10:")
    print(f"  Average: {avg_pm10:.2f} µg/m³")
    print(f"  Min: {min_pm10:.2f} µg/m³")
    print(f"  Max: {max_pm10:.2f} µg/m³")
    print()

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'stats':
        stats()
    else:
        limit = int(sys.argv[1]) if len(sys.argv) > 1 else 20
        view_latest(limit)

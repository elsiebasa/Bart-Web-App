import sqlite3
from datetime import datetime
import os

class BartDatabase:
    def __init__(self, db_path='data/bart.db'):
        # Create data directory if it doesn't exist
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        self.conn = sqlite3.connect(db_path)
        self.create_tables()
    
    def create_tables(self):
        cursor = self.conn.cursor()
        
        # Create stations table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS stations (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            abbr TEXT NOT NULL,
            city TEXT,
            county TEXT,
            state TEXT,
            zipcode TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # Create departures table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS departures (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            station_id TEXT NOT NULL,
            destination TEXT NOT NULL,
            platform TEXT,
            minutes INTEGER NOT NULL,
            direction TEXT NOT NULL,
            color TEXT,
            length INTEGER,
            bike_flag INTEGER,
            delay INTEGER DEFAULT 0,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            date DATE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (station_id) REFERENCES stations(id)
        )
        ''')
        
        # Create daily_stats table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS daily_stats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            station_id TEXT NOT NULL,
            date DATE NOT NULL,
            total_departures INTEGER DEFAULT 0,
            delayed_departures INTEGER DEFAULT 0,
            avg_delay_minutes REAL DEFAULT 0,
            max_delay_minutes INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (station_id) REFERENCES stations(id)
        )
        ''')
        
        self.conn.commit()
    
    def save_station(self, station_data):
        cursor = self.conn.cursor()
        cursor.execute('''
        INSERT OR REPLACE INTO stations 
        (id, name, abbr, city, county, state, zipcode)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            station_data['id'],
            station_data['name'],
            station_data['abbr'],
            station_data.get('city'),
            station_data.get('county'),
            station_data.get('state'),
            station_data.get('zipcode')
        ))
        self.conn.commit()
    
    def save_departure(self, departure_data):
        cursor = self.conn.cursor()
        cursor.execute('''
        INSERT INTO departures 
        (station_id, destination, platform, minutes, direction, color, length, bike_flag, delay, date)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            departure_data['station_id'],
            departure_data['destination'],
            departure_data.get('platform'),
            departure_data['minutes'],
            departure_data['direction'],
            departure_data.get('color'),
            departure_data.get('length'),
            departure_data.get('bike_flag'),
            departure_data.get('delay', 0),
            datetime.now().strftime('%Y-%m-%d')
        ))
        self.conn.commit()
    
    def update_daily_stats(self, station_id, date):
        cursor = self.conn.cursor()
        
        # Calculate stats for the day
        cursor.execute('''
        SELECT 
            COUNT(*) as total,
            SUM(CASE WHEN minutes > 0 THEN 1 ELSE 0 END) as delayed,
            AVG(CASE WHEN minutes > 0 THEN minutes ELSE NULL END) as avg_delay,
            MAX(CASE WHEN minutes > 0 THEN minutes ELSE 0 END) as max_delay
        FROM departures
        WHERE station_id = ? AND date(created_at) = ?
        ''', (station_id, date))
        
        stats = cursor.fetchone()
        
        # Update or insert stats
        cursor.execute('''
        INSERT OR REPLACE INTO daily_stats 
        (station_id, date, total_departures, delayed_departures, avg_delay_minutes, max_delay_minutes)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            station_id,
            date,
            stats[0] or 0,
            stats[1] or 0,
            stats[2] or 0,
            stats[3] or 0
        ))
        
        self.conn.commit()
    
    def get_station_stats(self, station_id, days=7):
        cursor = self.conn.cursor()
        cursor.execute('''
        SELECT 
            date,
            total_departures,
            delayed_departures,
            avg_delay_minutes,
            max_delay_minutes
        FROM daily_stats
        WHERE station_id = ?
        ORDER BY date DESC
        LIMIT ?
        ''', (station_id, days))
        
        return cursor.fetchall()
    
    def close(self):
        self.conn.close() 
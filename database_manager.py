import sqlite3
import logging
from typing import List, Dict, Any, Optional
import json
from datetime import datetime

logger = logging.getLogger(__name__)

class DatabaseManager:
    """Enhanced database manager for tender processing system"""
    
    def __init__(self, db_path: str = "tender_bidders.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize database with required tables"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Create works table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS works (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nit_number TEXT NOT NULL,
                        work_name TEXT NOT NULL,
                        estimated_cost REAL NOT NULL,
                        schedule_amount REAL,
                        earnest_money REAL,
                        time_of_completion INTEGER,
                        ee_name TEXT,
                        tender_date TEXT,
                        created_at TEXT NOT NULL,
                        updated_at TEXT NOT NULL
                    )
                ''')
                
                # Create bidders table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS bidders (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        work_id INTEGER NOT NULL,
                        name TEXT NOT NULL,
                        percentage REAL NOT NULL,
                        bid_amount REAL NOT NULL,
                        contact TEXT,
                        is_lowest BOOLEAN DEFAULT 0,
                        created_at TEXT NOT NULL,
                        FOREIGN KEY (work_id) REFERENCES works (id)
                    )
                ''')
                
                # Create bidder_profiles table for credential storage
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS bidder_profiles (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL UNIQUE,
                        contact TEXT,
                        address TEXT,
                        registration_number TEXT,
                        category TEXT,
                        experience_years INTEGER,
                        last_used TEXT,
                        usage_count INTEGER DEFAULT 1
                    )
                ''')
                
                # Create indexes for better performance
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_works_nit ON works(nit_number)')
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_bidders_work_id ON bidders(work_id)')
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_bidders_name ON bidders(name)')
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_bidder_profiles_name ON bidder_profiles(name)')
                
                conn.commit()
                logger.info("Database initialized successfully")
                
        except Exception as e:
            logger.error(f"Error initializing database: {str(e)}")
            raise
    
    def save_work_data(self, work_data: Dict[str, Any]) -> Optional[int]:
        """Save work data with bidders to database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                current_time = datetime.now().isoformat()
                
                # Insert work data
                cursor.execute('''
                    INSERT INTO works (
                        nit_number, work_name, estimated_cost, schedule_amount,
                        earnest_money, time_of_completion, ee_name, tender_date,
                        created_at, updated_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    work_data.get('nit_number'),
                    work_data.get('work_name'),
                    work_data.get('estimated_cost'),
                    work_data.get('schedule_amount'),
                    work_data.get('earnest_money'),
                    work_data.get('time_of_completion'),
                    work_data.get('ee_name'),
                    work_data.get('date'),
                    current_time,
                    current_time
                ))
                
                work_id = cursor.lastrowid
                
                # Insert bidders
                bidders = work_data.get('bidders', [])
                lowest_bidder = work_data.get('lowest_bidder', {})
                
                for bidder in bidders:
                    is_lowest = (bidder.get('name') == lowest_bidder.get('name'))
                    
                    cursor.execute('''
                        INSERT INTO bidders (
                            work_id, name, percentage, bid_amount, contact, is_lowest, created_at
                        ) VALUES (?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        work_id,
                        bidder.get('name'),
                        bidder.get('percentage'),
                        bidder.get('bid_amount'),
                        bidder.get('contact'),
                        is_lowest,
                        current_time
                    ))
                    
                    # Update or insert bidder profile
                    self._update_bidder_profile(cursor, bidder, current_time)
                
                conn.commit()
                logger.info(f"Work data saved successfully with ID: {work_id}")
                return work_id
                
        except Exception as e:
            logger.error(f"Error saving work data: {str(e)}")
            return None
    
    def _update_bidder_profile(self, cursor, bidder: Dict[str, Any], current_time: str):
        """Update or insert bidder profile"""
        try:
            bidder_name = bidder.get('name', '').strip()
            if not bidder_name:
                return
            
            # Check if profile exists
            cursor.execute('SELECT id, usage_count FROM bidder_profiles WHERE name = ?', (bidder_name,))
            result = cursor.fetchone()
            
            if result:
                # Update existing profile
                profile_id, usage_count = result
                cursor.execute('''
                    UPDATE bidder_profiles 
                    SET contact = COALESCE(?, contact), last_used = ?, usage_count = ?
                    WHERE id = ?
                ''', (bidder.get('contact'), current_time, usage_count + 1, profile_id))
            else:
                # Insert new profile
                cursor.execute('''
                    INSERT INTO bidder_profiles (name, contact, last_used, usage_count)
                    VALUES (?, ?, ?, 1)
                ''', (bidder_name, bidder.get('contact'), current_time))
                
        except Exception as e:
            logger.error(f"Error updating bidder profile: {str(e)}")
    
    def get_recent_bidders(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get recent bidders for auto-suggestion"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    SELECT name, contact, usage_count, last_used
                    FROM bidder_profiles
                    ORDER BY usage_count DESC, last_used DESC
                    LIMIT ?
                ''', (limit,))
                
                results = cursor.fetchall()
                
                bidders = []
                for result in results:
                    bidders.append({
                        'name': result[0],
                        'contact': result[1] or '',
                        'usage_count': result[2],
                        'last_used': result[3]
                    })
                
                return bidders
                
        except Exception as e:
            logger.error(f"Error fetching recent bidders: {str(e)}")
            return []
    
    def get_work_by_nit(self, nit_number: str) -> Optional[Dict[str, Any]]:
        """Get work data by NIT number"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Get work data
                cursor.execute('''
                    SELECT * FROM works WHERE nit_number = ?
                    ORDER BY created_at DESC LIMIT 1
                ''', (nit_number,))
                
                work_result = cursor.fetchone()
                if not work_result:
                    return None
                
                # Convert to dictionary
                work_columns = [desc[0] for desc in cursor.description]
                work_data = dict(zip(work_columns, work_result))
                
                # Get bidders
                cursor.execute('''
                    SELECT name, percentage, bid_amount, contact, is_lowest
                    FROM bidders WHERE work_id = ?
                    ORDER BY bid_amount ASC
                ''', (work_data['id'],))
                
                bidder_results = cursor.fetchall()
                bidders = []
                lowest_bidder = None
                
                for result in bidder_results:
                    bidder = {
                        'name': result[0],
                        'percentage': result[1],
                        'bid_amount': result[2],
                        'contact': result[3] or ''
                    }
                    bidders.append(bidder)
                    
                    if result[4]:  # is_lowest
                        lowest_bidder = bidder
                
                work_data['bidders'] = bidders
                work_data['lowest_bidder'] = lowest_bidder
                
                return work_data
                
        except Exception as e:
            logger.error(f"Error fetching work by NIT: {str(e)}")
            return None
    
    def get_all_works(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get all works with basic information"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    SELECT w.*, COUNT(b.id) as bidder_count
                    FROM works w
                    LEFT JOIN bidders b ON w.id = b.work_id
                    GROUP BY w.id
                    ORDER BY w.created_at DESC
                    LIMIT ?
                ''', (limit,))
                
                results = cursor.fetchall()
                columns = [desc[0] for desc in cursor.description]
                
                works = []
                for result in results:
                    work = dict(zip(columns, result))
                    works.append(work)
                
                return works
                
        except Exception as e:
            logger.error(f"Error fetching all works: {str(e)}")
            return []
    
    def get_bidder_statistics(self) -> Dict[str, Any]:
        """Get bidder statistics"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Total unique bidders
                cursor.execute('SELECT COUNT(DISTINCT name) FROM bidder_profiles')
                total_bidders = cursor.fetchone()[0]
                
                # Most frequent bidders
                cursor.execute('''
                    SELECT name, usage_count FROM bidder_profiles
                    ORDER BY usage_count DESC LIMIT 10
                ''')
                frequent_bidders = cursor.fetchall()
                
                # Recent activity
                cursor.execute('''
                    SELECT COUNT(*) FROM bidders 
                    WHERE created_at >= date('now', '-30 days')
                ''')
                recent_bids = cursor.fetchone()[0]
                
                return {
                    'total_unique_bidders': total_bidders,
                    'frequent_bidders': [{'name': name, 'count': count} for name, count in frequent_bidders],
                    'recent_bids_30_days': recent_bids
                }
                
        except Exception as e:
            logger.error(f"Error fetching bidder statistics: {str(e)}")
            return {}
    
    def delete_work(self, work_id: int) -> bool:
        """Delete work and associated bidders"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Delete bidders first
                cursor.execute('DELETE FROM bidders WHERE work_id = ?', (work_id,))
                
                # Delete work
                cursor.execute('DELETE FROM works WHERE id = ?', (work_id,))
                
                conn.commit()
                logger.info(f"Work {work_id} deleted successfully")
                return True
                
        except Exception as e:
            logger.error(f"Error deleting work {work_id}: {str(e)}")
            return False
    
    def update_work_data(self, work_id: int, work_data: Dict[str, Any]) -> bool:
        """Update existing work data"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                current_time = datetime.now().isoformat()
                
                # Update work data
                cursor.execute('''
                    UPDATE works SET
                        nit_number = ?, work_name = ?, estimated_cost = ?,
                        schedule_amount = ?, earnest_money = ?, time_of_completion = ?,
                        ee_name = ?, tender_date = ?, updated_at = ?
                    WHERE id = ?
                ''', (
                    work_data.get('nit_number'),
                    work_data.get('work_name'),
                    work_data.get('estimated_cost'),
                    work_data.get('schedule_amount'),
                    work_data.get('earnest_money'),
                    work_data.get('time_of_completion'),
                    work_data.get('ee_name'),
                    work_data.get('date'),
                    current_time,
                    work_id
                ))
                
                # Delete existing bidders
                cursor.execute('DELETE FROM bidders WHERE work_id = ?', (work_id,))
                
                # Insert updated bidders
                bidders = work_data.get('bidders', [])
                lowest_bidder = work_data.get('lowest_bidder', {})
                
                for bidder in bidders:
                    is_lowest = (bidder.get('name') == lowest_bidder.get('name'))
                    
                    cursor.execute('''
                        INSERT INTO bidders (
                            work_id, name, percentage, bid_amount, contact, is_lowest, created_at
                        ) VALUES (?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        work_id,
                        bidder.get('name'),
                        bidder.get('percentage'),
                        bidder.get('bid_amount'),
                        bidder.get('contact'),
                        is_lowest,
                        current_time
                    ))
                
                conn.commit()
                logger.info(f"Work {work_id} updated successfully")
                return True
                
        except Exception as e:
            logger.error(f"Error updating work {work_id}: {str(e)}")
            return False

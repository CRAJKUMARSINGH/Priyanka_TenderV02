import json
import os
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
from date_utils import DateUtils

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class BidderManager:
    """Enhanced bidder management with persistent storage and improved date handling."""
    
    def __init__(self, database_file: str = "bidder_database.json"):
        self.database_file = database_file
        self.date_utils = DateUtils()
        self.bidders_db = self._load_database()
    
    def _load_database(self) -> Dict[str, Any]:
        """Load bidder database from JSON file."""
        try:
            if os.path.exists(self.database_file):
                with open(self.database_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    logging.info(f"Loaded {len(data.get('bidders', []))} bidders from database")
                    return data
        except Exception as e:
            logging.error(f"Error loading database: {e}")
        
        # Return default structure if file doesn't exist or error occurred
        return {
            'bidders': [],
            'statistics': {
                'total_bidders': 0,
                'last_updated': self.date_utils.get_current_date()
            }
        }
    
    def _save_database(self) -> bool:
        """Save bidder database to JSON file."""
        try:
            # Update statistics
            self.bidders_db['statistics']['total_bidders'] = len(self.bidders_db['bidders'])
            self.bidders_db['statistics']['last_updated'] = self.date_utils.get_current_date()
            
            with open(self.database_file, 'w', encoding='utf-8') as f:
                json.dump(self.bidders_db, f, indent=2, ensure_ascii=False)
            
            logging.info(f"Saved database with {len(self.bidders_db['bidders'])} bidders")
            return True
            
        except Exception as e:
            logging.error(f"Error saving database: {e}")
            return False
    
    def add_bidder(self, bidder_data: Dict[str, Any]) -> bool:
        """
        Add new bidder to database.
        
        Args:
            bidder_data: Dictionary containing bidder information
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Validate required fields
            required_fields = ['name', 'percentage', 'bid_amount']
            for field in required_fields:
                if field not in bidder_data:
                    raise ValueError(f"Missing required field: {field}")
            
            # Enhance bidder data
            enhanced_data = bidder_data.copy()
            enhanced_data['id'] = self._generate_bidder_id()
            enhanced_data['date_added'] = self.date_utils.get_current_date()
            enhanced_data['last_updated'] = self.date_utils.get_current_date()
            
            # Normalize date format if date_added was provided
            if 'date_added' in bidder_data:
                parsed_date = self.date_utils.parse_date(bidder_data['date_added'])
                if parsed_date:
                    enhanced_data['date_added'] = self.date_utils.format_date(parsed_date)
            
            # Add to database
            self.bidders_db['bidders'].append(enhanced_data)
            self._save_database()
            
            logging.info(f"Added bidder: {enhanced_data['name']}")
            return True
            
        except Exception as e:
            logging.error(f"Error adding bidder: {e}")
            return False
    
    def update_bidder(self, bidder_id: str, updated_data: Dict[str, Any]) -> bool:
        """
        Update existing bidder information.
        
        Args:
            bidder_id: Unique identifier for the bidder
            updated_data: Dictionary containing updated information
            
        Returns:
            True if successful, False otherwise
        """
        try:
            for bidder in self.bidders_db['bidders']:
                if bidder.get('id') == bidder_id:
                    # Update fields
                    for key, value in updated_data.items():
                        if key != 'id':  # Don't allow ID changes
                            bidder[key] = value
                    
                    # Update timestamp
                    bidder['last_updated'] = self.date_utils.get_current_date()
                    
                    self._save_database()
                    logging.info(f"Updated bidder: {bidder['name']}")
                    return True
            
            logging.warning(f"Bidder with ID {bidder_id} not found")
            return False
            
        except Exception as e:
            logging.error(f"Error updating bidder: {e}")
            return False
    
    def remove_bidder(self, bidder_id: str) -> bool:
        """
        Remove bidder from database.
        
        Args:
            bidder_id: Unique identifier for the bidder
            
        Returns:
            True if successful, False otherwise
        """
        try:
            original_count = len(self.bidders_db['bidders'])
            self.bidders_db['bidders'] = [
                b for b in self.bidders_db['bidders'] 
                if b.get('id') != bidder_id
            ]
            
            if len(self.bidders_db['bidders']) < original_count:
                self._save_database()
                logging.info(f"Removed bidder with ID: {bidder_id}")
                return True
            else:
                logging.warning(f"Bidder with ID {bidder_id} not found")
                return False
                
        except Exception as e:
            logging.error(f"Error removing bidder: {e}")
            return False
    
    def get_bidder(self, bidder_id: str) -> Optional[Dict[str, Any]]:
        """
        Get bidder by ID.
        
        Args:
            bidder_id: Unique identifier for the bidder
            
        Returns:
            Bidder dictionary or None if not found
        """
        for bidder in self.bidders_db['bidders']:
            if bidder.get('id') == bidder_id:
                return bidder.copy()
        return None
    
    def get_all_bidders(self) -> List[Dict[str, Any]]:
        """
        Get all bidders from database.
        
        Returns:
            List of all bidder dictionaries
        """
        return [bidder.copy() for bidder in self.bidders_db['bidders']]
    
    def search_bidders(self, search_term: str) -> List[Dict[str, Any]]:
        """
        Search bidders by name.
        
        Args:
            search_term: Term to search for in bidder names
            
        Returns:
            List of matching bidder dictionaries
        """
        search_term = search_term.lower()
        results = []
        
        for bidder in self.bidders_db['bidders']:
            if search_term in bidder.get('name', '').lower():
                results.append(bidder.copy())
        
        return results
    
    def get_bidder_suggestions(self, partial_name: str, limit: int = 5) -> List[str]:
        """
        Get bidder name suggestions for auto-completion.
        
        Args:
            partial_name: Partial bidder name
            limit: Maximum number of suggestions
            
        Returns:
            List of suggested bidder names
        """
        partial_name = partial_name.lower()
        suggestions = []
        
        for bidder in self.bidders_db['bidders']:
            name = bidder.get('name', '')
            if partial_name in name.lower() and name not in suggestions:
                suggestions.append(name)
                if len(suggestions) >= limit:
                    break
        
        return suggestions
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get database statistics.
        
        Returns:
            Statistics dictionary
        """
        bidders = self.bidders_db['bidders']
        
        if not bidders:
            return {
                'total_bidders': 0,
                'average_percentage': 0,
                'most_common_bidder': None,
                'date_range': None,
                'last_updated': self.bidders_db['statistics'].get('last_updated', '')
            }
        
        # Calculate statistics
        percentages = [b.get('percentage', 0) for b in bidders if 'percentage' in b]
        bid_amounts = [b.get('bid_amount', 0) for b in bidders if 'bid_amount' in b]
        
        # Find most common bidder
        bidder_counts = {}
        for bidder in bidders:
            name = bidder.get('name', '')
            bidder_counts[name] = bidder_counts.get(name, 0) + 1
        
        most_common_bidder = max(bidder_counts.items(), key=lambda x: x[1])[0] if bidder_counts else None
        
        # Date range
        dates = []
        for bidder in bidders:
            date_added = bidder.get('date_added', '')
            parsed_date = self.date_utils.parse_date(date_added)
            if parsed_date:
                dates.append(parsed_date)
        
        date_range = None
        if dates:
            min_date = min(dates)
            max_date = max(dates)
            date_range = f"{self.date_utils.format_date(min_date)} to {self.date_utils.format_date(max_date)}"
        
        return {
            'total_bidders': len(bidders),
            'unique_bidders': len(bidder_counts),
            'average_percentage': sum(percentages) / len(percentages) if percentages else 0,
            'average_bid_amount': sum(bid_amounts) / len(bid_amounts) if bid_amounts else 0,
            'most_common_bidder': most_common_bidder,
            'date_range': date_range,
            'last_updated': self.bidders_db['statistics'].get('last_updated', '')
        }
    
    def _generate_bidder_id(self) -> str:
        """Generate unique bidder ID."""
        import uuid
        return str(uuid.uuid4())[:8]
    
    def export_data(self, file_path: str) -> bool:
        """
        Export bidder data to file.
        
        Args:
            file_path: Path to export file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if file_path.endswith('.json'):
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(self.bidders_db, f, indent=2, ensure_ascii=False)
            elif file_path.endswith('.csv'):
                import pandas as pd
                df = pd.DataFrame(self.bidders_db['bidders'])
                df.to_csv(file_path, index=False)
            else:
                raise ValueError("Unsupported file format. Use .json or .csv")
            
            logging.info(f"Exported data to {file_path}")
            return True
            
        except Exception as e:
            logging.error(f"Error exporting data: {e}")
            return False
    
    def import_data(self, file_path: str) -> bool:
        """
        Import bidder data from file.
        
        Args:
            file_path: Path to import file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if file_path.endswith('.json'):
                with open(file_path, 'r', encoding='utf-8') as f:
                    imported_data = json.load(f)
                    
                if 'bidders' in imported_data:
                    self.bidders_db = imported_data
                else:
                    # Assume it's a list of bidders
                    self.bidders_db['bidders'] = imported_data
                    
            elif file_path.endswith('.csv'):
                import pandas as pd
                df = pd.read_csv(file_path)
                self.bidders_db['bidders'] = df.to_dict('records')
            else:
                raise ValueError("Unsupported file format. Use .json or .csv")
            
            self._save_database()
            logging.info(f"Imported data from {file_path}")
            return True
            
        except Exception as e:
            logging.error(f"Error importing data: {e}")
            return False

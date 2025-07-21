from datetime import datetime, timedelta
import calendar
import logging
from typing import Optional, Union

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DateUtils:
    """Centralized date utility class for handling multiple date formats and operations."""
    
    SUPPORTED_FORMATS = [
        '%d/%m/%Y',    # DD/MM/YYYY
        '%d-%m-%Y',    # DD-MM-YYYY
        '%Y-%m-%d',    # YYYY-MM-DD
        '%d.%m.%Y',    # DD.MM.YYYY
        '%m/%d/%Y',    # MM/DD/YYYY (US format)
    ]
    
    OUTPUT_FORMAT = '%d/%m/%Y'  # Standard output format
    DISPLAY_FORMAT = '%d-%m-%Y'  # Display format for documents
    
    @classmethod
    def parse_date(cls, date_str: Union[str, datetime]) -> Optional[datetime]:
        """
        Parse date from various string formats.
        
        Args:
            date_str: Date string in various formats or datetime object
            
        Returns:
            datetime object or None if parsing fails
        """
        if isinstance(date_str, datetime):
            return date_str
            
        if not date_str or not isinstance(date_str, str):
            return None
            
        date_str = date_str.strip()
        
        for date_format in cls.SUPPORTED_FORMATS:
            try:
                return datetime.strptime(date_str, date_format)
            except ValueError:
                continue
                
        logging.warning(f"Unable to parse date: {date_str}")
        return None
    
    @classmethod
    def format_date(cls, date_obj: Union[datetime, str], output_format: str = None) -> str:
        """
        Format datetime object to string.
        
        Args:
            date_obj: datetime object or date string
            output_format: desired output format (default: DD/MM/YYYY)
            
        Returns:
            Formatted date string
        """
        if output_format is None:
            output_format = cls.OUTPUT_FORMAT
            
        if isinstance(date_obj, str):
            date_obj = cls.parse_date(date_obj)
            
        if date_obj is None:
            return ""
            
        try:
            return date_obj.strftime(output_format)
        except Exception as e:
            logging.error(f"Error formatting date {date_obj}: {e}")
            return ""
    
    @classmethod
    def format_display_date(cls, date_obj: Union[datetime, str]) -> str:
        """Format date for display in documents (DD-MM-YYYY)."""
        return cls.format_date(date_obj, cls.DISPLAY_FORMAT)
    
    @classmethod
    def add_months(cls, date_obj: Union[datetime, str], months: int) -> datetime:
        """
        Add months to a date, handling month-end edge cases.
        
        Args:
            date_obj: datetime object or date string
            months: number of months to add
            
        Returns:
            New datetime object
        """
        if isinstance(date_obj, str):
            date_obj = cls.parse_date(date_obj)
            
        if date_obj is None:
            raise ValueError("Invalid date provided")
            
        year = date_obj.year + (date_obj.month + months - 1) // 12
        month = (date_obj.month + months - 1) % 12 + 1
        day = min(date_obj.day, calendar.monthrange(year, month)[1])
        
        return datetime(year, month, day, date_obj.hour, date_obj.minute, date_obj.second)
    
    @classmethod
    def add_days(cls, date_obj: Union[datetime, str], days: int) -> datetime:
        """
        Add days to a date.
        
        Args:
            date_obj: datetime object or date string
            days: number of days to add
            
        Returns:
            New datetime object
        """
        if isinstance(date_obj, str):
            date_obj = cls.parse_date(date_obj)
            
        if date_obj is None:
            raise ValueError("Invalid date provided")
            
        return date_obj + timedelta(days=days)
    
    @classmethod
    def calculate_completion_date(cls, start_date: Union[datetime, str], 
                                time_completion: str) -> datetime:
        """
        Calculate completion date based on start date and time period.
        
        Args:
            start_date: Start date
            time_completion: Time period string (e.g., "3 Months", "45 Days")
            
        Returns:
            Completion date
        """
        if isinstance(start_date, str):
            start_date = cls.parse_date(start_date)
            
        if start_date is None:
            raise ValueError("Invalid start date provided")
            
        time_completion = time_completion.strip().lower()
        
        # Extract number and unit
        parts = time_completion.split()
        if len(parts) < 2:
            raise ValueError(f"Invalid time completion format: {time_completion}")
            
        try:
            number = int(parts[0])
            unit = parts[1].lower()
            
            if 'month' in unit:
                return cls.add_months(start_date, number)
            elif 'day' in unit:
                return cls.add_days(start_date, number)
            elif 'week' in unit:
                return cls.add_days(start_date, number * 7)
            elif 'year' in unit:
                return cls.add_months(start_date, number * 12)
            else:
                raise ValueError(f"Unsupported time unit: {unit}")
                
        except (ValueError, IndexError) as e:
            logging.error(f"Error parsing time completion '{time_completion}': {e}")
            # Default to 3 months if parsing fails
            return cls.add_months(start_date, 3)
    
    @classmethod
    def validate_date_range(cls, start_date: Union[datetime, str], 
                          end_date: Union[datetime, str]) -> bool:
        """
        Validate that end date is after start date.
        
        Args:
            start_date: Start date
            end_date: End date
            
        Returns:
            True if valid range, False otherwise
        """
        if isinstance(start_date, str):
            start_date = cls.parse_date(start_date)
        if isinstance(end_date, str):
            end_date = cls.parse_date(end_date)
            
        if start_date is None or end_date is None:
            return False
            
        return end_date >= start_date
    
    @classmethod
    def get_current_date(cls, format_str: str = None) -> str:
        """Get current date in specified format."""
        if format_str is None:
            format_str = cls.OUTPUT_FORMAT
        return datetime.now().strftime(format_str)
    
    @classmethod
    def is_valid_date_string(cls, date_str: str) -> bool:
        """Check if a string can be parsed as a valid date."""
        return cls.parse_date(date_str) is not None

# Convenience functions for backward compatibility
def parse_date(date_str: Union[str, datetime]) -> Optional[datetime]:
    """Parse date from string - convenience function."""
    return DateUtils.parse_date(date_str)

def format_date(date_obj: Union[datetime, str], output_format: str = None) -> str:
    """Format date to string - convenience function."""
    return DateUtils.format_date(date_obj, output_format)

def format_display_date(date_obj: Union[datetime, str]) -> str:
    """Format date for display - convenience function."""
    return DateUtils.format_display_date(date_obj)

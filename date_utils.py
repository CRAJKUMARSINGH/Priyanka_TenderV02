import logging
from datetime import datetime, date, timedelta
from typing import Union, Optional, Dict, Any
import re

logger = logging.getLogger(__name__)

class DateUtils:
    """Enhanced date utilities for tender processing system"""
    
    @staticmethod
    def get_current_date_statutory() -> str:
        """Get current date in statutory format (DD-MM-YY)"""
        return datetime.now().strftime('%d-%m-%y')
    
    @staticmethod
    def get_current_date_full() -> str:
        """Get current date in full format (DD-MM-YYYY)"""
        return datetime.now().strftime('%d-%m-%Y')
    
    @staticmethod
    def format_date_statutory(date_obj: Union[datetime, date, str]) -> str:
        """Format date in statutory format (DD-MM-YY)"""
        try:
            if isinstance(date_obj, str):
                # Try to parse string date
                parsed_date = DateUtils.parse_date_string(date_obj)
                if parsed_date:
                    return parsed_date.strftime('%d-%m-%y')
                else:
                    return DateUtils.get_current_date_statutory()
            
            elif isinstance(date_obj, date):
                return date_obj.strftime('%d-%m-%y')
            
            elif isinstance(date_obj, datetime):
                return date_obj.strftime('%d-%m-%y')
            
            else:
                logger.warning(f"Invalid date type: {type(date_obj)}")
                return DateUtils.get_current_date_statutory()
                
        except Exception as e:
            logger.error(f"Error formatting date: {str(e)}")
            return DateUtils.get_current_date_statutory()
    
    @staticmethod
    def format_date_full(date_obj: Union[datetime, date, str]) -> str:
        """Format date in full format (DD-MM-YYYY)"""
        try:
            if isinstance(date_obj, str):
                parsed_date = DateUtils.parse_date_string(date_obj)
                if parsed_date:
                    return parsed_date.strftime('%d-%m-%Y')
                else:
                    return DateUtils.get_current_date_full()
            
            elif isinstance(date_obj, date):
                return date_obj.strftime('%d-%m-%Y')
            
            elif isinstance(date_obj, datetime):
                return date_obj.strftime('%d-%m-%Y')
            
            else:
                return DateUtils.get_current_date_full()
                
        except Exception as e:
            logger.error(f"Error formatting date: {str(e)}")
            return DateUtils.get_current_date_full()
    
    @staticmethod
    def parse_date_string(date_str: str) -> Optional[datetime]:
        """Parse date string in various formats"""
        if not date_str:
            return None
        
        # Common date formats
        formats = [
            '%d-%m-%Y',     # 25-12-2024
            '%d/%m/%Y',     # 25/12/2024
            '%d-%m-%y',     # 25-12-24
            '%d/%m/%y',     # 25/12/24
            '%Y-%m-%d',     # 2024-12-25
            '%Y/%m/%d',     # 2024/12/25
            '%d.%m.%Y',     # 25.12.2024
            '%d.%m.%y',     # 25.12.24
        ]
        
        # Clean the input string
        cleaned_date = str(date_str).strip()
        
        for fmt in formats:
            try:
                return datetime.strptime(cleaned_date, fmt)
            except ValueError:
                continue
        
        logger.warning(f"Could not parse date string: {date_str}")
        return None
    
    @staticmethod
    def validate_date_format(date_str: str, format_str: str = "%d-%m-%Y") -> bool:
        """Validate date string against specific format"""
        try:
            datetime.strptime(date_str, format_str)
            return True
        except ValueError:
            return False
    
    @staticmethod
    def get_financial_year(date_obj: Optional[Union[datetime, date]] = None) -> str:
        """Get financial year in format YYYY-YY"""
        try:
            if date_obj is None:
                date_obj = datetime.now()
            
            if isinstance(date_obj, datetime):
                current_date = date_obj.date()
            else:
                current_date = date_obj
            
            # Financial year starts from April 1st
            if current_date.month >= 4:  # April to March
                start_year = current_date.year
                end_year = current_date.year + 1
            else:  # January to March
                start_year = current_date.year - 1
                end_year = current_date.year
            
            return f"{start_year}-{str(end_year)[2:]}"
            
        except Exception as e:
            logger.error(f"Error getting financial year: {str(e)}")
            current_year = datetime.now().year
            return f"{current_year}-{str(current_year + 1)[2:]}"
    
    @staticmethod
    def add_working_days(start_date: Union[datetime, date], days: int) -> date:
        """Add working days (excluding weekends) to a date"""
        try:
            if isinstance(start_date, datetime):
                current_date = start_date.date()
            else:
                current_date = start_date
            
            days_added = 0
            while days_added < days:
                current_date += timedelta(days=1)
                # Skip weekends (Saturday=5, Sunday=6)
                if current_date.weekday() < 5:
                    days_added += 1
            
            return current_date
            
        except Exception as e:
            logger.error(f"Error adding working days: {str(e)}")
            return datetime.now().date()
    
    @staticmethod
    def get_date_range_display(start_date: Union[datetime, date], end_date: Union[datetime, date]) -> str:
        """Get formatted date range for display"""
        try:
            start_str = DateUtils.format_date_statutory(start_date)
            end_str = DateUtils.format_date_statutory(end_date)
            return f"{start_str} to {end_str}"
        except Exception as e:
            logger.error(f"Error formatting date range: {str(e)}")
            return "Date range unavailable"
    
    @staticmethod
    def calculate_days_difference(start_date: Union[datetime, date], end_date: Union[datetime, date]) -> int:
        """Calculate difference between two dates in days"""
        try:
            if isinstance(start_date, datetime):
                start_date = start_date.date()
            if isinstance(end_date, datetime):
                end_date = end_date.date()
            
            diff = end_date - start_date
            return diff.days
            
        except Exception as e:
            logger.error(f"Error calculating date difference: {str(e)}")
            return 0
    
    @staticmethod
    def get_completion_date(start_date: Union[datetime, date], months: int) -> date:
        """Calculate completion date by adding months to start date"""
        try:
            if isinstance(start_date, datetime):
                start_date = start_date.date()
            
            # Simple month addition (may need adjustment for edge cases)
            year = start_date.year
            month = start_date.month + months
            day = start_date.day
            
            # Handle year overflow
            while month > 12:
                year += 1
                month -= 12
            
            # Handle day overflow for months with different days
            try:
                completion_date = date(year, month, day)
            except ValueError:
                # Handle cases like Feb 30 -> last day of Feb
                if month == 2:
                    # Check for leap year
                    if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):
                        completion_date = date(year, month, 29)
                    else:
                        completion_date = date(year, month, 28)
                else:
                    # For other months, use 30 days
                    completion_date = date(year, month, 30)
            
            return completion_date
            
        except Exception as e:
            logger.error(f"Error calculating completion date: {str(e)}")
            return datetime.now().date() + timedelta(days=30 * months)
    
    @staticmethod
    def format_duration_display(months: int) -> str:
        """Format duration for display"""
        try:
            if months <= 0:
                return "Invalid duration"
            elif months == 1:
                return "1 month"
            elif months < 12:
                return f"{months} months"
            else:
                years = months // 12
                remaining_months = months % 12
                
                if remaining_months == 0:
                    return f"{years} year{'s' if years > 1 else ''}"
                else:
                    return f"{years} year{'s' if years > 1 else ''} {remaining_months} month{'s' if remaining_months > 1 else ''}"
                    
        except Exception as e:
            logger.error(f"Error formatting duration: {str(e)}")
            return f"{months} months"
    
    @staticmethod
    def is_valid_tender_date(tender_date: Union[datetime, date, str]) -> bool:
        """Validate if tender date is reasonable"""
        try:
            if isinstance(tender_date, str):
                parsed_date = DateUtils.parse_date_string(tender_date)
                if not parsed_date:
                    return False
                check_date = parsed_date.date()
            elif isinstance(tender_date, datetime):
                check_date = tender_date.date()
            elif isinstance(tender_date, date):
                check_date = tender_date
            else:
                return False
            
            current_date = datetime.now().date()
            
            # Tender date should not be more than 2 years in the past
            min_date = current_date - timedelta(days=730)
            
            # Tender date should not be more than 1 year in the future
            max_date = current_date + timedelta(days=365)
            
            return min_date <= check_date <= max_date
            
        except Exception as e:
            logger.error(f"Error validating tender date: {str(e)}")
            return False
    
    @staticmethod
    def get_date_validation_info(date_str: str) -> Dict[str, Any]:
        """Get comprehensive date validation information"""
        try:
            result = {
                'is_valid': False,
                'parsed_date': None,
                'formatted_statutory': '',
                'formatted_full': '',
                'error_message': '',
                'format_detected': ''
            }
            
            if not date_str:
                result['error_message'] = "Date string is empty"
                return result
            
            # Try to parse the date
            parsed_date = DateUtils.parse_date_string(date_str)
            
            if parsed_date:
                result['is_valid'] = True
                result['parsed_date'] = parsed_date
                result['formatted_statutory'] = DateUtils.format_date_statutory(parsed_date)
                result['formatted_full'] = DateUtils.format_date_full(parsed_date)
                
                # Determine format
                if re.match(r'\d{2}-\d{2}-\d{4}', date_str):
                    result['format_detected'] = 'DD-MM-YYYY'
                elif re.match(r'\d{2}/\d{2}/\d{4}', date_str):
                    result['format_detected'] = 'DD/MM/YYYY'
                elif re.match(r'\d{2}-\d{2}-\d{2}', date_str):
                    result['format_detected'] = 'DD-MM-YY'
                else:
                    result['format_detected'] = 'Auto-detected'
                
                # Validate reasonableness
                if not DateUtils.is_valid_tender_date(parsed_date):
                    result['error_message'] = "Date is outside reasonable range for tender dates"
            else:
                result['error_message'] = f"Could not parse date format: {date_str}"
            
            return result
            
        except Exception as e:
            logger.error(f"Error in date validation: {str(e)}")
            return {
                'is_valid': False,
                'error_message': f"Date validation error: {str(e)}"
            }
    
    @staticmethod
    def suggest_date_format(date_str: str) -> str:
        """Suggest correct date format based on input"""
        if not date_str:
            return "Please enter date in DD-MM-YYYY format"
        
        # Analyze the input pattern
        if re.match(r'\d{1,2}[/-]\d{1,2}[/-]\d{4}', date_str):
            return "Format detected. Use DD-MM-YYYY for best results"
        elif re.match(r'\d{4}[/-]\d{1,2}[/-]\d{1,2}', date_str):
            return "Year-first format detected. Please use DD-MM-YYYY"
        elif re.match(r'\d{1,2}[/-]\d{1,2}[/-]\d{2}', date_str):
            return "Two-digit year detected. Consider using DD-MM-YYYY"
        else:
            return "Please use DD-MM-YYYY format (e.g., 25-12-2024)"

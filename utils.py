import re
import logging
from typing import Any, Optional, Union
from datetime import datetime

logger = logging.getLogger(__name__)

def validate_percentage(percentage: Union[str, float, int]) -> bool:
    """Validate percentage value"""
    try:
        if isinstance(percentage, str):
            # Remove % symbol and whitespace
            cleaned = percentage.replace('%', '').strip()
            percentage = float(cleaned)
        
        # Check if percentage is within reasonable range
        return -50.0 <= float(percentage) <= 100.0
        
    except (ValueError, TypeError):
        return False

def format_currency(amount: Union[str, float, int]) -> str:
    """Format currency amount with Indian numbering system"""
    try:
        if amount is None:
            return "0"
        
        # Convert to float and then to int for clean display
        amount = float(amount)
        amount_int = int(amount)
        
        # Format with Indian numbering (lakhs, crores)
        if amount_int >= 10000000:  # 1 crore
            crores = amount_int // 10000000
            remainder = amount_int % 10000000
            if remainder == 0:
                return f"{crores} Cr"
            else:
                lakhs = remainder // 100000
                if lakhs == 0:
                    return f"{crores} Cr"
                else:
                    return f"{crores}.{lakhs:02d} Cr"
        
        elif amount_int >= 100000:  # 1 lakh
            lakhs = amount_int // 100000
            remainder = amount_int % 100000
            if remainder == 0:
                return f"{lakhs} L"
            else:
                thousands = remainder // 1000
                if thousands == 0:
                    return f"{lakhs} L"
                else:
                    return f"{lakhs}.{thousands:02d} L"
        
        elif amount_int >= 1000:  # 1 thousand
            return f"{amount_int // 1000}K"
        
        else:
            return str(amount_int)
            
    except (ValueError, TypeError) as e:
        logger.warning(f"Error formatting currency {amount}: {str(e)}")
        return str(amount) if amount else "0"

def validate_nit_number(nit_number: str) -> bool:
    """Validate NIT number format"""
    if not nit_number or not isinstance(nit_number, str):
        return False
    
    # Common NIT number patterns
    patterns = [
        r'^\d+\/\d{4}-\d{2}$',  # 27/2024-25
        r'^\d+\/\d{4}$',        # 27/2024
        r'^NIT-\d+\/\d{4}$',    # NIT-27/2024
        r'^\d+-\d{4}$',         # 27-2024
        r'^[A-Z]+\d+\/\d{4}$',  # PWD27/2024
    ]
    
    for pattern in patterns:
        if re.match(pattern, nit_number.strip()):
            return True
    
    return False

def clean_text_for_latex(text: str) -> str:
    """Clean and escape text for LaTeX processing"""
    if not text:
        return ""
    
    # LaTeX special characters that need escaping
    replacements = {
        '\\': '\\textbackslash{}',
        '{': '\\{',
        '}': '\\}',
        '$': '\\$',
        '&': '\\&',
        '%': '\\%',
        '#': '\\#',
        '^': '\\textasciicircum{}',
        '_': '\\_',
        '~': '\\textasciitilde{}'
    }
    
    cleaned = str(text)
    for char, replacement in replacements.items():
        cleaned = cleaned.replace(char, replacement)
    
    return cleaned

def parse_amount_string(amount_str: str) -> Optional[float]:
    """Parse amount string and convert to float"""
    if not amount_str:
        return None
    
    try:
        # Remove currency symbols and formatting
        cleaned = str(amount_str).strip()
        
        # Remove common currency symbols and text
        remove_patterns = [
            r'[₹\$£€¥]',  # Currency symbols
            r'\bRs\.?\b',  # Rs or Rs.
            r'\bINR\b',    # INR
            r'\bUSD\b',    # USD
            r'\bcrores?\b', # crore/crores
            r'\blakhs?\b',  # lakh/lakhs
            r'\bthousands?\b', # thousand/thousands
        ]
        
        for pattern in remove_patterns:
            cleaned = re.sub(pattern, '', cleaned, flags=re.IGNORECASE)
        
        # Remove commas and extra spaces
        cleaned = re.sub(r'[,\s]', '', cleaned)
        
        # Handle special cases
        if 'crore' in amount_str.lower():
            base_amount = float(re.findall(r'\d+(?:\.\d+)?', cleaned)[0])
            return base_amount * 10000000
        elif 'lakh' in amount_str.lower():
            base_amount = float(re.findall(r'\d+(?:\.\d+)?', cleaned)[0])
            return base_amount * 100000
        elif 'thousand' in amount_str.lower() or 'k' in amount_str.lower():
            base_amount = float(re.findall(r'\d+(?:\.\d+)?', cleaned)[0])
            return base_amount * 1000
        
        # Extract numeric value
        numbers = re.findall(r'\d+(?:\.\d+)?', cleaned)
        if numbers:
            return float(numbers[0])
        
        return None
        
    except (ValueError, IndexError) as e:
        logger.warning(f"Could not parse amount string '{amount_str}': {str(e)}")
        return None

def validate_email(email: str) -> bool:
    """Validate email address format"""
    if not email:
        return False
    
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_phone(phone: str) -> bool:
    """Validate phone number format (Indian)"""
    if not phone:
        return False
    
    # Remove all non-digit characters
    digits_only = re.sub(r'\D', '', phone)
    
    # Indian phone patterns
    patterns = [
        r'^\d{10}$',      # 10 digits
        r'^91\d{10}$',    # +91 followed by 10 digits
        r'^\d{11}$',      # 11 digits (with STD code)
    ]
    
    for pattern in patterns:
        if re.match(pattern, digits_only):
            return True
    
    return False

def sanitize_filename(filename: str) -> str:
    """Sanitize filename for safe file operations"""
    if not filename:
        return "untitled"
    
    # Remove or replace unsafe characters
    unsafe_chars = '<>:"/\\|?*'
    sanitized = filename
    
    for char in unsafe_chars:
        sanitized = sanitized.replace(char, '_')
    
    # Remove leading/trailing dots and spaces
    sanitized = sanitized.strip('. ')
    
    # Ensure filename is not empty and not too long
    if not sanitized:
        sanitized = "untitled"
    
    if len(sanitized) > 200:
        sanitized = sanitized[:200]
    
    return sanitized

def calculate_earnest_money_percentage(earnest_money: float, estimated_cost: float) -> float:
    """Calculate earnest money as percentage of estimated cost"""
    try:
        if estimated_cost <= 0:
            return 0.0
        
        percentage = (earnest_money / estimated_cost) * 100
        return round(percentage, 2)
        
    except (ValueError, ZeroDivisionError):
        return 0.0

def format_percentage_display(percentage: float) -> str:
    """Format percentage for display in statutory format"""
    try:
        if percentage > 0:
            return f"{percentage:.2f}% ABOVE"
        elif percentage < 0:
            return f"{abs(percentage):.2f}% BELOW"
        else:
            return "AT ESTIMATE"
            
    except (ValueError, TypeError):
        return "AT ESTIMATE"

def validate_date_format(date_str: str, format_str: str = "%d-%m-%Y") -> bool:
    """Validate date string format"""
    try:
        datetime.strptime(date_str, format_str)
        return True
    except ValueError:
        return False

def format_date_statutory(date_obj: datetime) -> str:
    """Format date in statutory format (DD-MM-YY)"""
    try:
        return date_obj.strftime('%d-%m-%y')
    except (ValueError, AttributeError):
        return datetime.now().strftime('%d-%m-%y')

def extract_numbers_from_text(text: str) -> list:
    """Extract all numbers from text"""
    if not text:
        return []
    
    # Find all numbers (including decimals)
    numbers = re.findall(r'\d+(?:\.\d+)?', str(text))
    return [float(num) for num in numbers]

def is_valid_work_name(work_name: str) -> bool:
    """Validate work name for minimum requirements"""
    if not work_name or not isinstance(work_name, str):
        return False
    
    cleaned = work_name.strip()
    
    # Minimum length check
    if len(cleaned) < 10:
        return False
    
    # Should contain some meaningful words
    meaningful_words = ['construction', 'repair', 'maintenance', 'building', 
                       'road', 'bridge', 'work', 'project', 'development',
                       'installation', 'renovation', 'extension']
    
    cleaned_lower = cleaned.lower()
    has_meaningful_word = any(word in cleaned_lower for word in meaningful_words)
    
    # Should have reasonable word count
    word_count = len(cleaned.split())
    
    return has_meaningful_word or word_count >= 3

def calculate_bid_amount(estimated_cost: float, percentage: float) -> float:
    """Calculate bid amount from estimated cost and percentage"""
    try:
        return round(estimated_cost * (1 + percentage / 100), 2)
    except (ValueError, TypeError):
        return 0.0

def generate_nit_display_name(nit_data: dict) -> str:
    """Generate display name for NIT selection"""
    nit_number = nit_data.get('nit_number', 'Unknown')
    work_name = nit_data.get('work_name', 'Unnamed Work')
    
    # Truncate work name if too long
    if len(work_name) > 50:
        work_name = work_name[:47] + "..."
    
    bidder_count = len(nit_data.get('bidders', []))
    
    return f"{nit_number} - {work_name} ({bidder_count} bidders)"

def validate_numeric_field(value: Any, field_name: str, min_value: float = 0) -> tuple:
    """Validate numeric field and return (is_valid, cleaned_value, error_message)"""
    try:
        if value is None or value == "":
            return False, None, f"{field_name} is required"
        
        # Try to convert to float
        if isinstance(value, str):
            # Remove formatting
            cleaned = re.sub(r'[,\s₹$]', '', value)
            numeric_value = float(cleaned)
        else:
            numeric_value = float(value)
        
        # Check minimum value
        if numeric_value < min_value:
            return False, None, f"{field_name} must be at least {min_value}"
        
        return True, numeric_value, None
        
    except (ValueError, TypeError):
        return False, None, f"{field_name} must be a valid number"

def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    """Safely divide two numbers, returning default if division by zero"""
    try:
        if denominator == 0:
            return default
        return numerator / denominator
    except (ValueError, TypeError):
        return default

def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """Truncate text to specified length with suffix"""
    if not text:
        return ""
    
    text = str(text).strip()
    
    if len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix

def get_file_size_mb(file_obj) -> float:
    """Get file size in MB"""
    try:
        # Get current position
        current_pos = file_obj.tell()
        
        # Go to end to get size
        file_obj.seek(0, 2)
        size_bytes = file_obj.tell()
        
        # Reset position
        file_obj.seek(current_pos)
        
        # Convert to MB
        return size_bytes / (1024 * 1024)
        
    except Exception:
        return 0.0

def validate_file_type(filename: str, allowed_extensions: list) -> bool:
    """Validate file type by extension"""
    if not filename:
        return False
    
    file_ext = filename.lower().split('.')[-1]
    return file_ext in [ext.lower().lstrip('.') for ext in allowed_extensions]

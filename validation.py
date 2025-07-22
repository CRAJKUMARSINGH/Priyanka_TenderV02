import logging
import re
from typing import Dict, List, Any, Optional, Union, Tuple
from datetime import datetime
import os

logger = logging.getLogger(__name__)

class ValidationManager:
    """Comprehensive validation manager for tender processing system"""
    
    def __init__(self):
        self.required_fields = {
            'basic': ['nit_number', 'work_name', 'estimated_cost', 'earnest_money', 'time_of_completion'],
            'bidder': ['name', 'percentage'],
            'optional': ['schedule_amount', 'ee_name', 'date', 'contact']
        }
        
        self.field_constraints = {
            'estimated_cost': {'min': 1000, 'max': 10000000000},  # 1K to 1000 Cr
            'earnest_money': {'min': 100, 'max': 100000000},      # 100 to 10 Cr
            'time_of_completion': {'min': 1, 'max': 120},         # 1 to 120 months
            'percentage': {'min': -50.0, 'max': 100.0},           # -50% to +100%
            'work_name': {'min_length': 10, 'max_length': 500},
            'nit_number': {'min_length': 3, 'max_length': 50}
        }
    
    def validate_tender_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Comprehensive tender data validation"""
        try:
            validation_result = {
                'is_valid': True,
                'errors': [],
                'warnings': [],
                'field_status': {},
                'summary': {}
            }
            
            # Validate required fields
            missing_fields = self._check_required_fields(data)
            if missing_fields:
                validation_result['errors'].extend([f"Missing required field: {field}" for field in missing_fields])
                validation_result['is_valid'] = False
            
            # Validate field formats and constraints
            field_validations = self._validate_individual_fields(data)
            validation_result['field_status'] = field_validations['field_status']
            validation_result['errors'].extend(field_validations['errors'])
            validation_result['warnings'].extend(field_validations['warnings'])
            
            if field_validations['errors']:
                validation_result['is_valid'] = False
            
            # Business logic validations
            business_validations = self._validate_business_logic(data)
            validation_result['warnings'].extend(business_validations['warnings'])
            if business_validations['errors']:
                validation_result['errors'].extend(business_validations['errors'])
                validation_result['is_valid'] = False
            
            # Generate summary
            validation_result['summary'] = self._generate_validation_summary(validation_result)
            
            return validation_result
            
        except Exception as e:
            logger.error(f"Error in tender data validation: {str(e)}")
            return {
                'is_valid': False,
                'errors': [f"Validation system error: {str(e)}"],
                'warnings': [],
                'field_status': {},
                'summary': {'total_errors': 1, 'total_warnings': 0}
            }
    
    def validate_bidder_data(self, bidders: List[Dict[str, Any]], estimated_cost: float) -> Dict[str, Any]:
        """Validate bidder data"""
        try:
            validation_result = {
                'is_valid': True,
                'errors': [],
                'warnings': [],
                'bidder_status': [],
                'summary': {}
            }
            
            if not bidders:
                validation_result['errors'].append("At least one bidder is required")
                validation_result['is_valid'] = False
                return validation_result
            
            # Validate each bidder
            for i, bidder in enumerate(bidders, 1):
                bidder_validation = self._validate_single_bidder(bidder, estimated_cost, i)
                validation_result['bidder_status'].append(bidder_validation)
                
                if bidder_validation['errors']:
                    validation_result['errors'].extend(bidder_validation['errors'])
                    validation_result['is_valid'] = False
                
                validation_result['warnings'].extend(bidder_validation['warnings'])
            
            # Cross-bidder validations
            cross_validations = self._validate_cross_bidder_logic(bidders)
            validation_result['warnings'].extend(cross_validations['warnings'])
            if cross_validations['errors']:
                validation_result['errors'].extend(cross_validations['errors'])
                validation_result['is_valid'] = False
            
            # Generate summary
            validation_result['summary'] = self._generate_bidder_validation_summary(validation_result, bidders)
            
            return validation_result
            
        except Exception as e:
            logger.error(f"Error in bidder validation: {str(e)}")
            return {
                'is_valid': False,
                'errors': [f"Bidder validation error: {str(e)}"],
                'warnings': [],
                'bidder_status': [],
                'summary': {}
            }
    
    def _check_required_fields(self, data: Dict[str, Any]) -> List[str]:
        """Check for missing required fields"""
        missing = []
        for field in self.required_fields['basic']:
            if field not in data or not data[field] or (isinstance(data[field], str) and not data[field].strip()):
                missing.append(field)
        return missing
    
    def _validate_individual_fields(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate individual field formats and constraints"""
        result = {'errors': [], 'warnings': [], 'field_status': {}}
        
        # NIT Number validation
        if 'nit_number' in data:
            nit_validation = self._validate_nit_number(data['nit_number'])
            result['field_status']['nit_number'] = nit_validation
            if not nit_validation['is_valid']:
                result['errors'].append(f"NIT Number: {nit_validation['error']}")
        
        # Work Name validation
        if 'work_name' in data:
            work_validation = self._validate_work_name(data['work_name'])
            result['field_status']['work_name'] = work_validation
            if not work_validation['is_valid']:
                result['errors'].append(f"Work Name: {work_validation['error']}")
            elif work_validation.get('warning'):
                result['warnings'].append(f"Work Name: {work_validation['warning']}")
        
        # Numeric field validations
        numeric_fields = ['estimated_cost', 'earnest_money', 'time_of_completion', 'schedule_amount']
        for field in numeric_fields:
            if field in data:
                numeric_validation = self._validate_numeric_field(data[field], field)
                result['field_status'][field] = numeric_validation
                if not numeric_validation['is_valid']:
                    result['errors'].append(f"{field.replace('_', ' ').title()}: {numeric_validation['error']}")
        
        # Date validation
        if 'date' in data:
            date_validation = self._validate_date_field(data['date'])
            result['field_status']['date'] = date_validation
            if not date_validation['is_valid']:
                result['errors'].append(f"Date: {date_validation['error']}")
        
        # EE Name validation
        if 'ee_name' in data:
            ee_validation = self._validate_ee_name(data['ee_name'])
            result['field_status']['ee_name'] = ee_validation
            if not ee_validation['is_valid']:
                result['warnings'].append(f"EE Name: {ee_validation['error']}")
        
        return result
    
    def _validate_business_logic(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate business logic rules"""
        result = {'errors': [], 'warnings': []}
        
        try:
            # Earnest Money percentage validation
            if 'estimated_cost' in data and 'earnest_money' in data:
                estimated_cost = float(data['estimated_cost'])
                earnest_money = float(data['earnest_money'])
                
                if estimated_cost > 0:
                    em_percentage = (earnest_money / estimated_cost) * 100
                    
                    if em_percentage < 1:
                        result['warnings'].append(f"Earnest Money ({em_percentage:.2f}%) is below typical range (1-5%)")
                    elif em_percentage > 10:
                        result['warnings'].append(f"Earnest Money ({em_percentage:.2f}%) is above typical range (1-5%)")
            
            # Schedule Amount validation
            if 'estimated_cost' in data and 'schedule_amount' in data:
                estimated_cost = float(data['estimated_cost'])
                schedule_amount = float(data['schedule_amount'])
                
                if abs(schedule_amount - estimated_cost) > estimated_cost * 0.1:
                    result['warnings'].append("Schedule Amount differs significantly from Estimated Cost")
            
            # Time of completion reasonableness
            if 'time_of_completion' in data and 'estimated_cost' in data:
                months = int(data['time_of_completion'])
                cost = float(data['estimated_cost'])
                
                # Very rough heuristic: large projects should take more time
                if cost > 10000000 and months < 6:  # 1 Cr+ projects in less than 6 months
                    result['warnings'].append("Short completion time for large project - please verify")
                elif cost < 100000 and months > 12:  # Small projects taking more than a year
                    result['warnings'].append("Long completion time for small project - please verify")
        
        except (ValueError, TypeError) as e:
            result['warnings'].append(f"Could not validate business logic: {str(e)}")
        
        return result
    
    def _validate_single_bidder(self, bidder: Dict[str, Any], estimated_cost: float, bidder_num: int) -> Dict[str, Any]:
        """Validate a single bidder's data"""
        result = {
            'bidder_number': bidder_num,
            'is_valid': True,
            'errors': [],
            'warnings': [],
            'field_status': {}
        }
        
        # Required bidder fields
        for field in self.required_fields['bidder']:
            if field not in bidder or not bidder[field]:
                result['errors'].append(f"Bidder {bidder_num}: Missing {field}")
                result['is_valid'] = False
        
        # Bidder name validation
        if 'name' in bidder:
            name_validation = self._validate_bidder_name(bidder['name'])
            result['field_status']['name'] = name_validation
            if not name_validation['is_valid']:
                result['errors'].append(f"Bidder {bidder_num}: {name_validation['error']}")
                result['is_valid'] = False
        
        # Percentage validation
        if 'percentage' in bidder:
            pct_validation = self._validate_percentage(bidder['percentage'])
            result['field_status']['percentage'] = pct_validation
            if not pct_validation['is_valid']:
                result['errors'].append(f"Bidder {bidder_num}: {pct_validation['error']}")
                result['is_valid'] = False
            elif pct_validation.get('warning'):
                result['warnings'].append(f"Bidder {bidder_num}: {pct_validation['warning']}")
        
        # Contact validation (optional)
        if 'contact' in bidder and bidder['contact']:
            contact_validation = self._validate_contact(bidder['contact'])
            result['field_status']['contact'] = contact_validation
            if not contact_validation['is_valid']:
                result['warnings'].append(f"Bidder {bidder_num}: {contact_validation['error']}")
        
        # Bid amount validation (if provided)
        if 'bid_amount' in bidder:
            amount_validation = self._validate_bid_amount(bidder['bid_amount'], estimated_cost)
            result['field_status']['bid_amount'] = amount_validation
            if not amount_validation['is_valid']:
                result['errors'].append(f"Bidder {bidder_num}: {amount_validation['error']}")
                result['is_valid'] = False
        
        return result
    
    def _validate_cross_bidder_logic(self, bidders: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Validate cross-bidder business logic"""
        result = {'errors': [], 'warnings': []}
        
        try:
            # Check for duplicate bidder names
            names = [bidder.get('name', '').strip().lower() for bidder in bidders if bidder.get('name')]
            if len(names) != len(set(names)):
                result['errors'].append("Duplicate bidder names found")
            
            # Check bid spread (if bid amounts are available)
            bid_amounts = [bidder.get('bid_amount') for bidder in bidders if bidder.get('bid_amount')]
            if len(bid_amounts) > 1:
                min_bid = min(bid_amounts)
                max_bid = max(bid_amounts)
                spread = ((max_bid - min_bid) / min_bid) * 100
                
                if spread > 50:
                    result['warnings'].append(f"Large bid spread ({spread:.1f}%) - please verify bids")
                elif spread < 1:
                    result['warnings'].append("Very similar bid amounts - please verify")
            
            # Check percentage range
            percentages = [bidder.get('percentage') for bidder in bidders if bidder.get('percentage') is not None]
            if len(percentages) > 1:
                min_pct = min(percentages)
                max_pct = max(percentages)
                pct_range = max_pct - min_pct
                
                if pct_range > 30:
                    result['warnings'].append(f"Wide percentage range ({pct_range:.1f}%) in bids")
        
        except Exception as e:
            result['warnings'].append(f"Cross-bidder validation warning: {str(e)}")
        
        return result
    
    def _validate_nit_number(self, nit_number: str) -> Dict[str, Any]:
        """Validate NIT number format"""
        result = {'is_valid': True, 'error': '', 'cleaned_value': ''}
        
        try:
            if not nit_number or not isinstance(nit_number, str):
                result['is_valid'] = False
                result['error'] = "NIT number is required"
                return result
            
            cleaned = nit_number.strip()
            constraints = self.field_constraints['nit_number']
            
            if len(cleaned) < constraints['min_length']:
                result['is_valid'] = False
                result['error'] = f"NIT number too short (minimum {constraints['min_length']} characters)"
                return result
            
            if len(cleaned) > constraints['max_length']:
                result['is_valid'] = False
                result['error'] = f"NIT number too long (maximum {constraints['max_length']} characters)"
                return result
            
            # Check format patterns
            valid_patterns = [
                r'^\d+\/\d{4}-\d{2}$',  # 27/2024-25
                r'^\d+\/\d{4}$',        # 27/2024
                r'^NIT-\d+\/\d{4}$',    # NIT-27/2024
                r'^\d+-\d{4}$',         # 27-2024
                r'^[A-Z]+\d+\/\d{4}$',  # PWD27/2024
            ]
            
            is_valid_format = any(re.match(pattern, cleaned) for pattern in valid_patterns)
            
            if not is_valid_format:
                result['is_valid'] = False
                result['error'] = "Invalid NIT number format. Use formats like: 27/2024-25, NIT-27/2024"
                return result
            
            result['cleaned_value'] = cleaned
            return result
            
        except Exception as e:
            result['is_valid'] = False
            result['error'] = f"NIT validation error: {str(e)}"
            return result
    
    def _validate_work_name(self, work_name: str) -> Dict[str, Any]:
        """Validate work name"""
        result = {'is_valid': True, 'error': '', 'warning': '', 'cleaned_value': ''}
        
        try:
            if not work_name or not isinstance(work_name, str):
                result['is_valid'] = False
                result['error'] = "Work name is required"
                return result
            
            cleaned = work_name.strip()
            constraints = self.field_constraints['work_name']
            
            if len(cleaned) < constraints['min_length']:
                result['is_valid'] = False
                result['error'] = f"Work name too short (minimum {constraints['min_length']} characters)"
                return result
            
            if len(cleaned) > constraints['max_length']:
                result['is_valid'] = False
                result['error'] = f"Work name too long (maximum {constraints['max_length']} characters)"
                return result
            
            # Check for meaningful content
            meaningful_words = [
                'construction', 'repair', 'maintenance', 'building', 'road', 
                'bridge', 'work', 'project', 'development', 'installation', 
                'renovation', 'extension', 'electrical', 'plumbing', 'civil'
            ]
            
            cleaned_lower = cleaned.lower()
            has_meaningful_word = any(word in cleaned_lower for word in meaningful_words)
            word_count = len(cleaned.split())
            
            if not has_meaningful_word and word_count < 3:
                result['warning'] = "Work name may need more descriptive details"
            
            result['cleaned_value'] = cleaned
            return result
            
        except Exception as e:
            result['is_valid'] = False
            result['error'] = f"Work name validation error: {str(e)}"
            return result
    
    def _validate_numeric_field(self, value: Any, field_name: str) -> Dict[str, Any]:
        """Validate numeric fields"""
        result = {'is_valid': True, 'error': '', 'cleaned_value': None}
        
        try:
            if value is None or value == "":
                result['is_valid'] = False
                result['error'] = f"{field_name.replace('_', ' ').title()} is required"
                return result
            
            # Try to convert to appropriate type
            if field_name == 'time_of_completion':
                cleaned_value = int(float(value))
            else:
                cleaned_value = float(value)
            
            # Check constraints
            if field_name in self.field_constraints:
                constraints = self.field_constraints[field_name]
                
                if cleaned_value < constraints['min']:
                    result['is_valid'] = False
                    result['error'] = f"Value too low (minimum {constraints['min']})"
                    return result
                
                if cleaned_value > constraints['max']:
                    result['is_valid'] = False
                    result['error'] = f"Value too high (maximum {constraints['max']})"
                    return result
            
            result['cleaned_value'] = cleaned_value
            return result
            
        except (ValueError, TypeError):
            result['is_valid'] = False
            result['error'] = f"Must be a valid number"
            return result
    
    def _validate_percentage(self, percentage: Any) -> Dict[str, Any]:
        """Validate percentage field"""
        result = {'is_valid': True, 'error': '', 'warning': '', 'cleaned_value': None}
        
        try:
            if percentage is None or percentage == "":
                result['is_valid'] = False
                result['error'] = "Percentage is required"
                return result
            
            # Convert to float
            if isinstance(percentage, str):
                cleaned = percentage.replace('%', '').strip()
                pct_value = float(cleaned)
            else:
                pct_value = float(percentage)
            
            # Check constraints
            constraints = self.field_constraints['percentage']
            if pct_value < constraints['min'] or pct_value > constraints['max']:
                result['is_valid'] = False
                result['error'] = f"Percentage must be between {constraints['min']}% and {constraints['max']}%"
                return result
            
            # Warnings for unusual percentages
            if pct_value > 25:
                result['warning'] = "Very high percentage above estimate"
            elif pct_value < -25:
                result['warning'] = "Very low percentage below estimate"
            
            result['cleaned_value'] = pct_value
            return result
            
        except (ValueError, TypeError):
            result['is_valid'] = False
            result['error'] = "Percentage must be a valid number"
            return result
    
    def _validate_bidder_name(self, name: str) -> Dict[str, Any]:
        """Validate bidder name"""
        result = {'is_valid': True, 'error': '', 'cleaned_value': ''}
        
        try:
            if not name or not isinstance(name, str):
                result['is_valid'] = False
                result['error'] = "Bidder name is required"
                return result
            
            cleaned = name.strip()
            
            if len(cleaned) < 2:
                result['is_valid'] = False
                result['error'] = "Bidder name too short"
                return result
            
            if len(cleaned) > 100:
                result['is_valid'] = False
                result['error'] = "Bidder name too long"
                return result
            
            # Check for valid characters (letters, numbers, spaces, common business characters)
            if not re.match(r'^[a-zA-Z0-9\s\.\-\&\(\),]+$', cleaned):
                result['is_valid'] = False
                result['error'] = "Bidder name contains invalid characters"
                return result
            
            result['cleaned_value'] = cleaned
            return result
            
        except Exception as e:
            result['is_valid'] = False
            result['error'] = f"Name validation error: {str(e)}"
            return result
    
    def _validate_contact(self, contact: str) -> Dict[str, Any]:
        """Validate contact information"""
        result = {'is_valid': True, 'error': '', 'cleaned_value': ''}
        
        try:
            if not contact:
                result['is_valid'] = False
                result['error'] = "Contact information is required"
                return result
            
            cleaned = contact.strip()
            
            # Check if it's a phone number
            digits_only = re.sub(r'\D', '', cleaned)
            
            # Indian phone patterns
            phone_patterns = [
                r'^\d{10}$',      # 10 digits
                r'^91\d{10}$',    # +91 followed by 10 digits
                r'^\d{11}$',      # 11 digits (with STD code)
            ]
            
            is_phone = any(re.match(pattern, digits_only) for pattern in phone_patterns)
            
            # Check if it's an email
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            is_email = re.match(email_pattern, cleaned)
            
            if not is_phone and not is_email:
                result['is_valid'] = False
                result['error'] = "Contact must be a valid phone number or email"
                return result
            
            result['cleaned_value'] = cleaned
            return result
            
        except Exception as e:
            result['is_valid'] = False
            result['error'] = f"Contact validation error: {str(e)}"
            return result
    
    def _validate_bid_amount(self, bid_amount: Any, estimated_cost: float) -> Dict[str, Any]:
        """Validate bid amount"""
        result = {'is_valid': True, 'error': '', 'cleaned_value': None}
        
        try:
            if bid_amount is None or bid_amount == "":
                result['is_valid'] = False
                result['error'] = "Bid amount is required"
                return result
            
            amount = float(bid_amount)
            
            if amount <= 0:
                result['is_valid'] = False
                result['error'] = "Bid amount must be positive"
                return result
            
            # Check reasonableness against estimated cost
            if estimated_cost > 0:
                ratio = amount / estimated_cost
                if ratio > 2.0:  # More than 200% of estimate
                    result['is_valid'] = False
                    result['error'] = "Bid amount unreasonably high (>200% of estimate)"
                    return result
                elif ratio < 0.3:  # Less than 30% of estimate
                    result['is_valid'] = False
                    result['error'] = "Bid amount unreasonably low (<30% of estimate)"
                    return result
            
            result['cleaned_value'] = amount
            return result
            
        except (ValueError, TypeError):
            result['is_valid'] = False
            result['error'] = "Bid amount must be a valid number"
            return result
    
    def _validate_date_field(self, date_value: Any) -> Dict[str, Any]:
        """Validate date field"""
        result = {'is_valid': True, 'error': '', 'cleaned_value': ''}
        
        try:
            if not date_value:
                result['is_valid'] = False
                result['error'] = "Date is required"
                return result
            
            # Import here to avoid circular import
            from date_utils import DateUtils
            
            if isinstance(date_value, str):
                parsed_date = DateUtils.parse_date_string(date_value)
                if not parsed_date:
                    result['is_valid'] = False
                    result['error'] = "Invalid date format. Use DD-MM-YYYY"
                    return result
                
                # Check date reasonableness
                if not DateUtils.is_valid_tender_date(parsed_date):
                    result['is_valid'] = False
                    result['error'] = "Date is outside reasonable range for tender dates"
                    return result
                
                result['cleaned_value'] = DateUtils.format_date_statutory(parsed_date)
            else:
                result['cleaned_value'] = DateUtils.format_date_statutory(date_value)
            
            return result
            
        except Exception as e:
            result['is_valid'] = False
            result['error'] = f"Date validation error: {str(e)}"
            return result
    
    def _validate_ee_name(self, ee_name: str) -> Dict[str, Any]:
        """Validate Executive Engineer name"""
        result = {'is_valid': True, 'error': '', 'cleaned_value': ''}
        
        try:
            if not ee_name or not isinstance(ee_name, str):
                result['is_valid'] = False
                result['error'] = "Executive Engineer name is required"
                return result
            
            cleaned = ee_name.strip()
            
            if len(cleaned) < 3:
                result['is_valid'] = False
                result['error'] = "EE name too short"
                return result
            
            if cleaned.lower() == 'executive engineer':
                result['is_valid'] = False
                result['error'] = "Please provide actual EE name, not generic title"
                return result
            
            # Check for valid name characters
            if not re.match(r'^[a-zA-Z\s\.\-]+$', cleaned):
                result['is_valid'] = False
                result['error'] = "EE name contains invalid characters"
                return result
            
            result['cleaned_value'] = cleaned
            return result
            
        except Exception as e:
            result['is_valid'] = False
            result['error'] = f"EE name validation error: {str(e)}"
            return result
    
    def _generate_validation_summary(self, validation_result: Dict[str, Any]) -> Dict[str, Any]:
        """Generate validation summary"""
        return {
            'total_errors': len(validation_result['errors']),
            'total_warnings': len(validation_result['warnings']),
            'fields_validated': len(validation_result['field_status']),
            'is_complete': validation_result['is_valid'] and len(validation_result['warnings']) == 0
        }
    
    def _generate_bidder_validation_summary(self, validation_result: Dict[str, Any], bidders: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate bidder validation summary"""
        valid_bidders = sum(1 for status in validation_result['bidder_status'] if status['is_valid'])
        
        return {
            'total_bidders': len(bidders),
            'valid_bidders': valid_bidders,
            'total_errors': len(validation_result['errors']),
            'total_warnings': len(validation_result['warnings']),
            'all_valid': validation_result['is_valid']
        }

    def validate_file_upload(self, file_obj, allowed_extensions: List[str], max_size_mb: float = 10) -> Dict[str, Any]:
        """Validate uploaded file"""
        result = {'is_valid': True, 'error': '', 'warnings': []}
        
        try:
            if not file_obj:
                result['is_valid'] = False
                result['error'] = "No file uploaded"
                return result
            
            # Check file extension
            filename = getattr(file_obj, 'name', '')
            if filename:
                file_ext = filename.lower().split('.')[-1]
                if file_ext not in [ext.lower().lstrip('.') for ext in allowed_extensions]:
                    result['is_valid'] = False
                    result['error'] = f"Invalid file type. Allowed: {', '.join(allowed_extensions)}"
                    return result
            
            # Check file size
            if hasattr(file_obj, 'size'):
                size_mb = file_obj.size / (1024 * 1024)
                if size_mb > max_size_mb:
                    result['is_valid'] = False
                    result['error'] = f"File too large. Maximum size: {max_size_mb}MB"
                    return result
                elif size_mb > max_size_mb * 0.8:
                    result['warnings'].append("Large file size may affect processing speed")
            
            return result
            
        except Exception as e:
            result['is_valid'] = False
            result['error'] = f"File validation error: {str(e)}"
            return result

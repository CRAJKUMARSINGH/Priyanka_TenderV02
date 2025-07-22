import logging
from typing import Dict, Any, Optional, List
import re
try:
    import PyPDF2
    PDF_PARSER_AVAILABLE = True
except ImportError:
    PDF_PARSER_AVAILABLE = False

try:
    import fitz  # PyMuPDF
    PYMUPDF_AVAILABLE = True
except ImportError:
    PYMUPDF_AVAILABLE = False

logger = logging.getLogger(__name__)

class PDFParser:
    """Enhanced PDF parser for extracting tender data from PDF files"""
    
    def __init__(self):
        self.patterns = {
            'nit_number': r'(?:nit|tender)[\s:]*(?:no\.?|number)[\s:]*([A-Za-z0-9\/\-]+)',
            'estimated_cost': r'(?:estimate|estimated|cost)[\s:]*(?:rs\.?|\₹)?[\s]*([0-9,]+(?:\.[0-9]+)?)',
            'earnest_money': r'(?:earnest|em|security)[\s:]*(?:money|deposit)?[\s:]*(?:rs\.?|\₹)?[\s]*([0-9,]+(?:\.[0-9]+)?)',
            'time_of_completion': r'(?:completion|duration)[\s:]*(?:time|period)?[\s:]*([0-9]+)[\s]*(?:months?|days?)',
            'work_name': r'(?:work|project|construction)[\s:]*(.+?)(?:\n|estimate|cost|rs\.?|\₹)',
        }
    
    def parse_pdf(self, uploaded_file) -> Optional[Dict[str, Any]]:
        """Parse PDF file and extract tender information"""
        if not (PDF_PARSER_AVAILABLE or PYMUPDF_AVAILABLE):
            logger.error("No PDF parsing library available. Install PyPDF2 or PyMuPDF.")
            return None
        
        try:
            # Try different parsing methods
            text_content = self._extract_text(uploaded_file)
            
            if not text_content:
                logger.warning("No text content extracted from PDF")
                return None
            
            # Extract data using patterns
            extracted_data = self._extract_data_from_text(text_content)
            
            # Clean and validate extracted data
            cleaned_data = self._clean_extracted_data(extracted_data)
            
            if cleaned_data:
                logger.info("Successfully extracted data from PDF")
                return cleaned_data
            else:
                logger.warning("No valid data found in PDF")
                return None
                
        except Exception as e:
            logger.error(f"Error parsing PDF: {str(e)}")
            return None
    
    def _extract_text(self, uploaded_file) -> str:
        """Extract text from PDF using available libraries"""
        text_content = ""
        
        try:
            # Reset file pointer
            uploaded_file.seek(0)
            
            # Try PyMuPDF first (better text extraction)
            if PYMUPDF_AVAILABLE:
                text_content = self._extract_with_pymupdf(uploaded_file)
                if text_content:
                    return text_content
            
            # Fallback to PyPDF2
            if PDF_PARSER_AVAILABLE:
                uploaded_file.seek(0)
                text_content = self._extract_with_pypdf2(uploaded_file)
            
            return text_content
            
        except Exception as e:
            logger.error(f"Error extracting text from PDF: {str(e)}")
            return ""
    
    def _extract_with_pymupdf(self, uploaded_file) -> str:
        """Extract text using PyMuPDF (fitz)"""
        try:
            # Read file content
            file_content = uploaded_file.read()
            
            # Open PDF document
            pdf_document = fitz.open(stream=file_content, filetype="pdf")
            
            text_content = ""
            for page_num in range(pdf_document.page_count):
                page = pdf_document[page_num]
                text_content += page.get_text()
            
            pdf_document.close()
            return text_content
            
        except Exception as e:
            logger.error(f"Error with PyMuPDF extraction: {str(e)}")
            return ""
    
    def _extract_with_pypdf2(self, uploaded_file) -> str:
        """Extract text using PyPDF2"""
        try:
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            
            text_content = ""
            for page in pdf_reader.pages:
                text_content += page.extract_text()
            
            return text_content
            
        except Exception as e:
            logger.error(f"Error with PyPDF2 extraction: {str(e)}")
            return ""
    
    def _extract_data_from_text(self, text: str) -> Dict[str, Any]:
        """Extract structured data from text using regex patterns"""
        extracted_data = {}
        
        try:
            # Clean text for better pattern matching
            cleaned_text = self._clean_text(text)
            
            # Apply extraction patterns
            for field, pattern in self.patterns.items():
                matches = re.finditer(pattern, cleaned_text, re.IGNORECASE | re.MULTILINE)
                
                for match in matches:
                    if field not in extracted_data:
                        value = match.group(1).strip()
                        
                        # Special handling for different field types
                        if field in ['estimated_cost', 'earnest_money']:
                            value = self._extract_numeric_value(value)
                        elif field == 'time_of_completion':
                            value = self._extract_time_value(value)
                        elif field == 'work_name':
                            value = self._clean_work_name(value)
                        elif field == 'nit_number':
                            value = self._clean_nit_number(value)
                        
                        if value:
                            extracted_data[field] = value
                            break  # Take first valid match
            
            # Try to extract bidder information
            bidders = self._extract_bidders_from_text(cleaned_text)
            if bidders:
                extracted_data['bidders'] = bidders
            
            return extracted_data
            
        except Exception as e:
            logger.error(f"Error extracting data from text: {str(e)}")
            return {}
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize text for better extraction"""
        # Remove extra whitespace and normalize
        cleaned = re.sub(r'\s+', ' ', text)
        
        # Replace common variations
        replacements = {
            'Rs.': 'Rs',
            '₹': 'Rs',
            'Crore': '0000000',
            'Lakh': '00000',
            'Thousand': '000'
        }
        
        for old, new in replacements.items():
            cleaned = cleaned.replace(old, new)
        
        return cleaned
    
    def _extract_numeric_value(self, value: str) -> Optional[float]:
        """Extract numeric value from string"""
        try:
            # Remove commas and other formatting
            cleaned = re.sub(r'[,\s]', '', value)
            
            # Extract numbers
            numbers = re.findall(r'\d+(?:\.\d+)?', cleaned)
            if numbers:
                return float(numbers[0])
            
            return None
            
        except Exception as e:
            logger.warning(f"Could not extract numeric value from '{value}': {str(e)}")
            return None
    
    def _extract_time_value(self, value: str) -> Optional[int]:
        """Extract time value (months/days) from string"""
        try:
            # Extract first number
            numbers = re.findall(r'\d+', value)
            if numbers:
                time_value = int(numbers[0])
                
                # Convert days to months if needed
                if 'day' in value.lower() and time_value > 31:
                    time_value = max(1, time_value // 30)
                
                return time_value
            
            return None
            
        except Exception as e:
            logger.warning(f"Could not extract time value from '{value}': {str(e)}")
            return None
    
    def _clean_work_name(self, value: str) -> str:
        """Clean and format work name"""
        # Remove unwanted characters and extra spaces
        cleaned = re.sub(r'[^\w\s\-\.,]', ' ', value)
        cleaned = re.sub(r'\s+', ' ', cleaned).strip()
        
        # Capitalize properly
        if len(cleaned) > 10:  # Only if it's a reasonable length
            return cleaned
        
        return ""
    
    def _clean_nit_number(self, value: str) -> str:
        """Clean and format NIT number"""
        # Keep alphanumeric, slashes, and hyphens
        cleaned = re.sub(r'[^\w\-\/]', '', value)
        
        # Validate format (should have numbers and possibly year)
        if re.match(r'\d+\/\d{4}-?\d{0,2}', cleaned) or re.match(r'\d+\-\d{4}', cleaned):
            return cleaned
        
        return ""
    
    def _extract_bidders_from_text(self, text: str) -> List[Dict[str, Any]]:
        """Extract bidder information from text"""
        bidders = []
        
        try:
            # Look for tabular data with bidder names and amounts
            lines = text.split('\n')
            
            # Patterns for bidder information
            bidder_patterns = [
                r'(\w+\s+(?:company|contractors?|enterprises?|ltd|pvt))[^\d]*(\d+(?:\.\d+)?)[^\d]*([+-]?\d+(?:\.\d+)?)',
                r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)[^\d]*(\d+(?:,\d+)*)[^\d]*([+-]?\d+(?:\.\d+)?)',
            ]
            
            for line in lines:
                for pattern in bidder_patterns:
                    match = re.search(pattern, line, re.IGNORECASE)
                    if match:
                        name = match.group(1).strip()
                        amount = self._extract_numeric_value(match.group(2))
                        percentage = float(match.group(3)) if match.group(3) else 0
                        
                        if name and amount and len(name) > 2:
                            bidder = {
                                'name': name,
                                'bid_amount': amount,
                                'percentage': percentage
                            }
                            bidders.append(bidder)
                            
                            if len(bidders) >= 10:  # Limit to reasonable number
                                break
                
                if len(bidders) >= 10:
                    break
            
            return bidders
            
        except Exception as e:
            logger.error(f"Error extracting bidders: {str(e)}")
            return []
    
    def _clean_extracted_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Clean and validate extracted data"""
        cleaned_data = {}
        
        try:
            # Validate and clean each field
            if 'nit_number' in data and data['nit_number']:
                cleaned_data['nit_number'] = str(data['nit_number']).strip()
            
            if 'work_name' in data and data['work_name']:
                work_name = str(data['work_name']).strip()
                if len(work_name) > 10:  # Reasonable minimum length
                    cleaned_data['work_name'] = work_name
            
            if 'estimated_cost' in data and data['estimated_cost']:
                cost = data['estimated_cost']
                if isinstance(cost, (int, float)) and cost > 0:
                    cleaned_data['estimated_cost'] = float(cost)
            
            if 'earnest_money' in data and data['earnest_money']:
                em = data['earnest_money']
                if isinstance(em, (int, float)) and em >= 0:
                    cleaned_data['earnest_money'] = float(em)
            
            if 'time_of_completion' in data and data['time_of_completion']:
                time_val = data['time_of_completion']
                if isinstance(time_val, (int, float)) and 1 <= time_val <= 120:
                    cleaned_data['time_of_completion'] = int(time_val)
            
            if 'bidders' in data and data['bidders']:
                valid_bidders = []
                for bidder in data['bidders']:
                    if (bidder.get('name') and 
                        bidder.get('bid_amount') and 
                        isinstance(bidder['bid_amount'], (int, float)) and 
                        bidder['bid_amount'] > 0):
                        valid_bidders.append(bidder)
                
                if valid_bidders:
                    cleaned_data['bidders'] = valid_bidders
            
            return cleaned_data if cleaned_data else None
            
        except Exception as e:
            logger.error(f"Error cleaning extracted data: {str(e)}")
            return None
    
    def get_supported_formats(self) -> List[str]:
        """Get list of supported PDF parsing formats"""
        formats = []
        
        if PDF_PARSER_AVAILABLE:
            formats.append("PyPDF2")
        
        if PYMUPDF_AVAILABLE:
            formats.append("PyMuPDF")
        
        return formats if formats else ["None - Please install PyPDF2 or PyMuPDF"]

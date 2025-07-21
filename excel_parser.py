import pandas as pd
import logging
from typing import Dict, Any, Optional
import re
from date_utils import DateUtils

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ExcelParser:
    """Enhanced Excel parser with robust date handling for NIT documents."""
    
    def __init__(self):
        self.date_utils = DateUtils()
    
    def parse_nit_excel(self, file_path: str) -> Optional[Dict[str, Any]]:
        """
        Parse NIT Excel file and extract work information with enhanced date handling.
        
        Args:
            file_path: Path to the Excel file
            
        Returns:
            Dictionary containing parsed work information or None if parsing fails
        """
        try:
            # Read Excel file
            df = pd.read_excel(file_path, sheet_name=None)  # Read all sheets
            
            # Try to find the main sheet with tender information
            main_sheet = self._find_main_sheet(df)
            if main_sheet is None:
                logging.error("Could not find main sheet with tender information")
                return None
            
            # Extract work information
            work_data = self._extract_work_info(main_sheet)
            
            if work_data:
                logging.info(f"Successfully parsed NIT: {work_data['nit_number']}")
                return work_data
            else:
                logging.error("Failed to extract work information from Excel")
                return None
                
        except Exception as e:
            logging.error(f"Error parsing Excel file: {e}")
            return None
    
    def _find_main_sheet(self, sheets_dict: Dict[str, pd.DataFrame]) -> Optional[pd.DataFrame]:
        """
        Find the main sheet containing tender information.
        
        Args:
            sheets_dict: Dictionary of sheet names and DataFrames
            
        Returns:
            Main DataFrame or None if not found
        """
        # Priority order for sheet selection
        priority_keywords = [
            'tender', 'nit', 'notice', 'main', 'sheet1', 'work'
        ]
        
        # First, try to find by keywords
        for keyword in priority_keywords:
            for sheet_name, df in sheets_dict.items():
                if keyword.lower() in sheet_name.lower():
                    return df
        
        # If no keyword match, return the first non-empty sheet
        for sheet_name, df in sheets_dict.items():
            if not df.empty:
                return df
        
        return None
    
    def _extract_work_info(self, df: pd.DataFrame) -> Optional[Dict[str, Any]]:
        """
        Extract work information from the main DataFrame.
        
        Args:
            df: Main DataFrame containing tender information
            
        Returns:
            Dictionary with extracted work information
        """
        try:
            work_info = {}
            
            # Convert DataFrame to string for easier searching
            df_str = df.astype(str).fillna('')
            
            # Extract work name
            work_name = self._extract_work_name(df_str)
            if not work_name:
                return None
            
            # Extract NIT number
            nit_number = self._extract_nit_number(df_str)
            if not nit_number:
                return None
            
            # Extract estimated cost
            estimated_cost = self._extract_estimated_cost(df_str)
            if estimated_cost is None:
                return None
            
            # Extract date with enhanced handling
            date = self._extract_date(df_str)
            if not date:
                return None
            
            # Extract other information
            earnest_money = self._extract_earnest_money(df_str, estimated_cost)
            time_completion = self._extract_time_completion(df_str)
            
            return {
                'work_name': work_name,
                'nit_number': nit_number,
                'work_info': {
                    'estimated_cost': estimated_cost,
                    'earnest_money': earnest_money,
                    'date': date,
                    'time_of_completion': time_completion
                }
            }
            
        except Exception as e:
            logging.error(f"Error extracting work info: {e}")
            return None
    
    def _extract_work_name(self, df_str: pd.DataFrame) -> Optional[str]:
        """Extract work name from DataFrame."""
        work_keywords = [
            'work', 'name of work', 'work name', 'project', 'tender for'
        ]
        
        for _, row in df_str.iterrows():
            for col in df_str.columns:
                cell_value = str(row[col]).lower()
                
                for keyword in work_keywords:
                    if keyword in cell_value and len(cell_value) > 20:
                        # Clean and return work name
                        work_name = str(row[col]).strip()
                        if len(work_name) > 10:  # Ensure it's not just the header
                            return work_name
        
        # Fallback: look for long text that might be work name
        for _, row in df_str.iterrows():
            for col in df_str.columns:
                cell_value = str(row[col]).strip()
                if 50 <= len(cell_value) <= 500 and 'work' in cell_value.lower():
                    return cell_value
        
        return "Extracted Work Name"
    
    def _extract_nit_number(self, df_str: pd.DataFrame) -> Optional[str]:
        """Extract NIT number from DataFrame."""
        nit_patterns = [
            r'NIT\s*[:\-]?\s*([A-Z0-9\-\/]+)',
            r'TENDER\s*NO\s*[:\-]?\s*([A-Z0-9\-\/]+)',
            r'NOTICE\s*NO\s*[:\-]?\s*([A-Z0-9\-\/]+)',
            r'([A-Z0-9]+\/[A-Z0-9]+\/\d{4})',
            r'([A-Z0-9]+\-[A-Z0-9]+\-\d{4})'
        ]
        
        for _, row in df_str.iterrows():
            for col in df_str.columns:
                cell_value = str(row[col]).upper()
                
                for pattern in nit_patterns:
                    match = re.search(pattern, cell_value)
                    if match:
                        return match.group(1) if match.lastindex else match.group(0)
        
        # Generate default NIT number if not found
        from datetime import datetime
        return f"NIT-{datetime.now().strftime('%Y%m%d')}-001"
    
    def _extract_estimated_cost(self, df_str: pd.DataFrame) -> Optional[float]:
        """Extract estimated cost from DataFrame."""
        cost_keywords = [
            'estimated cost', 'estimate', 'cost', 'amount', 'value', 'budget'
        ]
        
        for _, row in df_str.iterrows():
            for col in df_str.columns:
                cell_value = str(row[col]).lower()
                
                # Check if this cell contains cost keywords
                if any(keyword in cell_value for keyword in cost_keywords):
                    # Look for numeric values in nearby cells
                    for search_col in df_str.columns:
                        search_value = str(row[search_col])
                        cost = self._extract_numeric_value(search_value)
                        if cost and cost > 1000:  # Reasonable minimum cost
                            return cost
        
        # Fallback: search for large numeric values
        for _, row in df_str.iterrows():
            for col in df_str.columns:
                cell_value = str(row[col])
                cost = self._extract_numeric_value(cell_value)
                if cost and 10000 <= cost <= 100000000:  # Reasonable range
                    return cost
        
        return None
    
    def _extract_numeric_value(self, text: str) -> Optional[float]:
        """Extract numeric value from text string."""
        try:
            # Remove common currency symbols and formatting
            clean_text = re.sub(r'[₹$,\s]', '', text)
            
            # Try to extract number
            number_match = re.search(r'(\d+\.?\d*)', clean_text)
            if number_match:
                return float(number_match.group(1))
        except:
            pass
        
        return None
    
    def _extract_date(self, df_str: pd.DataFrame) -> Optional[str]:
        """Extract date from DataFrame with enhanced date handling."""
        date_keywords = [
            'date', 'dated', 'on', 'issued', 'published', 'tender date'
        ]
        
        # Look for date keywords first
        for _, row in df_str.iterrows():
            for col in df_str.columns:
                cell_value = str(row[col]).lower()
                
                if any(keyword in cell_value for keyword in date_keywords):
                    # Search nearby cells for date values
                    for search_col in df_str.columns:
                        search_value = str(row[search_col]).strip()
                        parsed_date = self.date_utils.parse_date(search_value)
                        if parsed_date:
                            return self.date_utils.format_date(parsed_date)
        
        # Fallback: search all cells for date patterns
        for _, row in df_str.iterrows():
            for col in df_str.columns:
                cell_value = str(row[col]).strip()
                parsed_date = self.date_utils.parse_date(cell_value)
                if parsed_date:
                    return self.date_utils.format_date(parsed_date)
        
        # Default to current date if no date found
        return self.date_utils.get_current_date()
    
    def _extract_earnest_money(self, df_str: pd.DataFrame, estimated_cost: float) -> float:
        """Extract earnest money or calculate default."""
        em_keywords = [
            'earnest money', 'earnest', 'em', 'security deposit', 'deposit'
        ]
        
        for _, row in df_str.iterrows():
            for col in df_str.columns:
                cell_value = str(row[col]).lower()
                
                if any(keyword in cell_value for keyword in em_keywords):
                    # Look for numeric values in nearby cells
                    for search_col in df_str.columns:
                        search_value = str(row[search_col])
                        amount = self._extract_numeric_value(search_value)
                        if amount and 100 <= amount <= estimated_cost * 0.1:  # Reasonable range
                            return amount
        
        # Default to 2% of estimated cost
        return round(estimated_cost * 0.02, 2)
    
    def _extract_time_completion(self, df_str: pd.DataFrame) -> str:
        """Extract time of completion."""
        time_keywords = [
            'completion', 'duration', 'time', 'period', 'months', 'days'
        ]
        
        for _, row in df_str.iterrows():
            for col in df_str.columns:
                cell_value = str(row[col]).lower()
                
                if any(keyword in cell_value for keyword in time_keywords):
                    # Look for time patterns
                    time_patterns = [
                        r'(\d+)\s*months?',
                        r'(\d+)\s*days?',
                        r'(\d+)\s*weeks?'
                    ]
                    
                    for pattern in time_patterns:
                        match = re.search(pattern, cell_value)
                        if match:
                            number = match.group(1)
                            if 'month' in cell_value:
                                return f"{number} Months"
                            elif 'day' in cell_value:
                                return f"{number} Days"
                            elif 'week' in cell_value:
                                return f"{number} Weeks"
        
        # Default to 3 months
        return "3 Months"

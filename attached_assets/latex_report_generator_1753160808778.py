import os
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any
import re

logger = logging.getLogger(__name__)

class LatexReportGenerator:
    """Enhanced LaTeX report generator with exact template compliance"""
    
    def __init__(self):
        self.templates_dir = "templates"
        self.ensure_templates_exist()
    
    def ensure_templates_exist(self):
        """Ensure template directory exists"""
        os.makedirs(self.templates_dir, exist_ok=True)
    
    def generate_document(self, doc_type: str, work_data: Dict[str, Any]) -> Optional[str]:
        """Generate LaTeX content for specified document type"""
        try:
            template_path = os.path.join(self.templates_dir, f"{doc_type}.tex")
            
            if not os.path.exists(template_path):
                logger.error(f"Template not found: {template_path}")
                return None
            
            # Load template
            with open(template_path, 'r', encoding='utf-8') as f:
                template_content = f.read()
            
            # Prepare data for template
            template_data = self._prepare_template_data(work_data)
            
            # Process template with exact statutory format compliance
            latex_content = self._process_statutory_template(template_content, template_data)
            
            logger.info(f"Generated LaTeX content for {doc_type}")
            return latex_content
            
        except Exception as e:
            logger.error(f"Error generating {doc_type}: {str(e)}")
            return None
    
    def _prepare_template_data(self, work_data: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare and format data for template substitution with statutory compliance"""
        try:
            bidders = work_data.get('bidders', [])
            
            # Sort bidders by bid amount (lowest first)
            sorted_bidders = sorted(bidders, key=lambda x: x.get('bid_amount', float('inf')))
            
            # Find lowest bidder
            lowest_bidder = sorted_bidders[0] if sorted_bidders else None
            
            # Format currency amounts
            estimated_cost = work_data.get('estimated_cost', 0)
            earnest_money = work_data.get('earnest_money', 0)
            schedule_amount = work_data.get('schedule_amount', 0)
            
            # Calculate savings/excess
            if lowest_bidder:
                lowest_amount = lowest_bidder.get('bid_amount', 0)
                savings_amount = estimated_cost - lowest_amount
                savings_percentage = (savings_amount / estimated_cost * 100) if estimated_cost > 0 else 0
            else:
                lowest_amount = 0
                savings_amount = 0
                savings_percentage = 0
            
            # Format dates in DD-MM-YY format as per statutory requirement
            current_date = datetime.now().strftime('%d-%m-%y')
            tender_date = work_data.get('date', current_date)
            
            # Format receipt date (typically same day or next working day)
            receipt_date = work_data.get('receipt_date', tender_date)
            
            # Create bidder table rows exactly as per statutory format
            bidder_rows = []
            for i, bidder in enumerate(sorted_bidders, 1):
                percentage = bidder.get('percentage', 0)
                bid_amount = bidder.get('bid_amount', 0)
                
                # Format percentage display exactly as per statutory format
                if percentage > 0:
                    percentage_display = f"{percentage:.2f} ABOVE"
                elif percentage < 0:
                    percentage_display = f"{abs(percentage):.2f} BELOW"
                else:
                    percentage_display = "AT ESTIMATE"
                
                bidder_rows.append({
                    'serial': i,
                    'name': self._escape_latex(bidder.get('name', '')),
                    'estimated_cost': f"{int(estimated_cost)}",
                    'percentage': percentage_display,
                    'bid_amount': f"{int(bid_amount)}",
                    'contact': bidder.get('contact', '')
                })
            
            # Prepare lowest bidder percentage display
            if lowest_bidder:
                lowest_percentage = lowest_bidder.get('percentage', 0)
                if lowest_percentage > 0:
                    lowest_percentage_display = f"{lowest_percentage:.2f} ABOVE"
                elif lowest_percentage < 0:
                    lowest_percentage_display = f"{abs(lowest_percentage):.2f} BELOW"
                else:
                    lowest_percentage_display = "AT ESTIMATE"
            else:
                lowest_percentage_display = ""
            
            template_data = {
                # Basic information
                'nit_number': work_data.get('nit_number', ''),
                'work_name': self._escape_latex(work_data.get('work_name', '')),
                'estimated_cost': f"{int(estimated_cost)}",
                'estimated_cost_words': self._number_to_words(estimated_cost),
                'schedule_amount': f"{int(schedule_amount)}",
                'earnest_money': f"{int(earnest_money)}",
                'time_of_completion': work_data.get('time_of_completion', 12),
                'ee_name': self._escape_latex(work_data.get('ee_name', 'Executive Engineer')),
                
                # Dates in statutory format
                'tender_date': tender_date,
                'current_date': current_date,
                'calling_date': tender_date,
                'receipt_date': receipt_date,
                
                # Lowest bidder information
                'lowest_bidder_name': self._escape_latex(lowest_bidder.get('name', '') if lowest_bidder else ''),
                'lowest_bidder_amount': f"{int(lowest_amount)}" if lowest_bidder else '0',
                'lowest_bidder_amount_words': self._number_to_words(lowest_amount) if lowest_bidder else '',
                'lowest_bidder_percentage': lowest_bidder.get('percentage', 0) if lowest_bidder else 0,
                'lowest_bidder_percentage_display': lowest_percentage_display,
                
                # Financial calculations
                'savings_amount': f"{int(abs(savings_amount))}",
                'savings_percentage': f"{abs(savings_percentage):.2f}",
                
                # Bidder data
                'bidders': bidders,
                'sorted_bidders': sorted_bidders,
                'bidder_rows': bidder_rows,
                'total_bidders': len(bidders),
                
                # Additional statutory fields
                'office_name': 'OFFICE OF THE EXECUTIVE ENGINEER PWD ELECTRIC DIVISION, UDAIPUR',
                'department': 'PWD Electric Division',
                'location': 'Udaipur',
                'contingencies': 'As per rules',
                'item_number': '1',  # Default item number for statutory compliance
            }
            
            return template_data
            
        except Exception as e:
            logger.error(f"Error preparing template data: {str(e)}")
            return {}
    
    def _process_statutory_template(self, template_content: str, data: Dict[str, Any]) -> str:
        """Process template with exact statutory format compliance"""
        try:
            processed_content = template_content
            
            # Replace simple placeholders
            for key, value in data.items():
                if isinstance(value, (str, int, float)):
                    placeholder = f"{{{{{key}}}}}"
                    processed_content = processed_content.replace(placeholder, str(value))
            
            # Process bidder table rows with exact statutory format
            if '{{bidder_table_rows}}' in processed_content:
                bidder_rows = data.get('bidder_rows', [])
                table_rows = []
                
                for row in bidder_rows:
                    # Format exactly as per statutory requirement
                    latex_row = f"{row['serial']} & {row['name']} & {row['estimated_cost']} & {row['percentage']} & {row['bid_amount']} \\\\"
                    table_rows.append(latex_row)
                
                rows_content = '\n'.join(table_rows)
                processed_content = processed_content.replace('{{bidder_table_rows}}', rows_content)
            
            # Process any remaining template loops or conditionals
            processed_content = self._process_template_logic(processed_content, data)
            
            return processed_content
            
        except Exception as e:
            logger.error(f"Error processing statutory template: {str(e)}")
            return template_content
    
    def _process_template_logic(self, content: str, data: Dict[str, Any]) -> str:
        """Process template logic (loops, conditionals) for statutory compliance"""
        
        # Process each bidder loop for tables
        each_pattern = r'\{\{#each\s+(\w+)\}\}(.*?)\{\{/each\}\}'
        
        def replace_each(match):
            list_name = match.group(1)
            loop_content = match.group(2)
            
            if list_name == 'sorted_bidders':
                items = data.get('sorted_bidders', [])
                result_parts = []
                
                for i, item in enumerate(items):
                    item_content = loop_content
                    
                    # Replace item properties with proper escaping
                    item_content = item_content.replace('{{@index1}}', str(i + 1))
                    item_content = item_content.replace('{{name}}', self._escape_latex(item.get('name', '')))
                    item_content = item_content.replace('{{estimated_cost}}', str(int(data.get('estimated_cost', 0))))
                    
                    # Format percentage display
                    percentage = item.get('percentage', 0)
                    if percentage > 0:
                        percentage_display = f"{percentage:.2f} ABOVE"
                    elif percentage < 0:
                        percentage_display = f"{abs(percentage):.2f} BELOW"
                    else:
                        percentage_display = "AT ESTIMATE"
                    
                    item_content = item_content.replace('{{percentage_display}}', percentage_display)
                    item_content = item_content.replace('{{bid_amount}}', str(int(item.get('bid_amount', 0))))
                    
                    result_parts.append(item_content)
                
                return ''.join(result_parts)
            
            return match.group(0)  # Return unchanged if not handled
        
        content = re.sub(each_pattern, replace_each, content, flags=re.DOTALL)
        
        # Process conditionals
        if_pattern = r'\{\{#if\s+([^}]+)\}\}(.*?)(?:\{\{#else\}\}(.*?))?\{\{/if\}\}'
        
        def replace_conditional(match):
            condition = match.group(1).strip()
            if_content = match.group(2)
            else_content = match.group(3) if match.group(3) else ''
            
            # Evaluate condition
            condition_result = self._evaluate_condition(condition, data)
            
            return if_content if condition_result else else_content
        
        content = re.sub(if_pattern, replace_conditional, content, flags=re.DOTALL)
        
        return content
    
    def _evaluate_condition(self, condition: str, data: Dict[str, Any]) -> bool:
        """Evaluate condition for template logic"""
        try:
            # Handle percentage comparisons
            if 'percentage' in condition:
                if '>' in condition:
                    key, value = condition.split('>')
                    key = key.strip()
                    value = float(value.strip())
                    return data.get(key, 0) > value
                elif '<' in condition:
                    key, value = condition.split('<')
                    key = key.strip()
                    value = float(value.strip())
                    return data.get(key, 0) < value
            
            # Handle @first condition for first item in loop
            if condition == '@first':
                return True  # This would be handled in loop context
            
            # Simple existence check
            if condition in data:
                value = data[condition]
                return bool(value) and (value != 0 if isinstance(value, (int, float)) else True)
            
            return False
            
        except Exception as e:
            logger.error(f"Error evaluating condition '{condition}': {str(e)}")
            return False
    
    def _escape_latex(self, text: str) -> str:
        """Escape special LaTeX characters"""
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
        
        escaped = text
        for char, replacement in replacements.items():
            escaped = escaped.replace(char, replacement)
        
        return escaped
    
    def _number_to_words(self, number: float) -> str:
        """Convert number to words for Indian numbering system"""
        try:
            if number == 0:
                return "Zero"
            
            # Handle negative numbers
            if number < 0:
                return "Minus " + self._number_to_words(abs(number))
            
            # Convert to integer for word conversion
            num = int(number)
            
            # Define word mappings
            ones = ["", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine",
                   "Ten", "Eleven", "Twelve", "Thirteen", "Fourteen", "Fifteen", "Sixteen", 
                   "Seventeen", "Eighteen", "Nineteen"]
            
            tens = ["", "", "Twenty", "Thirty", "Forty", "Fifty", "Sixty", "Seventy", "Eighty", "Ninety"]
            
            def convert_hundred(n):
                result = ""
                if n >= 100:
                    result += ones[n // 100] + " Hundred "
                    n %= 100
                if n >= 20:
                    result += tens[n // 10] + " "
                    n %= 10
                if n > 0:
                    result += ones[n] + " "
                return result.strip()
            
            # Handle Indian numbering system (Crores, Lakhs, Thousands)
            result = ""
            
            if num >= 10000000:  # Crores
                crores = num // 10000000
                result += convert_hundred(crores) + " Crore "
                num %= 10000000
            
            if num >= 100000:  # Lakhs
                lakhs = num // 100000
                result += convert_hundred(lakhs) + " Lakh "
                num %= 100000
            
            if num >= 1000:  # Thousands
                thousands = num // 1000
                result += convert_hundred(thousands) + " Thousand "
                num %= 1000
            
            if num > 0:
                result += convert_hundred(num)
            
            # Add "Rupees Only" suffix
            result = result.strip()
            if result:
                result += " Rupees Only"
            
            return result
            
        except Exception as e:
            logger.error(f"Error converting number to words: {str(e)}")
            return f"{int(number)} Rupees Only"

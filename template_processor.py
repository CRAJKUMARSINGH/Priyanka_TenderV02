import os
import logging
from typing import Dict, Any, Optional
import re
from datetime import datetime

logger = logging.getLogger(__name__)

class TemplateProcessor:
    """Process LaTeX templates with enhanced data mapping for statutory compliance"""
    
    def __init__(self):
        self.templates_dir = "templates"
        self.ensure_templates()
    
    def ensure_templates(self):
        """Ensure templates directory exists and create statutory compliant templates"""
        os.makedirs(self.templates_dir, exist_ok=True)
        
        # Create statutory compliant templates based on attached assets
        statutory_templates = {
            "comparative_statement.tex": self._get_statutory_comparative_statement(),
            "letter_of_acceptance.tex": self._get_statutory_letter_of_acceptance(),
            "scrutiny_sheet.tex": self._get_statutory_scrutiny_sheet(),
            "work_order.tex": self._get_statutory_work_order()
        }
        
        for template_name, content in statutory_templates.items():
            template_path = os.path.join(self.templates_dir, template_name)
            if not os.path.exists(template_path):
                try:
                    with open(template_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    logger.info(f"Created statutory compliant template: {template_name}")
                except Exception as e:
                    logger.error(f"Error creating template {template_name}: {str(e)}")
    
    def process_template(self, template_type: str, latex_content: str, work_data: Dict[str, Any]) -> str:
        """Process template with statutory compliance and enhanced data mapping"""
        try:
            # Validate input data
            if not work_data:
                logger.error("No work data provided")
                return latex_content
            
            # Enhanced data processing for statutory compliance
            processed_data = self._enhance_work_data_statutory(work_data)
            
            # Process content with statutory substitution
            processed_content = self._statutory_substitution(latex_content, processed_data)
            
            # Ensure LaTeX compliance and statutory formatting
            processed_content = self._ensure_statutory_compliance(processed_content)
            
            logger.info(f"Statutory template processing completed for {template_type}")
            return processed_content
            
        except Exception as e:
            logger.error(f"Error processing statutory template {template_type}: {str(e)}")
            return latex_content
    
    def _enhance_work_data_statutory(self, work_data: Dict[str, Any]) -> Dict[str, Any]:
        """Enhance work data with statutory format compliance"""
        enhanced_data = work_data.copy()
        
        try:
            # Enhanced bidder processing for statutory format
            bidders = work_data.get('bidders', [])
            if bidders:
                # Sort bidders by amount (lowest first)
                sorted_bidders = sorted(bidders, key=lambda x: x.get('bid_amount', float('inf')))
                enhanced_data['sorted_bidders'] = sorted_bidders
                enhanced_data['lowest_bidder'] = sorted_bidders[0] if sorted_bidders else None
                
                # Process each bidder with statutory format
                for i, bidder in enumerate(sorted_bidders):
                    percentage = bidder.get('percentage', 0)
                    
                    # Format percentage as per statutory requirement
                    if percentage > 0:
                        bidder['percentage_display'] = f"{percentage:.2f} ABOVE"
                    elif percentage < 0:
                        bidder['percentage_display'] = f"{abs(percentage):.2f} BELOW"
                    else:
                        bidder['percentage_display'] = "AT ESTIMATE"
                    
                    bidder['serial_number'] = i + 1
                    bidder['formatted_amount'] = f"{int(bidder.get('bid_amount', 0))}"
            
            # Date processing for statutory format (DD-MM-YY)
            current_date = datetime.now()
            enhanced_data['current_date_statutory'] = current_date.strftime('%d-%m-%y')
            enhanced_data['current_date_full'] = current_date.strftime('%d-%m-%Y')
            
            # Financial calculations with statutory formatting
            estimated_cost = enhanced_data.get('estimated_cost', 0)
            if enhanced_data.get('lowest_bidder'):
                lowest_amount = enhanced_data['lowest_bidder'].get('bid_amount', 0)
                savings = estimated_cost - lowest_amount
                enhanced_data['absolute_savings'] = abs(savings)
                enhanced_data['savings_percentage'] = (abs(savings) / estimated_cost * 100) if estimated_cost > 0 else 0
                enhanced_data['is_saving'] = savings > 0
                
                # Format lowest bidder percentage for statutory display
                lowest_percentage = enhanced_data['lowest_bidder'].get('percentage', 0)
                if lowest_percentage > 0:
                    enhanced_data['lowest_bidder_percentage_display'] = f"{lowest_percentage:.2f} ABOVE"
                elif lowest_percentage < 0:
                    enhanced_data['lowest_bidder_percentage_display'] = f"{abs(lowest_percentage):.2f} BELOW"
                else:
                    enhanced_data['lowest_bidder_percentage_display'] = "AT ESTIMATE"
            
            # Statutory required fields
            enhanced_data['office_header'] = 'OFFICE OF THE EXECUTIVE ENGINEER PWD ELECTRIC DIVISION, UDAIPUR'
            enhanced_data['document_title'] = 'COMPARATIVE STATEMENT OF TENDERS'
            enhanced_data['item_number'] = 'ITEM-1'
            enhanced_data['contingencies_note'] = 'As per rules'
            enhanced_data['nil_amount'] = 'Nil'
            
            # Format amounts as integers (no decimals) as per statutory format
            for key in ['estimated_cost', 'earnest_money', 'schedule_amount']:
                if key in enhanced_data and enhanced_data[key]:
                    enhanced_data[f'{key}_formatted'] = f"{int(enhanced_data[key])}"
            
            return enhanced_data
            
        except Exception as e:
            logger.error(f"Error enhancing work data for statutory compliance: {str(e)}")
            return work_data
    
    def _statutory_substitution(self, content: str, data: Dict[str, Any]) -> str:
        """Advanced template substitution with statutory compliance"""
        try:
            processed_content = content
            
            # Process bidder table generation
            processed_content = self._process_bidder_tables(processed_content, data)
            
            # Process simple substitutions with proper formatting
            processed_content = self._process_statutory_substitutions(processed_content, data)
            
            # Process conditionals and loops
            processed_content = self._process_template_conditionals(processed_content, data)
            
            return processed_content
            
        except Exception as e:
            logger.error(f"Error in statutory substitution: {str(e)}")
            return content
    
    def _process_bidder_tables(self, content: str, data: Dict[str, Any]) -> str:
        """Process bidder table generation with exact statutory format"""
        
        # Generate bidder table rows
        if '{{bidder_table_rows}}' in content:
            sorted_bidders = data.get('sorted_bidders', [])
            estimated_cost = data.get('estimated_cost', 0)
            
            table_rows = []
            for i, bidder in enumerate(sorted_bidders, 1):
                name = self._escape_latex(bidder.get('name', ''))
                percentage_display = bidder.get('percentage_display', 'AT ESTIMATE')
                bid_amount = int(bidder.get('bid_amount', 0))
                
                # Format row exactly as per statutory requirement
                row = f"{i} & {name} & {int(estimated_cost)} & {percentage_display} & {bid_amount} \\\\"
                table_rows.append(row)
            
            table_content = '\n'.join(table_rows)
            content = content.replace('{{bidder_table_rows}}', table_content)
        
        return content
    
    def _process_statutory_substitutions(self, content: str, data: Dict[str, Any]) -> str:
        """Process simple substitutions with statutory formatting"""
        
        # Define statutory format substitutions
        substitutions = {
            'nit_number': data.get('nit_number', ''),
            'work_name': self._escape_latex(data.get('work_name', '')),
            'estimated_cost': f"{int(data.get('estimated_cost', 0))}",
            'earnest_money': f"{int(data.get('earnest_money', 0))}",
            'time_of_completion': str(data.get('time_of_completion', 12)),
            'tender_date': data.get('date', data.get('current_date_statutory', '')),
            'receipt_date': data.get('date', data.get('current_date_statutory', '')),
            'ee_name': self._escape_latex(data.get('ee_name', 'Executive Engineer')),
            'current_date': data.get('current_date_statutory', ''),
            'office_header': 'OFFICE OF THE EXECUTIVE ENGINEER PWD ELECTRIC DIVISION, UDAIPUR',
            'document_title': 'COMPARATIVE STATEMENT OF TENDERS',
            'item_number': 'ITEM-1',
            'contingencies_note': 'As per rules',
            'nil_amount': 'Nil'
        }
        
        # Add lowest bidder information
        lowest_bidder = data.get('lowest_bidder')
        if lowest_bidder:
            substitutions.update({
                'lowest_bidder_name': self._escape_latex(lowest_bidder.get('name', '')),
                'lowest_bidder_amount': f"{int(lowest_bidder.get('bid_amount', 0))}",
                'lowest_bidder_percentage_display': data.get('lowest_bidder_percentage_display', ''),
                'lowest_bidder_amount_words': self._number_to_words_statutory(lowest_bidder.get('bid_amount', 0))
            })
        
        # Apply substitutions
        for key, value in substitutions.items():
            placeholder = f"{{{{{key}}}}}"
            content = content.replace(placeholder, str(value))
        
        return content
    
    def _process_template_conditionals(self, content: str, data: Dict[str, Any]) -> str:
        """Process conditional logic in templates"""
        
        # Process each loops for bidders
        each_pattern = r'\{\{#each\s+(\w+)\}\}(.*?)\{\{/each\}\}'
        
        def replace_each(match):
            list_name = match.group(1)
            loop_content = match.group(2)
            
            if list_name == 'sorted_bidders':
                bidders = data.get('sorted_bidders', [])
                result = []
                
                for i, bidder in enumerate(bidders):
                    item_content = loop_content
                    
                    # Replace bidder-specific placeholders
                    replacements = {
                        '{{@index1}}': str(i + 1),
                        '{{name}}': self._escape_latex(bidder.get('name', '')),
                        '{{estimated_cost}}': f"{int(data.get('estimated_cost', 0))}",
                        '{{percentage_display}}': bidder.get('percentage_display', 'AT ESTIMATE'),
                        '{{bid_amount}}': f"{int(bidder.get('bid_amount', 0))}"
                    }
                    
                    for placeholder, value in replacements.items():
                        item_content = item_content.replace(placeholder, value)
                    
                    result.append(item_content)
                
                return ''.join(result)
            
            return match.group(0)
        
        content = re.sub(each_pattern, replace_each, content, flags=re.DOTALL)
        
        # Process if/else conditionals
        if_pattern = r'\{\{#if\s+([^}]+)\}\}(.*?)(?:\{\{#else\}\}(.*?))?\{\{/if\}\}'
        
        def replace_if(match):
            condition = match.group(1).strip()
            if_content = match.group(2)
            else_content = match.group(3) if match.group(3) else ''
            
            # Evaluate condition
            if self._evaluate_condition(condition, data):
                return if_content
            else:
                return else_content
        
        content = re.sub(if_pattern, replace_if, content, flags=re.DOTALL)
        
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
            
            # Simple existence check
            if condition in data:
                value = data[condition]
                return bool(value) and (value != 0 if isinstance(value, (int, float)) else True)
            
            return False
            
        except Exception as e:
            logger.error(f"Error evaluating condition '{condition}': {str(e)}")
            return False
    
    def _ensure_statutory_compliance(self, content: str) -> str:
        """Ensure LaTeX content meets statutory compliance requirements"""
        try:
            # Ensure proper document structure
            if not content.strip().startswith('\\documentclass'):
                content = "\\documentclass[12pt,a4paper]{article}\n" + content
            
            # Ensure required packages for statutory format
            required_packages = [
                "\\usepackage[utf8]{inputenc}",
                "\\usepackage[T1]{fontenc}",
                "\\usepackage{geometry}",
                "\\usepackage{array}",
                "\\usepackage{longtable}",
                "\\usepackage{booktabs}"
            ]
            
            for package in required_packages:
                if package not in content:
                    content = content.replace("\\documentclass", f"{package}\n\\documentclass", 1)
            
            return content
            
        except Exception as e:
            logger.error(f"Error ensuring statutory compliance: {str(e)}")
            return content
    
    def _escape_latex(self, text: str) -> str:
        """Escape special LaTeX characters"""
        if not text:
            return ""
        
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
    
    def _number_to_words_statutory(self, number: float) -> str:
        """Convert number to words in statutory format"""
        try:
            if number == 0:
                return "Zero Rupees Only"
            
            # Convert to integer for statutory format
            num = int(number)
            
            # Basic number to words conversion for statutory documents
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
            
            # Handle Indian numbering system
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
            
            result = result.strip()
            if result:
                result += " Rupees Only"
            
            return result
            
        except Exception as e:
            logger.error(f"Error converting number to words: {str(e)}")
            return f"{int(number)} Rupees Only"
    
    def _get_statutory_comparative_statement(self) -> str:
        """Get statutory compliant comparative statement template"""
        return """\\documentclass[12pt,a4paper]{article}
\\usepackage[utf8]{inputenc}
\\usepackage[T1]{fontenc}
\\usepackage{geometry}
\\usepackage{array}
\\usepackage{longtable}
\\usepackage{booktabs}
\\usepackage{fancyhdr}

\\geometry{margin=2cm}
\\pagestyle{fancy}

\\begin{document}

\\begin{center}
\\textbf{{{office_header}}}\\\\[0.3cm]
\\textbf{{{document_title}}}\\\\[0.2cm]
\\end{center}

\\vspace{0.5cm}

\\noindent
\\textbf{NIT No.:} {{nit_number}} \\hfill \\textbf{Date:} {{current_date}}\\\\
\\textbf{Work:} {{work_name}}\\\\
\\textbf{Estimated Cost:} Rs. {{estimated_cost}}\\\\
\\textbf{Earnest Money:} Rs. {{earnest_money}}\\\\
\\textbf{Time of Completion:} {{time_of_completion}} months

\\vspace{0.5cm}

\\begin{longtable}{|c|p{4cm}|c|c|c|}
\\hline
\\textbf{S.No.} & \\textbf{Name of Bidder} & \\textbf{Estimated Cost} & \\textbf{Percentage} & \\textbf{Bid Amount} \\\\
\\hline
{{bidder_table_rows}}
\\hline
\\end{longtable}

\\vspace{0.5cm}

\\noindent
\\textbf{Lowest Bidder:} {{lowest_bidder_name}}\\\\
\\textbf{Lowest Amount:} Rs. {{lowest_bidder_amount}} ({{lowest_bidder_percentage_display}})\\\\
\\textbf{Amount in Words:} {{lowest_bidder_amount_words}}

\\vspace{1cm}

\\noindent
\\textbf{Executive Engineer}\\\\
\\textbf{PWD Electric Division, Udaipur}

\\end{document}"""
    
    def _get_statutory_letter_of_acceptance(self) -> str:
        """Get statutory compliant letter of acceptance template"""
        return """\\documentclass[12pt,a4paper]{article}
\\usepackage[utf8]{inputenc}
\\usepackage[T1]{fontenc}
\\usepackage{geometry}
\\usepackage{fancyhdr}

\\geometry{margin=2cm}
\\pagestyle{fancy}

\\begin{document}

\\begin{center}
\\textbf{{{office_header}}}\\\\[0.3cm]
\\textbf{LETTER OF ACCEPTANCE}\\\\[0.2cm]
\\end{center}

\\vspace{0.5cm}

\\noindent
No. {{nit_number}} \\hfill Date: {{current_date}}

\\vspace{0.5cm}

\\noindent
To,\\\\
{{lowest_bidder_name}}

\\vspace{0.3cm}

\\noindent
Subject: Acceptance of tender for {{work_name}}

\\vspace{0.3cm}

\\noindent
Sir,

\\vspace{0.3cm}

\\noindent
Your tender dated {{tender_date}} for the work "{{work_name}}" for Rs. {{lowest_bidder_amount}} ({{lowest_bidder_amount_words}}) i.e., {{lowest_bidder_percentage_display}} the estimated cost is hereby accepted.

\\vspace{0.3cm}

\\noindent
You are requested to execute the agreement within 15 days from the date of issue of this letter and commence the work immediately.

\\vspace{0.3cm}

\\noindent
The work should be completed within {{time_of_completion}} months from the date of commencement.

\\vspace{1cm}

\\noindent
\\hfill {{ee_name}}\\\\
\\hfill Executive Engineer\\\\
\\hfill PWD Electric Division, Udaipur

\\end{document}"""
    
    def _get_statutory_scrutiny_sheet(self) -> str:
        """Get statutory compliant scrutiny sheet template"""
        return """\\documentclass[12pt,a4paper]{article}
\\usepackage[utf8]{inputenc}
\\usepackage[T1]{fontenc}
\\usepackage{geometry}
\\usepackage{array}
\\usepackage{longtable}
\\usepackage{booktabs}

\\geometry{margin=2cm}

\\begin{document}

\\begin{center}
\\textbf{{{office_header}}}\\\\[0.3cm]
\\textbf{TENDER SCRUTINY SHEET}\\\\[0.2cm]
\\end{center}

\\vspace{0.5cm}

\\noindent
\\textbf{NIT No.:} {{nit_number}} \\hfill \\textbf{Date:} {{current_date}}\\\\
\\textbf{Work:} {{work_name}}\\\\
\\textbf{Estimated Cost:} Rs. {{estimated_cost}}

\\vspace{0.5cm}

\\begin{longtable}{|c|p{3cm}|c|c|c|p{2cm}|}
\\hline
\\textbf{S.No.} & \\textbf{Bidder Name} & \\textbf{Bid Amount} & \\textbf{Technical} & \\textbf{Financial} & \\textbf{Remarks} \\\\
\\hline
{{#each sorted_bidders}}
{{@index1}} & {{name}} & {{bid_amount}} & Qualified & Qualified & {{#if @first}}Lowest{{/if}} \\\\
\\hline
{{/each}}
\\end{longtable}

\\vspace{0.5cm}

\\noindent
\\textbf{Recommendation:} {{lowest_bidder_name}} is recommended for award of work being the lowest technically and financially qualified bidder.

\\vspace{1cm}

\\noindent
\\textbf{{{ee_name}}}\\\\
\\textbf{Executive Engineer}\\\\
\\textbf{PWD Electric Division, Udaipur}

\\end{document}"""
    
    def _get_statutory_work_order(self) -> str:
        """Get statutory compliant work order template"""
        return """\\documentclass[12pt,a4paper]{article}
\\usepackage[utf8]{inputenc}
\\usepackage[T1]{fontenc}
\\usepackage{geometry}
\\usepackage{fancyhdr}

\\geometry{margin=2cm}
\\pagestyle{fancy}

\\begin{document}

\\begin{center}
\\textbf{{{office_header}}}\\\\[0.3cm]
\\textbf{WORK ORDER}\\\\[0.2cm]
\\end{center}

\\vspace{0.5cm}

\\noindent
Work Order No. {{nit_number}}/WO \\hfill Date: {{current_date}}

\\vspace{0.5cm}

\\noindent
To,\\\\
{{lowest_bidder_name}}

\\vspace{0.3cm}

\\noindent
Subject: Work Order for {{work_name}}

\\vspace{0.3cm}

\\noindent
Sir,

\\vspace{0.3cm}

\\noindent
You are hereby directed to execute the work "{{work_name}}" for a contract amount of Rs. {{lowest_bidder_amount}} ({{lowest_bidder_amount_words}}) as per the terms and conditions of the tender and agreement.

\\vspace{0.3cm}

\\noindent
\\textbf{Work Details:}
\\begin{itemize}
\\item Contract Amount: Rs. {{lowest_bidder_amount}}
\\item Time of Completion: {{time_of_completion}} months
\\item Earnest Money: Rs. {{earnest_money}}
\\item Commencement Date: {{current_date}}
\\end{itemize}

\\vspace{0.3cm}

\\noindent
The work shall be executed as per specifications, drawings, and conditions of contract. Any deviation from the approved plans requires prior written approval.

\\vspace{1cm}

\\noindent
\\hfill {{ee_name}}\\\\
\\hfill Executive Engineer\\\\
\\hfill PWD Electric Division, Udaipur

\\end{document}"""

from datetime import datetime, timedelta
from typing import Dict, Any, List
import logging
from date_utils import DateUtils

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class LetterAcceptanceGenerator:
    """Generates official PWD format Letter of Acceptance with enhanced date handling."""
    
    def __init__(self):
        self.date_utils = DateUtils()
        self.portrait_style = """
        <style>
            @page { 
                size: A4 portrait; 
                margin: 20mm; 
            }
            body {
                font-family: 'Arial', Arial, sans-serif;
                font-size: 11px;
                line-height: 1.4;
                margin: 0;
                padding: 0;
                color: black;
            }
            .header {
                text-align: center;
                font-weight: bold;
                font-size: 12px;
                margin-bottom: 20px;
            }
            .office-header {
                text-align: center;
                font-weight: bold;
                font-size: 12px;
                margin-bottom: 10px;
                border-bottom: 1px solid black;
                padding-bottom: 5px;
            }
            .content {
                text-align: justify;
                margin: 20px 0;
                line-height: 1.6;
            }
            .details-table {
                width: 100%;
                border-collapse: collapse;
                margin: 15px 0;
            }
            .details-table td {
                padding: 5px;
                border: none;
                vertical-align: top;
            }
            .details-table .label {
                width: 200px;
                font-weight: bold;
            }
            .signature-section {
                margin-top: 40px;
                text-align: right;
            }
        </style>
        """
    
    def generate_letter_of_acceptance(self, work: Dict[str, Any], bidders: List[Dict[str, Any]]) -> str:
        """Generate official PWD Letter of Acceptance format with enhanced date handling."""
        
        # Sort bidders by bid amount (lowest first)
        sorted_bidders = sorted(bidders, key=lambda x: x['bid_amount'])
        lowest_bidder = sorted_bidders[0]
        
        # Get work details
        work_name = work['work_name']
        nit_number = work['nit_number']
        work_info = work['work_info']
        estimated_cost = float(work_info['estimated_cost'])
        earnest_money = work_info['earnest_money']
        time_completion = work_info['time_of_completion']
        
        # Enhanced date parsing and calculation
        original_date = work_info['date']
        parsed_date = self.date_utils.parse_date(original_date)
        
        if not parsed_date:
            logging.warning(f"Could not parse date '{original_date}', using current date")
            parsed_date = datetime.now()
        
        # Format the original date for display
        formatted_date = self.date_utils.format_display_date(parsed_date)
        
        # Calculate project timeline
        try:
            timeline = self._calculate_project_timeline(parsed_date, time_completion)
        except Exception as e:
            logging.error(f"Error calculating timeline: {e}")
            # Use fallback timeline
            timeline = {
                'commencement_date': self.date_utils.format_display_date(self.date_utils.add_days(parsed_date, 1)),
                'completion_date': self.date_utils.format_display_date(self.date_utils.add_months(parsed_date, 3))
            }
        
        # Format amount in words
        amount_words = self._amount_to_words(lowest_bidder['bid_amount'])
        
        # Calculate performance security (3% of contract value)
        performance_security = int(lowest_bidder['bid_amount'] * 0.03)
        
        # Generate current timestamp
        current_timestamp = self.date_utils.get_current_date()
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Letter of Acceptance - {nit_number}</title>
            {self.portrait_style}
        </head>
        <body>
            <div class="office-header">
                OFFICE OF THE EXECUTIVE ENGINEER PWD ELECTRIC DIVISION UDAIPUR
            </div>
            
            <div style="margin: 15px 0;">
                No.- {nit_number}/LOA/{datetime.now().year}<br>
                Date- {formatted_date}<br>
            </div>
            
            <div class="content">
                <div style="text-align: center; font-weight: bold; margin: 20px 0; font-size: 14px;">
                    LETTER OF ACCEPTANCE
                </div>
                
                <p>To,</p>
                <p style="margin-left: 20px;">
                    <strong>{lowest_bidder['name']}</strong><br>
                    [Complete Address with Pin Code]<br>
                    [Phone/Mobile Number]<br>
                    [Email ID]
                </p>
                
                <p>Subject: <strong>Acceptance of tender for "{work_name}"</strong></p>
                
                <p>Sir,</p>
                
                <p>I am pleased to inform you that your tender dated <strong>{formatted_date}</strong> 
                for the above mentioned work has been accepted by the competent authority.</p>
                
                <table class="details-table">
                    <tr>
                        <td class="label">Name of Work:</td>
                        <td>{work_name}</td>
                    </tr>
                    <tr>
                        <td class="label">NIT Number:</td>
                        <td>{nit_number}</td>
                    </tr>
                    <tr>
                        <td class="label">NIT Date:</td>
                        <td>{formatted_date}</td>
                    </tr>
                    <tr>
                        <td class="label">Estimated Cost:</td>
                        <td>Rs. {estimated_cost:,.0f}/-</td>
                    </tr>
                    <tr>
                        <td class="label">Your Tendered Amount:</td>
                        <td>Rs. {lowest_bidder['bid_amount']:,.0f}/- (Rupees {amount_words} Only)</td>
                    </tr>
                    <tr>
                        <td class="label">Percentage:</td>
                        <td>{lowest_bidder['percentage']:+.2f}% {'below' if lowest_bidder['percentage'] < 0 else 'above'} estimate</td>
                    </tr>
                    <tr>
                        <td class="label">Earnest Money:</td>
                        <td>Rs. {earnest_money}/-</td>
                    </tr>
                    <tr>
                        <td class="label">Performance Security:</td>
                        <td>Rs. {performance_security:,.0f}/- (3% of contract value)</td>
                    </tr>
                    <tr>
                        <td class="label">Time of Completion:</td>
                        <td>{time_completion}</td>
                    </tr>
                    <tr>
                        <td class="label">Commencement Date:</td>
                        <td>{timeline['commencement_date']}</td>
                    </tr>
                    <tr>
                        <td class="label">Completion Date:</td>
                        <td>{timeline['completion_date']}</td>
                    </tr>
                </table>
                
                <p>You are requested to:</p>
                <ol>
                    <li>Submit the Performance Security of Rs. {performance_security:,.0f}/- within 15 days from the date of this letter.</li>
                    <li>Execute the agreement within 21 days from the date of this letter.</li>
                    <li>Commence the work as per the scheduled date mentioned above.</li>
                    <li>Complete the work within the stipulated time period.</li>
                </ol>
                
                <p>The acceptance is subject to the following conditions:</p>
                <ol>
                    <li>All terms and conditions mentioned in the tender document shall be binding.</li>
                    <li>The work shall be executed as per approved drawings and specifications.</li>
                    <li>Any deviation from the approved plans will require prior written approval.</li>
                    <li>The contractor shall be responsible for the quality of work and materials.</li>
                    <li>Payment will be made as per the terms specified in the tender document.</li>
                </ol>
                
                <p>Congratulations on being awarded this contract. We look forward to your cooperation 
                for timely and quality completion of the work.</p>
                
                <p>Yours faithfully,</p>
            </div>
            
            <div class="signature-section">
                <p style="margin-top: 40px;">
                    <strong>Executive Engineer</strong><br>
                    PWD Electric Division<br>
                    Udaipur<br>
                    On behalf of the Governor of Rajasthan
                </p>
            </div>
            
            <div style="margin-top: 30px; font-size: 10px;">
                Copy to:<br>
                1. The Accountant General, Rajasthan, Jaipur<br>
                2. The Superintending Engineer, PWD Electric Circle, Udaipur<br>
                3. The Assistant Engineer concerned for information and necessary action<br>
                4. Office file<br><br>
                
                <div style="text-align: right;">
                    <strong>Executive Engineer</strong><br>
                    PWD Electric Division<br>
                    Udaipur
                </div>
            </div>
            
            <div style="margin-top: 20px; font-size: 9px; text-align: center; color: #666;">
                Letter of Acceptance generated on {current_timestamp}
            </div>
        </body>
        </html>
        """
        
        return html_content
    
    def _calculate_project_timeline(self, start_date: datetime, time_completion: str) -> Dict[str, str]:
        """
        Calculate project timeline dates with enhanced error handling.
        
        Args:
            start_date: Project start date
            time_completion: Time completion string (e.g., "3 Months")
            
        Returns:
            Dictionary with formatted timeline dates
        """
        try:
            # Commencement date is the next day after start date
            commencement_date = self.date_utils.add_days(start_date, 1)
            
            # Calculate completion date based on time_completion
            completion_date = self.date_utils.calculate_completion_date(commencement_date, time_completion)
            
            return {
                'commencement_date': self.date_utils.format_display_date(commencement_date),
                'completion_date': self.date_utils.format_display_date(completion_date)
            }
            
        except Exception as e:
            logging.error(f"Error in timeline calculation: {e}")
            # Fallback to default 3 months
            commencement_date = self.date_utils.add_days(start_date, 1)
            completion_date = self.date_utils.add_months(commencement_date, 3)
            
            return {
                'commencement_date': self.date_utils.format_display_date(commencement_date),
                'completion_date': self.date_utils.format_display_date(completion_date)
            }
    
    def _amount_to_words(self, amount: float) -> str:
        """Convert amount to words in Indian format with error handling."""
        try:
            amount = int(amount)
            
            # Simple conversion for common amounts
            if amount < 100000:  # Less than 1 lakh
                thousands = amount // 1000
                hundreds = (amount % 1000) // 100
                remainder = amount % 100
                
                words = []
                if thousands > 0:
                    words.append(f"{thousands} Thousand")
                if hundreds > 0:
                    words.append(f"{hundreds} Hundred")
                if remainder > 0:
                    words.append(str(remainder))
                
                return " ".join(words) if words else "Zero"
            
            elif amount < 10000000:  # Less than 1 crore
                lakhs = amount // 100000
                remainder = amount % 100000
                
                words = [f"{lakhs} Lakh"]
                if remainder >= 1000:
                    thousands = remainder // 1000
                    words.append(f"{thousands} Thousand")
                    remainder = remainder % 1000
                if remainder > 0:
                    words.append(str(remainder))
                
                return " ".join(words)
            
            else:
                crores = amount // 10000000
                remainder = amount % 10000000
                
                words = [f"{crores} Crore"]
                if remainder >= 100000:
                    lakhs = remainder // 100000
                    words.append(f"{lakhs} Lakh")
                    remainder = remainder % 100000
                if remainder >= 1000:
                    thousands = remainder // 1000
                    words.append(f"{thousands} Thousand")
                    remainder = remainder % 1000
                if remainder > 0:
                    words.append(str(remainder))
                
                return " ".join(words)
                
        except Exception as e:
            logging.error(f"Error converting amount to words: {e}")
            return f"{amount:,.0f}"

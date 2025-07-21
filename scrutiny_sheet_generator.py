from datetime import datetime
from typing import Dict, Any, List
import logging
from date_utils import DateUtils

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ScrutinySheetGenerator:
    """Generates official PWD format scrutiny sheet with enhanced date handling."""
    
    def __init__(self):
        self.date_utils = DateUtils()
        self.portrait_style = """
        <style>
            @page { 
                size: A4 portrait; 
                margin: 15mm; 
            }
            body {
                font-family: 'Arial', Arial, sans-serif;
                font-size: 14px;
                line-height: 1.4;
                margin: 0;
                padding: 0;
                color: black;
            }
            .header {
                text-align: center;
                font-weight: bold;
                font-size: 18px;
                margin-bottom: 20px;
                border: 2px solid black;
                padding: 8px;
            }
            .main-table {
                width: 100%;
                border-collapse: collapse;
                border: 3px solid black;
                margin: 10px 0;
            }
            .main-table td, .main-table th {
                border: 2px solid black;
                padding: 8px 10px;
                font-size: 14px;
                vertical-align: top;
                text-align: left;
            }
            .main-table td:first-child {
                width: 5%;
                text-align: center;
                font-weight: bold;
                padding: 8px 5px;
            }
            .main-table td:nth-child(2) {
                width: 35%;
                font-weight: bold;
                padding: 8px 10px;
            }
            .main-table td:last-child {
                width: 60%;
                padding: 8px 10px;
            }
            .main-table tr {
                height: 20px;
            }
            .signature-section {
                text-align: center;
                font-weight: bold;
                font-size: 16px;
                margin-top: 30px;
                padding: 20px;
                border: 2px solid black;
            }
        </style>
        """
    
    def generate_scrutiny_sheet(self, work: Dict[str, Any], bidders: List[Dict[str, Any]]) -> str:
        """Generate official PWD scrutiny sheet format with enhanced date handling."""
        
        try:
            # Sort bidders by bid amount (lowest first)
            sorted_bidders = sorted(bidders, key=lambda x: x['bid_amount'])
            lowest_bidder = sorted_bidders[0]
            
            # Get work details
            work_name = work['work_name']
            nit_number = work['nit_number']
            work_info = work['work_info']
            estimated_cost = float(work_info['estimated_cost'])
            
            # Enhanced date parsing and handling
            original_date = work_info['date']
            parsed_date = self.date_utils.parse_date(original_date)
            
            if not parsed_date:
                logging.warning(f"Could not parse date '{original_date}', using current date")
                parsed_date = datetime.now()
            
            # Format dates for display
            formatted_date = self.date_utils.format_display_date(parsed_date)
            
            # Calculate dates (assuming some standard dates for calling and receipt)
            calling_date = formatted_date
            receipt_date = formatted_date
            
            # Calculate validity dates (20 days from current date)
            validity_date = self.date_utils.add_days(datetime.now(), 20)
            validity_date_str = self.date_utils.format_display_date(validity_date)
            
            # Generate current timestamp
            current_timestamp = self.date_utils.get_current_date()
            
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <title>Scrutiny Sheet - {nit_number}</title>
                {self.portrait_style}
            </head>
            <body>
                <div class="header">
                    <u>Scrutiny Sheet of Tender</u>
                </div>
                
                <table class="main-table">
                    <tr>
                        <td>1</td>
                        <td>Head of Account</td>
                        <td>PWD Electric Works</td>
                    </tr>
                    <tr>
                        <td>2</td>
                        <td>Name of work</td>
                        <td>{work_name}<br>Job No. {nit_number}</td>
                    </tr>
                    <tr>
                        <td>3</td>
                        <td>Reference of ADM. Sanction<br>Amount in Rs.</td>
                        <td>As per administrative approval<br>Rs. {estimated_cost:.0f}/-</td>
                    </tr>
                    <tr>
                        <td>4</td>
                        <td>Reference of technical sanction with amount</td>
                        <td>As per technical sanction for Rs. {estimated_cost:.0f}/-</td>
                    </tr>
                    <tr>
                        <td>5</td>
                        <td>Date of calling NIT</td>
                        <td>{calling_date}</td>
                    </tr>
                    <tr>
                        <td>6</td>
                        <td>Date of receipt of tender</td>
                        <td>{receipt_date}</td>
                    </tr>
                    <tr>
                        <td>7</td>
                        <td>Number of tenders received</td>
                        <td>{len(bidders)}</td>
                    </tr>
                    <tr>
                        <td>8</td>
                        <td>Date of opening of tender</td>
                        <td>{formatted_date}</td>
                    </tr>
                    <tr>
                        <td>9</td>
                        <td>Allotment of fund during the current financial year</td>
                        <td>Adequate.</td>
                    </tr>
                    <tr>
                        <td>10</td>
                        <td>Expenditure up to last bill</td>
                        <td>Nil.</td>
                    </tr>
                    <tr>
                        <td>11</td>
                        <td>Lowest rate quoted and condition if any</td>
                        <td>{lowest_bidder['name']}<br>Rs. {lowest_bidder['bid_amount']:,.0f}/- ({lowest_bidder['percentage']:+.2f}% {'below' if lowest_bidder['percentage'] < 0 else 'above'} estimate)</td>
                    </tr>
                    <tr>
                        <td>12</td>
                        <td>Financial implication of condition if any in tender</td>
                        <td>Not Applicable.</td>
                    </tr>
                    <tr>
                        <td>13</td>
                        <td>Name of lowest contractor</td>
                        <td>{lowest_bidder['name']}</td>
                    </tr>
                    <tr>
                        <td>14</td>
                        <td>Authority competent to sanction the tender</td>
                        <td>The Executive Engineer</td>
                    </tr>
                    <tr>
                        <td>15</td>
                        <td>Validity of tender<br>Valid Upto Dated</td>
                        <td>20 Days<br>{validity_date_str}</td>
                    </tr>
                    <tr>
                        <td>16</td>
                        <td>Remarks if any</td>
                        <td>All documents verified and found in order. Recommended for acceptance.</td>
                    </tr>
                </table>
                
                <div class="signature-section">
                    EXECUTIVE ENGINEER<br>
                    PWD ELECTRIC DIVISION<br>
                    UDAIPUR
                </div>
                
                <div style="margin-top: 20px; font-size: 10px; text-align: center; color: #666;">
                    Scrutiny Sheet generated on {current_timestamp}
                </div>
            </body>
            </html>
            """
            
            return html_content
            
        except Exception as e:
            logging.error(f"Error generating scrutiny sheet: {e}")
            raise

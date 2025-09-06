from datetime import datetime
from typing import Dict, Any, List
import logging
from date_utils import DateUtils

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ComparativeStatementGenerator:
    """Generates official PWD format comparative statement with enhanced date handling."""
    
    def __init__(self):
        self.date_utils = DateUtils()
        self.landscape_style = """
        <style>
            @page { 
                size: A4 landscape; 
                margin: 15mm; 
            }
            body {
                font-family: 'Arial', Arial, sans-serif;
                font-size: 10px;
                line-height: 1.3;
                margin: 0;
                padding: 0;
                color: black;
            }
            .header {
                text-align: center;
                font-weight: bold;
                font-size: 12px;
                margin-bottom: 15px;
            }
            .office-header {
                text-align: center;
                font-weight: bold;
                font-size: 11px;
                margin-bottom: 10px;
                border-bottom: 1px solid black;
                padding-bottom: 5px;
            }
            .work-details {
                margin: 10px 0;
                font-size: 10px;
            }
            .main-table {
                width: 100%;
                border-collapse: collapse;
                border: 3px solid black;
                margin: 10px 0;
            }
            .main-table td, .main-table th {
                border: 2px solid black;
                padding: 6px 4px;
                font-size: 9px;
                vertical-align: middle;
                text-align: center;
            }
            .main-table th {
                background-color: #f0f0f0;
                font-weight: bold;
                font-size: 9px;
            }
            .main-table .bidder-name {
                text-align: left;
                max-width: 120px;
                word-wrap: break-word;
            }
            .main-table .amount {
                text-align: right;
                font-weight: bold;
            }
            .main-table .percentage {
                font-weight: bold;
            }
            .l1-row {
                background-color: #e8f5e8;
                font-weight: bold;
            }
            .signature-section {
                margin-top: 20px;
                display: flex;
                justify-content: space-between;
            }
            .signature-box {
                text-align: center;
                font-size: 9px;
                border: 2px solid black;
                padding: 15px;
                width: 150px;
                height: 60px;
            }
        </style>
        """
    
    def generate_comparative_statement(self, work: Dict[str, Any], bidders: List[Dict[str, Any]]) -> str:
        """Generate official PWD comparative statement format with enhanced date handling."""
        
        # Sort bidders by bid amount (lowest first)
        sorted_bidders = sorted(bidders, key=lambda x: x['bid_amount'])
        
        # Get work details with enhanced date parsing
        work_name = work['work_name']
        nit_number = work['nit_number']
        work_info = work['work_info']
        estimated_cost = float(work_info['estimated_cost'])
        earnest_money = work_info['earnest_money']
        time_completion = work_info['time_of_completion']
        
        # Parse and format date with fallback handling
        original_date = work_info['date']
        parsed_date = self.date_utils.parse_date(original_date)
        if parsed_date:
            formatted_date = self.date_utils.format_display_date(parsed_date)
        else:
            formatted_date = original_date
            logging.warning(f"Could not parse date '{original_date}', using original format")
        
        # Generate current timestamp for the report
        current_timestamp = self.date_utils.get_current_date()
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Comparative Statement - {nit_number}</title>
            {self.landscape_style}
        </head>
        <body>
            <div class="office-header">
                OFFICE OF THE EXECUTIVE ENGINEER PWD ELECTRIC DIVISION UDAIPUR
            </div>
            
            <div class="header">
                <u>COMPARATIVE STATEMENT OF TENDER</u>
            </div>
            
            <div class="work-details">
                <strong>Name of Work:</strong> {work_name}<br>
                <strong>NIT No.:</strong> {nit_number} &nbsp;&nbsp;&nbsp;&nbsp; <strong>Date:</strong> {formatted_date}<br>
                <strong>Estimated Cost:</strong> Rs. {estimated_cost:,.0f}/- &nbsp;&nbsp;&nbsp;&nbsp; 
                <strong>Earnest Money:</strong> Rs. {earnest_money} &nbsp;&nbsp;&nbsp;&nbsp;
                <strong>Time of Completion:</strong> {time_completion}
            </div>
            
            <table class="main-table">
                <thead>
                    <tr>
                        <th rowspan="2" style="width: 8%;">S.No.</th>
                        <th rowspan="2" style="width: 30%;">Name of Bidders</th>
                        <th colspan="2" style="width: 30%;">Rate Quoted</th>
                        <th rowspan="2" style="width: 20%;">Tendered Amount<br>(Rs.)</th>
                        <th rowspan="2" style="width: 20%;">Remarks</th>
                    </tr>
                    <tr>
                        <th style="width: 12%;">% Above/Below</th>
                        <th style="width: 13%;">Amount (Rs.)</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td><strong>E</strong></td>
                        <td class="bidder-name"><strong>ESTIMATED COST</strong></td>
                        <td class="percentage">-</td>
                        <td class="amount"><strong>{estimated_cost:,.0f}</strong></td>
                        <td class="amount"><strong>{estimated_cost:,.0f}</strong></td>
                        <td>-</td>
                    </tr>
        """
        
        # Add bidder rows
        for i, bidder in enumerate(sorted_bidders):
            serial_no = i + 1
            row_class = "l1-row" if i == 0 else ""
            rank_text = "L1" if i == 0 else f"L{serial_no}"
            
            # Format percentage with proper sign
            percentage_str = f"{bidder['percentage']:+.2f}%"
            
            html_content += f"""
                    <tr class="{row_class}">
                        <td><strong>{serial_no}</strong></td>
                        <td class="bidder-name">{bidder['name']}</td>
                        <td class="percentage">{percentage_str}</td>
                        <td class="amount">{bidder['bid_amount']:,.0f}</td>
                        <td class="amount">{bidder['bid_amount']:,.0f}</td>
                        <td>{rank_text}</td>
                    </tr>
            """
        
        # Calculate statistics
        if sorted_bidders:
            lowest_bid = sorted_bidders[0]['bid_amount']
            savings = estimated_cost - lowest_bid
            savings_percentage = (savings / estimated_cost) * 100
        else:
            lowest_bid = 0
            savings = 0
            savings_percentage = 0
        
        html_content += f"""
                </tbody>
            </table>
            
            <div style="margin: 15px 0; font-size: 10px;">
                <strong>Summary:</strong><br>
                Lowest Bidder: {sorted_bidders[0]['name'] if sorted_bidders else 'N/A'}<br>
                Lowest Bid Amount: Rs. {lowest_bid:,.0f}/-<br>
                Cost Savings: Rs. {savings:,.0f}/- ({savings_percentage:.2f}% below estimate)<br>
                Total Bidders: {len(sorted_bidders)}<br>
                Report Generated: {current_timestamp}
            </div>
            
            <div class="signature-section">
                <div class="signature-box">
                    <div style="height: 40px;"></div>
                    <div style="border-top: 1px solid black; padding-top: 5px;">
                        <strong>JUNIOR ENGINEER</strong>
                    </div>
                </div>
                
                <div class="signature-box">
                    <div style="height: 40px;"></div>
                    <div style="border-top: 1px solid black; padding-top: 5px;">
                        <strong>ASSISTANT ENGINEER</strong>
                    </div>
                </div>
                
                <div class="signature-box">
                    <div style="height: 40px;"></div>
                    <div style="border-top: 1px solid black; padding-top: 5px;">
                        <strong>EXECUTIVE ENGINEER</strong>
                    </div>
                </div>
            </div>
            
            <div style="margin-top: 20px; font-size: 9px; text-align: center;">
                <strong>PWD ELECTRIC DIVISION UDAIPUR</strong><br>
                Comparative Statement generated on {current_timestamp}
            </div>
        </body>
        </html>
        """
        
        return html_content

import logging
from typing import Dict, Any, List
from datetime import datetime
from date_utils import DateUtils

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ReportGenerator:
    """Enhanced report generator with improved date handling and formatting."""
    
    def __init__(self):
        self.date_utils = DateUtils()
    
    def generate_detailed_report(self, work: Dict[str, Any], bidders: List[Dict[str, Any]]) -> str:
        """
        Generate comprehensive detailed report with enhanced formatting.
        
        Args:
            work: Work information dictionary
            bidders: List of bidder dictionaries
            
        Returns:
            HTML report content
        """
        try:
            # Sort bidders by bid amount
            sorted_bidders = sorted(bidders, key=lambda x: x['bid_amount'])
            
            # Get work details with date parsing
            work_name = work['work_name']
            nit_number = work['nit_number']
            work_info = work['work_info']
            estimated_cost = float(work_info['estimated_cost'])
            earnest_money = work_info['earnest_money']
            time_completion = work_info['time_of_completion']
            
            # Parse and format date
            parsed_date = self.date_utils.parse_date(work_info['date'])
            formatted_date = self.date_utils.format_display_date(parsed_date) if parsed_date else work_info['date']
            
            # Calculate statistics
            stats = self._calculate_report_statistics(sorted_bidders, estimated_cost)
            
            # Generate report timestamp
            report_timestamp = self.date_utils.get_current_date()
            
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <title>Detailed Tender Report - {nit_number}</title>
                <style>
                    {self._get_report_styles()}
                </style>
            </head>
            <body>
                <div class="header">
                    <h1>🏗️ Detailed Tender Report</h1>
                    <p class="subtitle">PWD Electric Division - Government Engineering Office</p>
                </div>
                
                <div class="work-summary">
                    <h2>📋 Work Summary</h2>
                    <div class="info-grid">
                        <div class="info-item">
                            <label>Work Name:</label>
                            <span>{work_name}</span>
                        </div>
                        <div class="info-item">
                            <label>NIT Number:</label>
                            <span>{nit_number}</span>
                        </div>
                        <div class="info-item">
                            <label>Date:</label>
                            <span>{formatted_date}</span>
                        </div>
                        <div class="info-item">
                            <label>Estimated Cost:</label>
                            <span>₹{estimated_cost:,.2f}</span>
                        </div>
                        <div class="info-item">
                            <label>Earnest Money:</label>
                            <span>₹{earnest_money}</span>
                        </div>
                        <div class="info-item">
                            <label>Time of Completion:</label>
                            <span>{time_completion}</span>
                        </div>
                    </div>
                </div>
                
                <div class="statistics">
                    <h2>📊 Tender Statistics</h2>
                    <div class="stats-grid">
                        <div class="stat-card">
                            <div class="stat-value">{stats['total_bidders']}</div>
                            <div class="stat-label">Total Bidders</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-value">₹{stats['lowest_bid']:,.0f}</div>
                            <div class="stat-label">Lowest Bid</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-value">₹{stats['highest_bid']:,.0f}</div>
                            <div class="stat-label">Highest Bid</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-value">{stats['avg_percentage']:+.2f}%</div>
                            <div class="stat-label">Average Percentage</div>
                        </div>
                    </div>
                </div>
                
                <div class="bidders-section">
                    <h2>👥 Bidder Analysis</h2>
                    <table class="bidders-table">
                        <thead>
                            <tr>
                                <th>Rank</th>
                                <th>Bidder Name</th>
                                <th>Percentage (%)</th>
                                <th>Bid Amount (₹)</th>
                                <th>Difference from Estimate</th>
                                <th>Status</th>
                            </tr>
                        </thead>
                        <tbody>
            """
            
            # Add bidder rows
            for i, bidder in enumerate(sorted_bidders):
                rank = i + 1
                difference = bidder['bid_amount'] - estimated_cost
                status = "🥇 L1 (Lowest)" if rank == 1 else f"L{rank}"
                status_class = "l1" if rank == 1 else "other"
                
                html_content += f"""
                            <tr class="bidder-row {status_class}">
                                <td class="rank">{rank}</td>
                                <td class="bidder-name">{bidder['name']}</td>
                                <td class="percentage">{bidder['percentage']:+.2f}%</td>
                                <td class="bid-amount">₹{bidder['bid_amount']:,.2f}</td>
                                <td class="difference">₹{difference:+,.2f}</td>
                                <td class="status">{status}</td>
                            </tr>
                """
            
            html_content += f"""
                        </tbody>
                    </table>
                </div>
                
                <div class="recommendations">
                    <h2>💡 Recommendations</h2>
                    <div class="recommendation-box">
                        <p><strong>Lowest Bidder:</strong> {sorted_bidders[0]['name']}</p>
                        <p><strong>Recommended Action:</strong> Proceed with technical evaluation of L1 bidder</p>
                        <p><strong>Cost Saving:</strong> ₹{estimated_cost - sorted_bidders[0]['bid_amount']:,.2f} 
                           ({abs(sorted_bidders[0]['percentage']):.2f}% below estimate)</p>
                    </div>
                </div>
                
                <div class="footer">
                    <p>Report generated on: {report_timestamp}</p>
                    <p>PWD Electric Division Tender Processing System v2.1.0</p>
                </div>
            </body>
            </html>
            """
            
            return html_content
            
        except Exception as e:
            logging.error(f"Error generating detailed report: {e}")
            raise
    
    def _calculate_report_statistics(self, bidders: List[Dict[str, Any]], estimated_cost: float) -> Dict[str, Any]:
        """Calculate statistics for the report."""
        if not bidders:
            return {
                'total_bidders': 0,
                'lowest_bid': 0,
                'highest_bid': 0,
                'avg_percentage': 0,
                'cost_savings': 0
            }
        
        bid_amounts = [bidder['bid_amount'] for bidder in bidders]
        percentages = [bidder['percentage'] for bidder in bidders]
        
        return {
            'total_bidders': len(bidders),
            'lowest_bid': min(bid_amounts),
            'highest_bid': max(bid_amounts),
            'avg_percentage': sum(percentages) / len(percentages),
            'cost_savings': estimated_cost - min(bid_amounts)
        }
    
    def _get_report_styles(self) -> str:
        """Get CSS styles for the report."""
        return """
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: 'Arial', sans-serif;
                line-height: 1.6;
                color: #333;
                background-color: #f8f9fa;
                padding: 20px;
            }
            
            .header {
                text-align: center;
                background: linear-gradient(135deg, #1f77b4, #2c3e50);
                color: white;
                padding: 30px;
                border-radius: 12px;
                margin-bottom: 30px;
                box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            }
            
            .header h1 {
                font-size: 2.5em;
                margin-bottom: 10px;
            }
            
            .subtitle {
                font-size: 1.2em;
                opacity: 0.9;
            }
            
            .work-summary, .statistics, .bidders-section, .recommendations {
                background: white;
                padding: 25px;
                border-radius: 12px;
                margin-bottom: 25px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            
            h2 {
                color: #2c3e50;
                font-size: 1.8em;
                margin-bottom: 20px;
                border-bottom: 3px solid #1f77b4;
                padding-bottom: 10px;
            }
            
            .info-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 15px;
            }
            
            .info-item {
                display: flex;
                justify-content: space-between;
                padding: 12px;
                background: #f8f9fa;
                border-radius: 8px;
                border-left: 4px solid #1f77b4;
            }
            
            .info-item label {
                font-weight: bold;
                color: #495057;
            }
            
            .info-item span {
                font-weight: 600;
                color: #2c3e50;
            }
            
            .stats-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 20px;
            }
            
            .stat-card {
                text-align: center;
                padding: 20px;
                background: linear-gradient(135deg, #667eea, #764ba2);
                color: white;
                border-radius: 12px;
                box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            }
            
            .stat-value {
                font-size: 2em;
                font-weight: bold;
                margin-bottom: 5px;
            }
            
            .stat-label {
                font-size: 0.9em;
                opacity: 0.9;
            }
            
            .bidders-table {
                width: 100%;
                border-collapse: collapse;
                margin-top: 15px;
                background: white;
                border-radius: 8px;
                overflow: hidden;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            
            .bidders-table th {
                background: linear-gradient(135deg, #343a40, #495057);
                color: white;
                padding: 15px 12px;
                text-align: center;
                font-weight: bold;
            }
            
            .bidders-table td {
                padding: 12px;
                text-align: center;
                border-bottom: 1px solid #dee2e6;
            }
            
            .bidder-row.l1 {
                background: linear-gradient(135deg, #d4edda, #c3e6cb);
                font-weight: bold;
            }
            
            .bidder-row:hover {
                background: #f8f9fa;
            }
            
            .rank {
                font-weight: bold;
                color: #1f77b4;
            }
            
            .bidder-name {
                text-align: left;
                font-weight: 600;
            }
            
            .percentage {
                font-weight: bold;
            }
            
            .bid-amount {
                font-weight: bold;
                color: #28a745;
            }
            
            .difference {
                font-weight: bold;
            }
            
            .status {
                font-weight: bold;
                color: #dc3545;
            }
            
            .recommendation-box {
                background: linear-gradient(135deg, #fff3cd, #ffeaa7);
                padding: 20px;
                border-radius: 8px;
                border-left: 4px solid #ffc107;
            }
            
            .recommendation-box p {
                margin-bottom: 10px;
                font-weight: 500;
            }
            
            .footer {
                text-align: center;
                padding: 20px;
                background: #6c757d;
                color: white;
                border-radius: 8px;
                margin-top: 30px;
            }
            
            @media print {
                body {
                    background: white;
                    padding: 0;
                }
                
                .header, .work-summary, .statistics, .bidders-section, .recommendations {
                    box-shadow: none;
                    border: 1px solid #dee2e6;
                }
            }
        """

    def generate_summary_report(self, work: Dict[str, Any], bidders: List[Dict[str, Any]]) -> str:
        """Generate a concise summary report."""
        try:
            sorted_bidders = sorted(bidders, key=lambda x: x['bid_amount'])
            lowest_bidder = sorted_bidders[0] if sorted_bidders else None
            
            work_info = work['work_info']
            parsed_date = self.date_utils.parse_date(work_info['date'])
            formatted_date = self.date_utils.format_display_date(parsed_date) if parsed_date else work_info['date']
            
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <title>Tender Summary - {work['nit_number']}</title>
                <style>
                    body {{ font-family: Arial, sans-serif; margin: 20px; }}
                    .header {{ text-align: center; background: #1f77b4; color: white; padding: 20px; }}
                    .content {{ margin: 20px 0; }}
                    .summary-table {{ width: 100%; border-collapse: collapse; margin: 15px 0; }}
                    .summary-table th, .summary-table td {{ border: 1px solid #ddd; padding: 10px; }}
                    .summary-table th {{ background: #f8f9fa; }}
                </style>
            </head>
            <body>
                <div class="header">
                    <h1>Tender Summary Report</h1>
                    <p>{work['nit_number']} - {formatted_date}</p>
                </div>
                
                <div class="content">
                    <h2>Work: {work['work_name']}</h2>
                    <p><strong>Estimated Cost:</strong> ₹{work_info['estimated_cost']:,.2f}</p>
                    <p><strong>Number of Bidders:</strong> {len(bidders)}</p>
                    
                    {f"<p><strong>Lowest Bidder:</strong> {lowest_bidder['name']} - ₹{lowest_bidder['bid_amount']:,.2f} ({lowest_bidder['percentage']:+.2f}%)</p>" if lowest_bidder else ""}
                    
                    <table class="summary-table">
                        <tr><th>Rank</th><th>Bidder</th><th>Amount</th><th>Percentage</th></tr>
            """
            
            for i, bidder in enumerate(sorted_bidders[:5]):  # Top 5 bidders
                html_content += f"""
                        <tr>
                            <td>{i+1}</td>
                            <td>{bidder['name']}</td>
                            <td>₹{bidder['bid_amount']:,.2f}</td>
                            <td>{bidder['percentage']:+.2f}%</td>
                        </tr>
                """
            
            html_content += """
                    </table>
                </div>
            </body>
            </html>
            """
            
            return html_content
            
        except Exception as e:
            logging.error(f"Error generating summary report: {e}")
            raise

import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
from date_utils import DateUtils

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class TenderProcessor:
    """Core tender processing business logic with enhanced date handling."""
    
    def __init__(self):
        self.date_utils = DateUtils()
    
    def calculate_bid_amount(self, estimated_cost: float, percentage: float) -> float:
        """
        Calculate bid amount based on estimated cost and percentage.
        
        Args:
            estimated_cost: Base estimated cost
            percentage: Percentage above (+) or below (-) estimated cost
            
        Returns:
            Calculated bid amount
        """
        try:
            estimated_cost = float(estimated_cost)
            percentage = float(percentage)
            
            if not (-99.99 <= percentage <= 99.99):
                raise ValueError(f"Percentage must be between -99.99% and +99.99%, got {percentage}%")
            
            multiplier = 1 + (percentage / 100)
            bid_amount = estimated_cost * multiplier
            
            return round(bid_amount, 2)
            
        except (ValueError, TypeError) as e:
            logging.error(f"Error calculating bid amount: {e}")
            raise ValueError(f"Invalid input for bid calculation: {e}")
    
    def validate_percentage(self, percentage: float) -> bool:
        """
        Validate percentage is within acceptable range.
        
        Args:
            percentage: Percentage value to validate
            
        Returns:
            True if valid, False otherwise
        """
        try:
            percentage = float(percentage)
            return -99.99 <= percentage <= 99.99
        except (ValueError, TypeError):
            return False
    
    def validate_work_data(self, work_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate and normalize work data with enhanced date handling.
        
        Args:
            work_data: Raw work data dictionary
            
        Returns:
            Validated and normalized work data
        """
        validated_data = work_data.copy()
        
        # Validate required fields
        required_fields = ['work_name', 'nit_number', 'work_info']
        for field in required_fields:
            if field not in validated_data:
                raise ValueError(f"Missing required field: {field}")
        
        work_info = validated_data['work_info']
        
        # Validate and normalize date
        if 'date' in work_info:
            parsed_date = self.date_utils.parse_date(work_info['date'])
            if parsed_date:
                work_info['date'] = self.date_utils.format_date(parsed_date)
                work_info['parsed_date'] = parsed_date
            else:
                logging.warning(f"Could not parse date: {work_info['date']}")
        
        # Validate estimated cost
        if 'estimated_cost' in work_info:
            try:
                work_info['estimated_cost'] = float(work_info['estimated_cost'])
            except (ValueError, TypeError):
                raise ValueError("Invalid estimated cost format")
        
        # Validate earnest money
        if 'earnest_money' in work_info:
            try:
                # Handle both string and numeric earnest money
                earnest_money = work_info['earnest_money']
                if isinstance(earnest_money, str):
                    # Remove currency symbols and commas
                    earnest_money = earnest_money.replace('₹', '').replace(',', '').strip()
                work_info['earnest_money'] = float(earnest_money)
            except (ValueError, TypeError):
                logging.warning(f"Could not parse earnest money: {work_info['earnest_money']}")
                # Set default earnest money as 2% of estimated cost
                work_info['earnest_money'] = work_info.get('estimated_cost', 0) * 0.02
        
        return validated_data
    
    def validate_bidder_data(self, bidder_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate and normalize bidder data.
        
        Args:
            bidder_data: Raw bidder data dictionary
            
        Returns:
            Validated and normalized bidder data
        """
        validated_data = bidder_data.copy()
        
        # Validate required fields
        required_fields = ['name', 'percentage', 'bid_amount']
        for field in required_fields:
            if field not in validated_data:
                raise ValueError(f"Missing required field: {field}")
        
        # Validate percentage
        if not self.validate_percentage(validated_data['percentage']):
            raise ValueError(f"Invalid percentage: {validated_data['percentage']}")
        
        # Validate bid amount
        try:
            validated_data['bid_amount'] = float(validated_data['bid_amount'])
        except (ValueError, TypeError):
            raise ValueError("Invalid bid amount format")
        
        # Add date if not present
        if 'date_added' not in validated_data:
            validated_data['date_added'] = self.date_utils.get_current_date()
        
        return validated_data
    
    def rank_bidders(self, bidders: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Rank bidders by bid amount (lowest first).
        
        Args:
            bidders: List of bidder dictionaries
            
        Returns:
            Sorted list of bidders with rank information
        """
        if not bidders:
            return []
        
        # Sort by bid amount (lowest first)
        sorted_bidders = sorted(bidders, key=lambda x: x['bid_amount'])
        
        # Add rank information
        for i, bidder in enumerate(sorted_bidders):
            bidder['rank'] = i + 1
            bidder['rank_text'] = f"L{i + 1}"
            if i == 0:
                bidder['is_lowest'] = True
            else:
                bidder['is_lowest'] = False
        
        return sorted_bidders
    
    def calculate_statistics(self, bidders: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Calculate statistics for the current tender.
        
        Args:
            bidders: List of bidder dictionaries
            
        Returns:
            Statistics dictionary
        """
        if not bidders:
            return {
                'total_bidders': 0,
                'lowest_bid': 0,
                'highest_bid': 0,
                'average_bid': 0,
                'average_percentage': 0,
                'bid_range': 0
            }
        
        bid_amounts = [bidder['bid_amount'] for bidder in bidders]
        percentages = [bidder['percentage'] for bidder in bidders]
        
        return {
            'total_bidders': len(bidders),
            'lowest_bid': min(bid_amounts),
            'highest_bid': max(bid_amounts),
            'average_bid': sum(bid_amounts) / len(bid_amounts),
            'average_percentage': sum(percentages) / len(percentages),
            'bid_range': max(bid_amounts) - min(bid_amounts)
        }
    
    def format_currency(self, amount: float) -> str:
        """
        Format amount as currency in Indian format.
        
        Args:
            amount: Amount to format
            
        Returns:
            Formatted currency string
        """
        try:
            amount = float(amount)
            # Indian currency formatting
            if amount >= 10000000:  # 1 crore
                crores = amount / 10000000
                return f"₹{crores:.2f} Cr"
            elif amount >= 100000:  # 1 lakh
                lakhs = amount / 100000
                return f"₹{lakhs:.2f} L"
            else:
                return f"₹{amount:,.2f}"
        except (ValueError, TypeError):
            return "₹0.00"
    
    def calculate_project_timeline(self, work_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate project timeline dates with enhanced date handling.
        
        Args:
            work_data: Work data dictionary
            
        Returns:
            Timeline dictionary with calculated dates
        """
        work_info = work_data.get('work_info', {})
        
        # Parse start date
        start_date = self.date_utils.parse_date(work_info.get('date'))
        if not start_date:
            raise ValueError("Invalid or missing start date")
        
        # Calculate commencement date (next day)
        commencement_date = self.date_utils.add_days(start_date, 1)
        
        # Calculate completion date
        time_completion = work_info.get('time_of_completion', '3 Months')
        completion_date = self.date_utils.calculate_completion_date(
            commencement_date, time_completion
        )
        
        return {
            'start_date': start_date,
            'commencement_date': commencement_date,
            'completion_date': completion_date,
            'start_date_str': self.date_utils.format_date(start_date),
            'commencement_date_str': self.date_utils.format_display_date(commencement_date),
            'completion_date_str': self.date_utils.format_display_date(completion_date),
            'duration': time_completion
        }
        
    def generate_outputs(self, work_data: Dict[str, Any], bidders: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate all outputs for a work including comparison table, scrutiny sheet, and acceptance letter.
        
        Args:
            work_data: Dictionary containing work details
            bidders: List of bidder dictionaries
            
        Returns:
            Dictionary containing all generated outputs
        """
        if not work_data or not bidders:
            raise ValueError("Work data and bidders list cannot be empty")
            
        # Rank the bidders
        ranked_bidders = self.rank_bidders(bidders)
        
        # Prepare variables for report generation
        variables = {
            'nit_number': work_data.get('nit_number', ''),
            'work_name': work_data.get('work_name', ''),
            'date': work_data.get('work_info', {}).get('date', ''),
            'estimated_cost': work_data.get('work_info', {}).get('estimated_cost', 0),
            'time_of_completion': work_data.get('work_info', {}).get('time_of_completion', '3 Months'),
            'schedule_amount': work_data.get('work_info', {}).get('schedule_amount', 0),
            'earnest_money': work_data.get('work_info', {}).get('earnest_money', 0),
            'ee_name': work_data.get('work_info', {}).get('ee_name', 'Executive Engineer'),
            'lowest_bidder': ranked_bidders[0] if ranked_bidders else None,
            'bidders': ranked_bidders
        }
        
        try:
            # Generate comparison table
            comparison_table = self._generate_comparison_table(variables)
            
            # Generate scrutiny sheet
            scrutiny_sheet = self._generate_scrutiny_sheet(variables)
            
            # Generate acceptance letter
            acceptance_letter = self._generate_acceptance_letter(variables)
            
            return {
                'comparison_table': comparison_table,
                'scrutiny_sheet': scrutiny_sheet,
                'acceptance_letter': acceptance_letter,
                'variables': variables  # Include variables for reference
            }
            
        except Exception as e:
            logging.error(f"Error generating outputs: {str(e)}")
            raise ValueError(f"Failed to generate outputs: {str(e)}")
            
    def _generate_comparison_table(self, variables: Dict[str, Any]) -> str:
        """
        Generate a comparison table for the bidders.
        
        Args:
            variables: Dictionary containing work and bidder information
            
        Returns:
            Formatted comparison table as string
        """
        if not variables.get('bidders'):
            return "No bidders available for comparison."
            
        table = [
            "Rank | Bidder Name | Quoted Percentage | Bid Amount (₹) | Status",
            "-----|-------------|-------------------|----------------|--------"
        ]
        
        for bidder in variables['bidders']:
            rank = bidder.get('rank', 0)
            name = bidder.get('name', 'N/A')
            percentage = bidder.get('percentage', 0)
            amount = bidder.get('bid_amount', 0)
            
            # Determine status based on rank
            if rank == 1:
                status = 'L1 (Lowest)'
            else:
                if percentage < -5:
                    status = f'L{rank} (Well Below)'
                elif percentage < 0:
                    status = f'L{rank} (Below Est.)'
                elif percentage == 0:
                    status = f'L{rank} (At Estimate)'
                elif percentage < 10:
                    status = f'L{rank} (Above Est.)'
                else:
                    status = f'L{rank} (Well Above)'
            
            table.append(f"{rank:<4} | {name:<11} | {percentage:>+16.2f}% | {amount:>14,.2f} | {status}")
            
        return '\n'.join(table)
        
    def _generate_scrutiny_sheet(self, variables: Dict[str, Any]) -> str:
        """
        Generate a scrutiny sheet for the tender evaluation.
        
        Args:
            variables: Dictionary containing work and bidder information
            
        Returns:
            Formatted scrutiny sheet as string
        """
        if not variables.get('bidders'):
            return "No bidders available for scrutiny."
            
        estimated_cost = float(variables.get('estimated_cost', 0))
        lowest_bidder = variables.get('lowest_bidder')
        
        # Calculate savings if there's a lowest bidder
        if lowest_bidder:
            savings = estimated_cost - lowest_bidder.get('bid_amount', 0)
            savings_percentage = (savings / estimated_cost * 100) if estimated_cost > 0 else 0
        else:
            savings = 0
            savings_percentage = 0
        
        # Prepare bidder details
        bidder_details = []
        for bidder in variables['bidders']:
            bid_amount = bidder.get('bid_amount', 0)
            difference = bid_amount - estimated_cost
            status = f"L{bidder.get('rank', 0)}"
            
            bidder_details.append(
                f"{bidder.get('name', 'N/A'):<40} {bidder.get('percentage', 0):>+8.2f}% "
                f"₹{bid_amount:>15,.2f} {status:>10} (₹{difference:>+12,.2f})"
            )
        
        # Generate the scrutiny sheet
        lowest_bidder_name = lowest_bidder.get('name', 'N/A') if lowest_bidder else 'N/A'
        quoted_percentage = f"{lowest_bidder.get('percentage', 0):+.2f}%" if lowest_bidder else 'N/A'
        calculated_amount = f"₹{lowest_bidder.get('bid_amount', 0):,.2f}" if lowest_bidder else 'N/A'
        
        scrutiny_sheet = f"""
TECHNICAL SCRUTINY SHEET OF TENDER
{'=' * 90}

NIT Number: {variables.get('nit_number', 'N/A')}
Work Name: {variables.get('work_name', 'N/A')}
Date of Opening: {variables.get('date', 'N/A')}
Executive Engineer: {variables.get('ee_name', 'N/A')}

WORK DETAILS:
{'─' * 90}
Estimated Cost: ₹{estimated_cost:,.2f}
Time of Completion: {variables.get('time_of_completion', '3 Months')}
Schedule Amount: ₹{variables.get('schedule_amount', 0):,.2f}
Earnest Money: ₹{variables.get('earnest_money', 0):,.2f}

COMPARATIVE STATEMENT OF BIDS:
{'─' * 90}
{'Bidder Name':<40} {'% Rate':>8} {'Bid Amount (₹)':>15} {'Rank':>10} {'Difference':>12}
{'─' * 90}
{chr(10).join(bidder_details)}
{'─' * 90}

EVALUATION SUMMARY:
{'─' * 90}
LOWEST BIDDER: {lowest_bidder_name}
QUOTED PERCENTAGE: {quoted_percentage}
CALCULATED AMOUNT: {calculated_amount}
ESTIMATED COST: ₹{estimated_cost:,.2f}
NET SAVINGS/EXCESS: ₹{savings:+,.2f} ({savings_percentage:+.2f}%)

TECHNICAL EVALUATION:
- All bidders have quoted rates within permissible range (-99.99% to +99.99%)
- Financial capability and technical qualifications verified
- Bid documents found in order

RECOMMENDATION:
{'─' * 90}
The tender of {lowest_bidder_name}
quoting {quoted_percentage}
(calculated amount: {calculated_amount})
is technically acceptable and financially lowest.

RECOMMENDED for acceptance subject to:
1. Fulfillment of all terms and conditions mentioned in the tender document
2. Submission of required performance security
3. Compliance with technical specifications

Prepared by: Assistant Engineer                  Checked by: Executive Engineer
Date: {datetime.now().strftime('%Y-%m-%d')}                          Date: ___________

Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        return scrutiny_sheet
        
    def _generate_acceptance_letter(self, variables: Dict[str, Any]) -> str:
        """
        Generate acceptance letter as text with enhanced formatting.
        
        Args:
            variables: Dictionary containing all required variables
            
        Returns:
            Formatted acceptance letter as string
        """
        if not variables.get('lowest_bidder'):
            return "No bidders available for acceptance letter generation."
        
        lowest_bidder = variables['lowest_bidder']
        estimated_cost = float(variables.get('estimated_cost', 0))
        
        # Format dates
        date_str = variables.get('date', '')
        parsed_date = self.date_utils.parse_date(date_str)
        formatted_date = self.date_utils.format_display_date(parsed_date) if parsed_date else date_str
        
        # Get work details with defaults
        work_name = variables.get('work_name', '')
        nit_number = variables.get('nit_number', '')
        nit_date = variables.get('nit_date', '')
        
        # Format the acceptance letter according to the provided template
        acceptance_letter = f"""OFFICE OF THE EXECUTIVE ENGINEER PWD ELECTRIC DIVISION UDAIPUR
No.-					Date-		
(Letter of Acceptance of Tender)						
To,						
M/s. {lowest_bidder.get('name', '')}, {lowest_bidder.get('address', '')}						
						
						
Name of Work:		{work_name}			
NIT No.:		{nit_number}		ITEM-1			
NIT Date:		{nit_date}					
Tender Receipt Date:			{formatted_date}				
Your Tender / Negotiations dated:				{formatted_date}			
Dear Sir,						

Security Deposit as per rule of the gross amount of the ruining bill shall be deducted from each running bill or you may opt to deposit full amount of security deposit in the shape of bank guarantee or any acceptable form of security before or at the time of executing agreement. Kindly submit the required stamp duty of Rs. 1000/- as per rule and Deposit Additional Performance Guarantee Amounting to Rs NIL in this Office and do may sign the agreement within 3 days failing which action as per rule may be is initiated.

The receipt of the may please be acknowledged.						
						
Yours Faithfully,						
						
Executive Engineer						
On behalf of the Governor of State of Rajasthan						
No.-					Date-		
Copy to the following for information & necessary action: -						
1. The Superintending Engineer PWD Electric Circle Udaipur.						
2. The Assistant Engineer PWD Electric Sub. Dn I/II Udaipur/Rajsamand for similar action.						
						
Executive Engineer,						
PWD ELECTRICAL DIVISION- UDAIPUR
"""
        return acceptance_letter

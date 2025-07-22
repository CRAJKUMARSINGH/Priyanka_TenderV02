import logging
from typing import Dict, Any, List, Optional
import pandas as pd
from datetime import datetime

logger = logging.getLogger(__name__)

class TenderProcessor:
    """Process tender data and perform calculations"""
    
    def __init__(self):
        self.current_date = datetime.now()
    
    def process_tender_data(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process and validate tender data"""
        try:
            processed_data = raw_data.copy()
            
            # Standardize data types
            processed_data = self._standardize_data_types(processed_data)
            
            # Validate required fields
            validation_result = self._validate_tender_data(processed_data)
            if not validation_result['valid']:
                processed_data['validation_errors'] = validation_result['errors']
                return processed_data
            
            # Calculate derived fields
            processed_data = self._calculate_derived_fields(processed_data)
            
            logger.info("Tender data processed successfully")
            return processed_data
            
        except Exception as e:
            logger.error(f"Error processing tender data: {str(e)}")
            return raw_data
    
    def _standardize_data_types(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Standardize data types for consistent processing"""
        try:
            standardized = data.copy()
            
            # Convert numeric fields
            numeric_fields = [
                'estimated_cost', 'schedule_amount', 'earnest_money', 
                'time_of_completion'
            ]
            
            for field in numeric_fields:
                if field in standardized:
                    try:
                        value = standardized[field]
                        if isinstance(value, str):
                            # Remove currency symbols and commas
                            value = value.replace('₹', '').replace(',', '').replace('Rs.', '').strip()
                        
                        if field == 'time_of_completion':
                            standardized[field] = int(float(value))
                        else:
                            standardized[field] = float(value)
                            
                    except (ValueError, TypeError):
                        logger.warning(f"Could not convert {field} to numeric: {standardized[field]}")
            
            # Standardize text fields
            text_fields = ['nit_number', 'work_name', 'ee_name']
            for field in text_fields:
                if field in standardized and standardized[field]:
                    standardized[field] = str(standardized[field]).strip()
            
            # Standardize date
            if 'date' in standardized:
                date_value = standardized['date']
                if isinstance(date_value, str):
                    standardized['date'] = date_value
                else:
                    standardized['date'] = str(date_value)
            
            return standardized
            
        except Exception as e:
            logger.error(f"Error standardizing data types: {str(e)}")
            return data
    
    def _validate_tender_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate tender data completeness and accuracy"""
        errors = []
        
        # Required fields validation
        required_fields = {
            'nit_number': 'NIT Number',
            'work_name': 'Work Name',
            'estimated_cost': 'Estimated Cost',
            'earnest_money': 'Earnest Money',
            'time_of_completion': 'Time of Completion'
        }
        
        for field, display_name in required_fields.items():
            if field not in data or not data[field]:
                errors.append(f"{display_name} is required")
        
        # Numeric validations
        if 'estimated_cost' in data and data['estimated_cost'] <= 0:
            errors.append("Estimated Cost must be positive")
        
        if 'earnest_money' in data and data['earnest_money'] < 0:
            errors.append("Earnest Money cannot be negative")
        
        if 'time_of_completion' in data and data['time_of_completion'] <= 0:
            errors.append("Time of Completion must be positive")
        
        # Business logic validations
        if 'estimated_cost' in data and 'earnest_money' in data:
            estimated_cost = data['estimated_cost']
            earnest_money = data['earnest_money']
            
            # Typical earnest money is 1-5% of estimated cost
            if earnest_money > 0:
                percentage = (earnest_money / estimated_cost) * 100
                if percentage < 0.5 or percentage > 10:
                    errors.append(f"Earnest Money ({percentage:.2f}% of estimated cost) seems unusual")
        
        return {
            'valid': len(errors) == 0,
            'errors': errors
        }
    
    def _calculate_derived_fields(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate derived fields from tender data"""
        try:
            calculated_data = data.copy()
            
            # Calculate earnest money percentage
            if 'estimated_cost' in data and 'earnest_money' in data and data['estimated_cost'] > 0:
                earnest_percentage = (data['earnest_money'] / data['estimated_cost']) * 100
                calculated_data['earnest_money_percentage'] = round(earnest_percentage, 2)
            
            # Set default schedule amount if not provided
            if 'schedule_amount' not in calculated_data or not calculated_data['schedule_amount']:
                calculated_data['schedule_amount'] = calculated_data.get('estimated_cost', 0)
            
            # Add processing timestamp
            calculated_data['processed_at'] = self.current_date.isoformat()
            
            return calculated_data
            
        except Exception as e:
            logger.error(f"Error calculating derived fields: {str(e)}")
            return data
    
    def process_bidder_data(self, bidders: List[Dict[str, Any]], estimated_cost: float) -> Dict[str, Any]:
        """Process and analyze bidder data"""
        try:
            if not bidders:
                return {
                    'processed_bidders': [],
                    'analysis': {'error': 'No bidder data provided'}
                }
            
            processed_bidders = []
            
            for i, bidder in enumerate(bidders):
                processed_bidder = self._process_single_bidder(bidder, estimated_cost, i + 1)
                if processed_bidder:
                    processed_bidders.append(processed_bidder)
            
            # Sort by bid amount (lowest first)
            processed_bidders.sort(key=lambda x: x['bid_amount'])
            
            # Add rank information
            for rank, bidder in enumerate(processed_bidders, 1):
                bidder['rank'] = rank
                bidder['is_lowest'] = (rank == 1)
            
            # Perform analysis
            analysis = self._analyze_bidders(processed_bidders, estimated_cost)
            
            return {
                'processed_bidders': processed_bidders,
                'analysis': analysis
            }
            
        except Exception as e:
            logger.error(f"Error processing bidder data: {str(e)}")
            return {
                'processed_bidders': bidders,
                'analysis': {'error': str(e)}
            }
    
    def _process_single_bidder(self, bidder: Dict[str, Any], estimated_cost: float, serial: int) -> Optional[Dict[str, Any]]:
        """Process a single bidder's data"""
        try:
            processed = bidder.copy()
            
            # Validate required fields
            if not bidder.get('name', '').strip():
                logger.warning(f"Bidder {serial}: Name is required")
                return None
            
            # Standardize name
            processed['name'] = bidder['name'].strip()
            
            # Process percentage
            percentage = bidder.get('percentage', 0)
            if isinstance(percentage, str):
                try:
                    percentage = float(percentage.replace('%', '').strip())
                except ValueError:
                    percentage = 0
            
            processed['percentage'] = float(percentage)
            
            # Calculate bid amount
            if 'bid_amount' not in processed or not processed['bid_amount']:
                bid_amount = estimated_cost * (1 + percentage / 100)
                processed['bid_amount'] = round(bid_amount, 2)
            else:
                processed['bid_amount'] = float(processed['bid_amount'])
            
            # Format percentage display
            if percentage > 0:
                processed['percentage_display'] = f"{percentage:.2f}% ABOVE"
            elif percentage < 0:
                processed['percentage_display'] = f"{abs(percentage):.2f}% BELOW"
            else:
                processed['percentage_display'] = "AT ESTIMATE"
            
            # Add serial number
            processed['serial'] = serial
            
            # Standardize contact
            processed['contact'] = str(bidder.get('contact', '')).strip()
            
            return processed
            
        except Exception as e:
            logger.error(f"Error processing bidder {serial}: {str(e)}")
            return None
    
    def _analyze_bidders(self, bidders: List[Dict[str, Any]], estimated_cost: float) -> Dict[str, Any]:
        """Analyze bidder data and provide insights"""
        try:
            if not bidders:
                return {'error': 'No valid bidders to analyze'}
            
            bid_amounts = [b['bid_amount'] for b in bidders]
            percentages = [b['percentage'] for b in bidders]
            
            analysis = {
                'total_bidders': len(bidders),
                'lowest_bid': min(bid_amounts),
                'highest_bid': max(bid_amounts),
                'average_bid': sum(bid_amounts) / len(bid_amounts),
                'bid_range': max(bid_amounts) - min(bid_amounts),
                'lowest_bidder': bidders[0],  # Already sorted by bid amount
            }
            
            # Calculate savings/excess
            lowest_bid = analysis['lowest_bid']
            if lowest_bid < estimated_cost:
                analysis['savings'] = estimated_cost - lowest_bid
                analysis['savings_percentage'] = ((estimated_cost - lowest_bid) / estimated_cost) * 100
                analysis['is_saving'] = True
            else:
                analysis['excess'] = lowest_bid - estimated_cost
                analysis['excess_percentage'] = ((lowest_bid - estimated_cost) / estimated_cost) * 100
                analysis['is_saving'] = False
            
            # Bidder distribution analysis
            above_estimate = len([p for p in percentages if p > 0])
            below_estimate = len([p for p in percentages if p < 0])
            at_estimate = len([p for p in percentages if p == 0])
            
            analysis['bidder_distribution'] = {
                'above_estimate': above_estimate,
                'below_estimate': below_estimate,
                'at_estimate': at_estimate
            }
            
            # Competition analysis
            if len(bidders) >= 3:
                analysis['competition_level'] = 'High'
            elif len(bidders) == 2:
                analysis['competition_level'] = 'Moderate'
            else:
                analysis['competition_level'] = 'Low'
            
            # Price spread analysis
            if analysis['bid_range'] > 0:
                spread_percentage = (analysis['bid_range'] / analysis['average_bid']) * 100
                analysis['price_spread_percentage'] = spread_percentage
                
                if spread_percentage > 20:
                    analysis['spread_analysis'] = 'High variation in bids'
                elif spread_percentage > 10:
                    analysis['spread_analysis'] = 'Moderate variation in bids'
                else:
                    analysis['spread_analysis'] = 'Low variation in bids'
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing bidders: {str(e)}")
            return {'error': str(e)}
    
    def generate_recommendation(self, analysis: Dict[str, Any]) -> str:
        """Generate recommendation based on bidder analysis"""
        try:
            if 'error' in analysis:
                return f"Unable to generate recommendation: {analysis['error']}"
            
            recommendations = []
            
            # Lowest bidder recommendation
            lowest_bidder = analysis.get('lowest_bidder', {})
            if lowest_bidder:
                name = lowest_bidder.get('name', 'Unknown')
                amount = lowest_bidder.get('bid_amount', 0)
                recommendations.append(f"Lowest bidder: {name} with bid amount ₹{amount:,.2f}")
            
            # Savings/excess analysis
            if analysis.get('is_saving'):
                savings = analysis.get('savings', 0)
                savings_pct = analysis.get('savings_percentage', 0)
                recommendations.append(f"Project will save ₹{savings:,.2f} ({savings_pct:.2f}% below estimate)")
            else:
                excess = analysis.get('excess', 0)
                excess_pct = analysis.get('excess_percentage', 0)
                recommendations.append(f"Project will cost ₹{excess:,.2f} extra ({excess_pct:.2f}% above estimate)")
            
            # Competition analysis
            competition = analysis.get('competition_level', 'Unknown')
            total_bidders = analysis.get('total_bidders', 0)
            recommendations.append(f"Competition level: {competition} ({total_bidders} bidders)")
            
            # Price spread analysis
            spread_analysis = analysis.get('spread_analysis')
            if spread_analysis:
                recommendations.append(f"Price analysis: {spread_analysis}")
            
            return ". ".join(recommendations) + "."
            
        except Exception as e:
            logger.error(f"Error generating recommendation: {str(e)}")
            return "Unable to generate recommendation due to processing error."

import pandas as pd
import random
import os
from datetime import datetime, timedelta

class TestDataGenerator:
    """Generate test data for comprehensive testing"""
    
    def __init__(self):
        self.company_names = [
            "ABC Construction Pvt. Ltd.",
            "XYZ Builders & Contractors",
            "Supreme Engineering Works",
            "Modern Infrastructure Ltd.",
            "Progressive Construction Co.",
            "Elite Builders Pvt. Ltd.",
            "Reliable Construction Group",
            "Advanced Engineering Solutions",
            "Prime Infrastructure Pvt. Ltd.",
            "Excellence Construction Co."
        ]
        
        self.work_descriptions = [
            "Construction of concrete road with drainage",
            "Building construction with modern facilities",
            "Bridge construction over river",
            "Water supply pipeline installation",
            "Sewerage treatment plant construction",
            "Multi-story building construction",
            "Road widening and improvement",
            "Park development and landscaping",
            "School building construction",
            "Hospital building construction"
        ]
    
    def generate_nit_1_work_data(self):
        """Generate test data for single work NIT"""
        # Basic tender information
        tender_data = {
            'NIT Number': f"NIT-{random.randint(100, 999)}/2024-25",
            'Work Description': random.choice(self.work_descriptions),
            'Estimated Cost': random.randint(500000, 5000000),
            'EMD Amount': random.randint(10000, 100000),
            'Completion Period': f"{random.randint(6, 24)} months",
            'Date of Opening': (datetime.now() + timedelta(days=random.randint(1, 30))).strftime('%d/%m/%Y')
        }
        
        # Generate bidder data
        num_bidders = random.randint(3, 8)
        bidders_data = []
        
        for i in range(num_bidders):
            base_rate = tender_data['Estimated Cost']
            variation = random.uniform(-0.15, 0.10)  # -15% to +10% variation
            quoted_amount = base_rate * (1 + variation)
            
            bidder = {
                'S.No.': i + 1,
                'Name of Bidder': random.choice(self.company_names),
                'Quoted Amount': round(quoted_amount, 2),
                'EMD Submitted': random.choice(['Yes', 'No']),
                'Technical Qualification': random.choice(['Qualified', 'Not Qualified', 'Conditional']),
                'Financial Qualification': random.choice(['Qualified', 'Not Qualified']),
                'Overall Status': random.choice(['Qualified', 'Not Qualified', 'Conditional'])
            }
            bidders_data.append(bidder)
        
        # Create DataFrame and save to Excel
        df_tender = pd.DataFrame([tender_data])
        df_bidders = pd.DataFrame(bidders_data)
        
        return df_tender, df_bidders
    
    def generate_nit_10_works_data(self):
        """Generate test data for multiple works NIT"""
        works_data = []
        all_bidders_data = []
        
        for work_no in range(1, 11):  # 10 works
            # Work details
            work_data = {
                'Work No.': work_no,
                'NIT Number': f"NIT-{random.randint(100, 999)}/2024-25",
                'Work Description': random.choice(self.work_descriptions),
                'Estimated Cost': random.randint(200000, 2000000),
                'EMD Amount': random.randint(5000, 50000),
                'Completion Period': f"{random.randint(3, 18)} months"
            }
            works_data.append(work_data)
            
            # Generate bidders for this work
            num_bidders = random.randint(2, 6)
            for bidder_no in range(num_bidders):
                base_rate = work_data['Estimated Cost']
                variation = random.uniform(-0.12, 0.08)
                quoted_amount = base_rate * (1 + variation)
                
                bidder_data = {
                    'Work No.': work_no,
                    'Bidder No.': bidder_no + 1,
                    'Name of Bidder': random.choice(self.company_names),
                    'Quoted Amount': round(quoted_amount, 2),
                    'EMD Status': random.choice(['Submitted', 'Not Submitted']),
                    'Technical Score': random.randint(60, 100),
                    'Financial Score': random.randint(70, 100),
                    'Overall Status': random.choice(['Qualified', 'Not Qualified'])
                }
                all_bidders_data.append(bidder_data)
        
        df_works = pd.DataFrame(works_data)
        df_all_bidders = pd.DataFrame(all_bidders_data)
        
        return df_works, df_all_bidders
    
    def create_test_excel_files(self):
        """Create test Excel files in attached_assets directory"""
        os.makedirs("attached_assets", exist_ok=True)
        
        # Create NIT_1 work test file
        df_tender_1, df_bidders_1 = self.generate_nit_1_work_data()
        
        with pd.ExcelWriter("attached_assets/test_nit_1.xlsx", engine='openpyxl') as writer:
            df_tender_1.to_excel(writer, sheet_name='Tender_Info', index=False)
            df_bidders_1.to_excel(writer, sheet_name='Bidders', index=False)
        
        # Create NIT_10 works test file
        df_works_10, df_bidders_10 = self.generate_nit_10_works_data()
        
        with pd.ExcelWriter("attached_assets/test_nit_10.xlsx", engine='openpyxl') as writer:
            df_works_10.to_excel(writer, sheet_name='Works_Info', index=False)
            df_bidders_10.to_excel(writer, sheet_name='All_Bidders', index=False)
        
        return "attached_assets/test_nit_1.xlsx", "attached_assets/test_nit_10.xlsx"
    
    def generate_custom_bidder_data(self, work_count=1):
        """Generate custom bidder data for testing"""
        custom_bidders = []
        
        for work_no in range(1, work_count + 1):
            # Add some outside bidders
            outside_bidders = [
                {
                    'name': 'Custom Builder Pvt. Ltd.',
                    'quoted_amount': random.randint(500000, 1500000),
                    'work_no': work_no,
                    'status': 'Outside List'
                },
                {
                    'name': 'Independent Contractors',
                    'quoted_amount': random.randint(600000, 1600000),
                    'work_no': work_no,
                    'status': 'Outside List'
                }
            ]
            custom_bidders.extend(outside_bidders)
        
        return custom_bidders

# Global test data generator instance
test_data_gen = TestDataGenerator()

#!/usr/bin/env python3
"""
Margin Test Script - Generate PDFs and verify 10mm margins
"""

import os
import sys
from datetime import datetime
from template_processor import TemplateProcessor
from pdf_generator import PDFGenerator
from latex_report_generator import LatexReportGenerator

def create_sample_work_data():
    """Create sample work data with bidders"""
    return {
        'nit_number': 'TEST/2025-26',
        'work_name': 'Test Electric Cabling and Maintenance Work - Margin Test',
        'estimated_cost': 500000,
        'earnest_money': 10000,
        'schedule_amount': 500000,
        'time_of_completion': 6,
        'ee_name': 'Test Executive Engineer',
        'date': '01-01-25',
        'receipt_date': '02-01-25',
        'bidders': [
            {
                'name': 'M/s. Test Contractor A',
                'percentage': -2.5,
                'bid_amount': 487500,
                'contact': '9876543210'
            },
            {
                'name': 'M/s. Test Contractor B', 
                'percentage': -1.0,
                'bid_amount': 495000,
                'contact': '9876543211'
            },
            {
                'name': 'M/s. Test Contractor C',
                'percentage': 0.5,
                'bid_amount': 502500,
                'contact': '9876543212'
            },
            {
                'name': 'M/s. Test Contractor D',
                'percentage': 1.5,
                'bid_amount': 507500,
                'contact': '9876543213'
            }
        ]
    }

def test_document_generation():
    """Test document generation with margin verification"""
    
    print("🔧 Starting margin test - generating documents with 10mm margins...")
    
    # Initialize processors
    latex_generator = LatexReportGenerator()
    pdf_generator = PDFGenerator()
    
    # Create sample data
    work_data = create_sample_work_data()
    
    # Document types to test
    doc_types = [
        ('comparative_statement', 'Comparative Statement'),
        ('letter_of_acceptance', 'Letter of Acceptance'),  
        ('scrutiny_sheet', 'Scrutiny Sheet'),
        ('work_order', 'Work Order')
    ]
    
    results = []
    
    for doc_type, display_name in doc_types:
        print(f"\n📄 Generating {display_name}...")
        
        try:
            # Generate LaTeX content using the LaTeX report generator
            latex_content = latex_generator.generate_document(doc_type, work_data)
            
            if not latex_content:
                print(f"❌ Failed to generate LaTeX content for {display_name}")
                continue
            
            # Save LaTeX file for inspection
            tex_filename = f"margin_test_{doc_type}"
            tex_path = os.path.join("outputs", f"{tex_filename}.tex")
            
            with open(tex_path, 'w', encoding='utf-8') as f:
                f.write(latex_content)
            
            print(f"✅ LaTeX file saved: {tex_path}")
            
            # Check if geometry settings are correct in the LaTeX
            if "margin=10mm" in latex_content:
                print(f"✅ Correct margin setting found in LaTeX: margin=10mm")
                margin_status = "✅ 10mm"
            elif "margin=2cm" in latex_content:
                print(f"❌ Wrong margin setting found in LaTeX: margin=2cm (should be 10mm)")
                margin_status = "❌ 20mm (2cm)"
            else:
                print(f"⚠️  No explicit margin setting found in LaTeX")
                margin_status = "⚠️  Default"
            
            # Generate PDF
            pdf_result = pdf_generator.generate_pdf(latex_content, tex_filename)
            
            if pdf_result['success']:
                print(f"✅ PDF generated successfully: {pdf_result['pdf_path']}")
                print(f"📏 PDF file size: {pdf_result['size']} bytes")
                
                results.append({
                    'document': display_name,
                    'latex_file': tex_path,
                    'pdf_file': pdf_result['pdf_path'],
                    'margin_setting': margin_status,
                    'status': '✅ Success'
                })
            else:
                print(f"❌ PDF generation failed: {pdf_result['error']}")
                results.append({
                    'document': display_name,
                    'latex_file': tex_path,
                    'pdf_file': 'Not generated',
                    'margin_setting': margin_status,
                    'status': f"❌ PDF Error: {pdf_result['error']}"
                })
                
        except Exception as e:
            print(f"❌ Error generating {display_name}: {str(e)}")
            results.append({
                'document': display_name,
                'latex_file': 'Not generated',
                'pdf_file': 'Not generated', 
                'margin_setting': '❌ Error',
                'status': f"❌ Exception: {str(e)}"
            })
    
    # Print summary
    print("\n" + "="*60)
    print("📊 MARGIN TEST RESULTS SUMMARY")
    print("="*60)
    
    for result in results:
        print(f"\n📄 {result['document']}")
        print(f"   LaTeX: {result['latex_file']}")
        print(f"   PDF: {result['pdf_file']}")
        print(f"   Margin: {result['margin_setting']}")
        print(f"   Status: {result['status']}")
    
    print("\n" + "="*60)
    print("🔍 NEXT STEPS:")
    print("1. Check the generated PDF files in the 'outputs' directory")
    print("2. Measure the actual margins in the PDF viewer")
    print("3. Verify A4 page size (210mm x 297mm)")
    print("4. Confirm 10mm margins on all sides")
    print("="*60)
    
    return results

def check_latex_settings():
    """Check current LaTeX settings in templates"""
    print("\n🔍 Checking current template settings...")
    
    template_files = [
        "templates/comparative_statement.tex",
        "templates/letter_of_acceptance.tex", 
        "templates/scrutiny_sheet.tex",
        "templates/work_order.tex"
    ]
    
    for template_file in template_files:
        if os.path.exists(template_file):
            with open(template_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            print(f"\n📄 {template_file}:")
            if "margin=10mm" in content:
                print("   ✅ Correct: margin=10mm")
            elif "margin=2cm" in content:
                print("   ❌ Wrong: margin=2cm (should be 10mm)")
            elif "geometry" in content:
                # Extract geometry line
                for line in content.split('\n'):
                    if 'geometry' in line.lower() and ('margin' in line or 'left=' in line):
                        print(f"   ⚠️  Found: {line.strip()}")
            else:
                print("   ⚠️  No geometry settings found")
        else:
            print(f"\n📄 {template_file}: ❌ File not found")

if __name__ == "__main__":
    print("🚀 TenderLatexPro Margin Test")
    print("="*40)
    
    # Ensure output directory exists
    os.makedirs("outputs", exist_ok=True)
    
    # Check current template settings
    check_latex_settings()
    
    # Run the test
    results = test_document_generation()
    
    print(f"\n✅ Test completed. Check the 'outputs' directory for generated files.")

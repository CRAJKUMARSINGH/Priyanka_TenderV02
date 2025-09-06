import sys
import os
sys.path.append('..')
from pdf_generator import PDFGenerator

# Read the simple test file
with open('simple_margin_test.tex', 'r', encoding='utf-8') as f:
    content = f.read()

# Generate PDF
pdf_gen = PDFGenerator()
result = pdf_gen.generate_pdf(content, 'simple_margin_test')

if result['success']:
    print('✅ PDF generated successfully!')
    print('📄 File:', result['pdf_path'])
    print('📏 Size:', result['size'], 'bytes')
    print('🔍 Please check the PDF for 10mm margins on all sides.')
    print('📐 Expected: A4 page (210mm × 297mm) with 10mm margins = 190mm × 277mm content area')
else:
    print('❌ PDF generation failed:')
    print('Error:', result['error'])
    if 'latex_check' in result:
        print('LaTeX check:', result['latex_check'])

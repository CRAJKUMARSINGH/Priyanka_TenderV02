import logging
from typing import Dict, Any, List
from datetime import datetime

logger = logging.getLogger(__name__)

class UserManualGenerator:
    """Generate comprehensive user manual and help content"""
    
    def __init__(self):
        self.version = "2.0"
        self.last_updated = datetime.now().strftime("%Y-%m-%d")
    
    def get_complete_manual(self) -> Dict[str, str]:
        """Get complete user manual sections"""
        return {
            "getting_started": self.get_getting_started_guide(),
            "excel_format": self.get_excel_format_guide(),
            "document_types": self.get_document_types_guide(),
            "troubleshooting": self.get_troubleshooting_guide(),
            "latex_templates": self.get_latex_templates_guide(),
            "system_requirements": self.get_system_requirements(),
            "faq": self.get_faq_section(),
            "contact_support": self.get_contact_support()
        }
    
    def get_getting_started_guide(self) -> str:
        """Get getting started guide"""
        return """
# Getting Started with Enhanced Tender Processing System

## Welcome!
This system helps government departments process tenders efficiently with automated PDF generation and statutory compliance.

## Quick Start Steps

### 1. 📁 Data Input
- **Upload Excel Files**: Use the Excel upload feature for bulk data import
- **Upload PDF Files**: Extract data from existing PDF documents  
- **Manual Entry**: Enter NIT details manually using the form

### 2. 🏗️ Work Entry
- Add bidder information including names and bid percentages
- System automatically calculates bid amounts and rankings
- Manage bidder database for future reference

### 3. 📊 PDF Reports
- Generate statutory-compliant documents:
  - Comparative Statement of Tenders
  - Letter of Acceptance
  - Scrutiny Sheet
  - Work Order
- Choose output format (PDF, LaTeX, or both)

### 4. 👥 Bidder Management
- Track bidder participation across tenders
- View statistics and analytics
- Export bidder lists for reporting

## System Features
✅ **Excel and PDF file parsing** - Intelligent data extraction  
✅ **Automated calculations** - Bid amounts and percentages  
✅ **LaTeX-based PDF generation** - Professional document output  
✅ **Statutory compliance** - Government format requirements  
✅ **Bidder database** - Centralized bidder management  
✅ **Template management** - Customizable document templates  
✅ **Data validation** - Error checking and warnings  
✅ **Export capabilities** - Multiple output formats

## First Time Setup
1. Check system status in the sidebar
2. Ensure LaTeX is installed for PDF generation
3. Verify template files are available
4. Test with sample data entry

## Navigation Tips
- Use the sidebar to monitor system health
- Check template status before generating documents
- Enable debug mode for detailed error information
- Use the clear data option to reset all information
"""
    
    def get_excel_format_guide(self) -> str:
        """Get Excel format guide"""
        return """
# Excel File Format Guide

## Required Columns for NIT Data

### Basic Information
- **NIT Number**: Format like "27/2024-25" or "NIT-123/2024"
- **Work Name**: Detailed description of the work/project
- **Estimated Cost**: Numerical value in rupees (without currency symbols)
- **Schedule Amount**: Numerical value in rupees
- **Earnest Money**: Security deposit amount in rupees
- **Time of Completion**: Duration in months (numerical)
- **EE Name**: Executive Engineer's full name
- **Date**: Tender date in DD-MM-YYYY format

### Bidder Information Columns
- **Bidder 1 Name**: Full legal name of first bidder
- **Bidder 1 Percentage**: Bid percentage (+/- from estimate)
- **Bidder 1 Contact**: Phone number or email
- **Bidder 2 Name**: Second bidder name (if applicable)
- **Bidder 2 Percentage**: Second bidder percentage
- ... (continue for additional bidders)

## Sample Excel Structure

| NIT Number | Work Name | Estimated Cost | Earnest Money | Bidder 1 Name | Bidder 1 % |
|------------|-----------|----------------|---------------|---------------|-------------|
| 27/2024-25 | Road Construction Work | 1000000 | 20000 | ABC Company | -5.5 |
| 28/2024-25 | Building Repair | 500000 | 10000 | XYZ Contractors | 2.0 |

## Column Name Variations
The system recognizes multiple column name formats:

### NIT Number
- "NIT Number", "NIT No", "Tender Number", "Tender No"

### Work Name  
- "Work Name", "Work Description", "Description", "Work"

### Estimated Cost
- "Estimated Cost", "Estimate", "Cost", "Amount"

### Earnest Money
- "Earnest Money", "EM", "Security Deposit"

### Time of Completion
- "Time of Completion", "Completion Time", "Duration", "Months"

## Data Format Requirements

### Numeric Fields
- Use plain numbers without currency symbols (₹, Rs.)
- Avoid commas in large numbers when possible
- Decimals are acceptable for percentages

### Percentage Fields
- Use positive numbers for bids above estimate (+5.5)
- Use negative numbers for bids below estimate (-3.2)
- Zero for bids exactly at estimate (0)

### Text Fields
- Use clear, descriptive names
- Avoid special characters that might cause LaTeX issues
- Keep contact information in standard formats

## Multiple Sheet Support
- The system can read multiple sheets in a workbook
- Data will be combined from all sheets
- Use consistent column naming across sheets

## Common Issues and Solutions

### File Not Reading
- Save as .xlsx format for best compatibility
- Ensure first row contains column headers
- Remove completely empty rows and columns

### Data Not Extracting
- Check column names match expected formats
- Verify numeric fields contain only numbers
- Ensure percentage values are in decimal format

### Bidder Information Missing
- Use consistent naming pattern (Bidder 1, Bidder 2, etc.)
- Include both name and percentage columns
- Contact information is optional but recommended

## Tips for Best Results
1. **Use Template**: Create a template file with proper column headers
2. **Consistent Format**: Maintain same format across all tender files
3. **Data Validation**: Check data before uploading
4. **Backup Files**: Keep original files as backup
5. **Test Small**: Test with a few entries before bulk upload
"""
    
    def get_document_types_guide(self) -> str:
        """Get document types guide"""
        return """
# Document Types and Templates

## Available Document Types

### 📊 Comparative Statement of Tenders
**Purpose**: Complete bidder comparison with statutory format compliance

**Contents**:
- Office header with department information
- NIT details (number, work name, estimated cost)
- Bidder comparison table with rankings
- Percentage calculations (above/below/at estimate)
- Lowest bidder identification
- Executive Engineer signature block

**When to Use**: 
- After tender opening and evaluation
- For internal review and approval
- Required for all government tenders

**Output Format**: Professional table layout with proper statutory formatting

---

### ✉️ Letter of Acceptance
**Purpose**: Official acceptance letter for the successful bidder

**Contents**:
- Official letterhead and office details
- Tender reference and date
- Successful bidder details
- Accepted bid amount and percentage
- Contract terms and conditions
- Commencement and completion requirements
- Official signatures and seals

**When to Use**:
- After tender approval and selection
- To formally notify the successful bidder
- As part of contract documentation

**Output Format**: Official government letter format

---

### 🔍 Scrutiny Sheet
**Purpose**: Technical and financial evaluation document

**Contents**:
- Tender evaluation criteria
- Bidder qualification status
- Technical compliance checklist
- Financial evaluation summary
- Recommendation section
- Evaluator signatures

**When to Use**:
- During tender evaluation process
- For technical committee review
- Documentation of evaluation decisions

**Output Format**: Structured evaluation form

---

### 📝 Work Order
**Purpose**: Project commencement authorization document

**Contents**:
- Work order number and date
- Contractor details and contact information
- Scope of work description
- Contract amount and payment terms
- Timeline and milestones
- Terms and conditions
- Performance guarantees
- Authority signatures

**When to Use**:
- After contract finalization
- To authorize work commencement
- As legal work authorization

**Output Format**: Official work order with all contractual details

## Template Customization

### Variable Substitution
Templates use the following variable format: `{{variable_name}}`

**Common Variables**:
- `{{nit_number}}` - Tender/NIT number
- `{{work_name}}` - Work description
- `{{estimated_cost}}` - Estimated project cost
- `{{lowest_bidder_name}}` - Name of successful bidder
- `{{lowest_bidder_amount}}` - Winning bid amount
- `{{ee_name}}` - Executive Engineer name
- `{{current_date}}` - Current date in DD-MM-YY format

### Conditional Logic
Templates support conditional statements:
```latex
{{#if condition}}
Content shown when condition is true
{{#else}}
Content shown when condition is false
{{/if}}
```

### Loop Constructs
For repetitive data like bidder tables:
```latex
{{#each bidders}}
{{@index1}} & {{name}} & {{amount}} \\
{{/each}}
```

## Best Practices

### Template Maintenance
- Keep templates in the `templates/` directory
- Use descriptive file names (e.g., `comparative_statement.tex`)
- Include comments for complex LaTeX sections
- Test templates with sample data before production use

### Variable Naming
- Use descriptive variable names
- Follow consistent naming conventions
- Include units in amount variables (e.g., `amount_rupees`)
- Use clear date format indicators

### Output Quality
- All documents follow PWD statutory requirements
- Professional formatting with proper spacing
- Government letterhead and official signatures
- Compliance with tender documentation standards
"""

    def get_troubleshooting_guide(self) -> str:
        """Get troubleshooting guide"""
        return """
# Troubleshooting Guide

## Common Issues and Solutions

### 🚫 Application Startup Issues

**Issue**: Application won't start or shows import errors
**Solutions**:
1. Check Python version (requires Python 3.8+)
2. Install required packages: `pip install -r requirements.txt`
3. Verify Streamlit installation: `streamlit --version`
4. Check file permissions in project directory

**Issue**: Database connection errors
**Solutions**:
1. Check if `tender_bidders.db` exists in project root
2. Verify SQLite installation
3. Check file write permissions
4. Restart application to reinitialize database

### 📁 File Upload Problems

**Issue**: Excel file not reading correctly
**Solutions**:
1. Save file in .xlsx format (not .xls)
2. Ensure first row contains column headers
3. Remove empty rows and columns
4. Check for merged cells (not supported)
5. Verify file is not password protected

**Issue**: PDF parsing fails
**Solutions**:
1. Ensure PDF contains readable text (not scanned images)
2. Check file is not corrupted
3. Try OCR for scanned documents
4. Use alternative PDF processing if available

### 💾 Data Entry Issues

**Issue**: Bidder information not saving
**Solutions**:
1. Check all required fields are filled
2. Verify percentage format (use decimal: 0.95 for 95%)
3. Ensure bidder names are unique
4. Check database write permissions

**Issue**: Validation errors
**Solutions**:
1. Check NIT number format (must be alphanumeric)
2. Verify dates are in DD-MM-YYYY format
3. Ensure amounts are numeric only
4. Check percentage values are between 0 and 2 (0-200%)

### 📄 PDF Generation Problems

**Issue**: LaTeX compilation fails
**Solutions**:
1. Install complete LaTeX distribution
2. Check LaTeX PATH environment variable
3. Verify template syntax is correct
4. Use simpler templates for testing
5. Check special characters in data

**Issue**: Generated PDF has formatting issues
**Solutions**:
1. Check template variable substitution
2. Verify long text fields don't break layout
3. Test with shorter data first
4. Update LaTeX packages if needed

### 🔧 System Performance Issues

**Issue**: Slow file processing
**Solutions**:
1. Process smaller files first
2. Close other applications to free memory
3. Check available disk space
4. Restart application periodically

**Issue**: Memory errors
**Solutions**:
1. Process files in smaller batches
2. Restart application between large operations
3. Check system RAM availability
4. Close unnecessary browser tabs

## Error Messages and Solutions

### "File not found" Errors
- Check file path is correct
- Verify file exists and is accessible
- Check file permissions
- Ensure file is not open in another application

### "Permission denied" Errors
- Run with appropriate user permissions
- Check folder write permissions
- Close files that may be locked
- Restart application as administrator if needed

### "Invalid format" Errors
- Check file format matches expected type
- Verify data structure matches requirements
- Use provided templates for reference
- Remove any special characters or formatting

## Getting Help

### Log Files
Application logs are stored in the `logs/` directory:
- `app.log` - General application events
- `error.log` - Error messages and stack traces
- `processing.log` - File processing activities

### Contact Information
For technical support and queries:
- System developed for PWD Electric Division, Udaipur
- Technical support: Contact system administrator
- Feature requests: Document and submit through proper channels

### Development Notes
- Built with Streamlit and Python
- Uses SQLite for data storage
- LaTeX for professional document generation
- Open source libraries for file processing

## Preventive Measures

### Data Backup
- Regularly backup `tender_bidders.db`
- Keep copies of template files
- Save processed documents in organized folders
- Maintain original source files

### System Maintenance
- Keep Python and packages updated
- Regularly clean temporary files
- Monitor disk space usage
- Restart application weekly for optimal performance

### Best Practices
- Test with small datasets first
- Validate data before bulk processing
- Use consistent file naming conventions
- Document any custom modifications
"""

    def get_latex_templates_guide(self) -> str:
        """Get LaTeX templates guide"""
        return """
# LaTeX Templates Guide

## Template Structure
All LaTeX templates follow government documentation standards with:
- Official PWD letterhead formatting
- Statutory compliance requirements
- Professional layout and typography
- Dynamic variable substitution

## Available Templates
- `comparative_statement.tex` - Bidder comparison table
- `letter_of_acceptance.tex` - Official acceptance letter
- `scrutiny_sheet.tex` - Technical evaluation form
- `work_order.tex` - Project authorization document

## Customization
Templates support dynamic variables using `{{variable_name}}` syntax.
Variables are automatically populated from tender data during PDF generation.
"""

    def get_system_requirements(self) -> str:
        """Get system requirements"""
        return """
# System Requirements

## Software Requirements
- Python 3.8 or higher
- Streamlit web framework
- LaTeX distribution (for PDF generation)
- SQLite database support

## Hardware Requirements
- 4GB RAM minimum (8GB recommended)
- 2GB free disk space
- Internet connection for initial setup

## Operating System Support
- Windows 10/11
- macOS 10.14 or later
- Linux (Ubuntu 18.04+ or equivalent)
"""

    def get_faq_section(self) -> str:
        """Get FAQ section"""
        return """
# Frequently Asked Questions

## Q: Can I use .xls files instead of .xlsx?
A: The system works best with .xlsx format. Convert .xls files to .xlsx for optimal compatibility.

## Q: What if LaTeX is not installed?
A: Download and install a complete LaTeX distribution like TeX Live or MiKTeX before using PDF generation features.

## Q: How do I handle special characters in tender data?
A: The system automatically escapes special characters for LaTeX compatibility. Avoid manually adding LaTeX commands in data fields.

## Q: Can I modify the generated PDFs?
A: PDFs are generated from templates. To modify format, edit the LaTeX template files in the templates/ directory.
"""

    def get_contact_support(self) -> str:
        """Get contact support information"""
        return """
# Contact and Support

## System Credits
Developed for **PWD Electric Division, Udaipur**
Under the guidance of **Mrs. Premlata Jain, Additional Administrative Officer, PWD, Udaipur**

## Technical Support
For technical assistance and system support:
- Contact your local IT administrator
- Refer to the troubleshooting guide for common issues
- Document any bugs or feature requests through proper channels

## Training and Documentation
- User manual sections cover all major features
- Practice with sample data before production use
- Refer to template guides for customization help
"""

from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.lib.units import inch, mm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from datetime import datetime
from typing import Dict, Any, List
import io
import logging
from date_utils import DateUtils

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class PDFGenerator:
    """Generates PDF documents for tender processing system."""
    
    def __init__(self):
        self.date_utils = DateUtils()
        self.styles = getSampleStyleSheet()
        
        # Custom styles
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=14,
            spaceAfter=12,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        self.header_style = ParagraphStyle(
            'CustomHeader',
            parent=self.styles['Heading2'],
            fontSize=12,
            spaceAfter=10,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        self.body_style = ParagraphStyle(
            'CustomBody',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=6,
            alignment=TA_LEFT,
            fontName='Helvetica'
        )
    
    def generate_comparative_statement_pdf(self, work: Dict[str, Any], bidders: List[Dict[str, Any]]) -> bytes:
        """Generate comparative statement in PDF format."""
        
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=landscape(A4), 
                              rightMargin=15*mm, leftMargin=15*mm,
                              topMargin=15*mm, bottomMargin=15*mm)
        
        # Sort bidders by bid amount
        sorted_bidders = sorted(bidders, key=lambda x: x['bid_amount'])
        
        # Get work details
        work_name = work['work_name']
        nit_number = work['nit_number']
        work_info = work['work_info']
        estimated_cost = float(work_info['estimated_cost'])
        earnest_money = work_info['earnest_money']
        time_completion = work_info['time_of_completion']
        
        # Parse date
        original_date = work_info['date']
        parsed_date = self.date_utils.parse_date(original_date)
        formatted_date = self.date_utils.format_display_date(parsed_date) if parsed_date else original_date
        
        elements = []
        
        # Office header
        office_header = Paragraph("OFFICE OF THE EXECUTIVE ENGINEER PWD ELECTRIC DIVISION UDAIPUR", self.header_style)
        elements.append(office_header)
        elements.append(Spacer(1, 12))
        
        # Title
        title = Paragraph("<u>COMPARATIVE STATEMENT OF TENDER</u>", self.title_style)
        elements.append(title)
        elements.append(Spacer(1, 12))
        
        # Work details
        work_details = f"""
        <b>Name of Work:</b> {work_name}<br/>
        <b>NIT No.:</b> {nit_number} &nbsp;&nbsp;&nbsp;&nbsp; <b>Date:</b> {formatted_date}<br/>
        <b>Estimated Cost:</b> Rs. {estimated_cost:,.0f}/- &nbsp;&nbsp;&nbsp;&nbsp; 
        <b>Earnest Money:</b> Rs. {earnest_money} &nbsp;&nbsp;&nbsp;&nbsp;
        <b>Time of Completion:</b> {time_completion}
        """
        details_para = Paragraph(work_details, self.body_style)
        elements.append(details_para)
        elements.append(Spacer(1, 12))
        
        # Table data
        table_data = [
            ['S.No.', 'Name of Bidders', '% Above/Below', 'Amount (Rs.)', 'Tendered\nAmount (Rs.)', 'Remarks'],
            ['E', 'ESTIMATED COST', '-', f'{estimated_cost:,.0f}', f'{estimated_cost:,.0f}', '-']
        ]
        
        # Add bidder data
        for i, bidder in enumerate(sorted_bidders):
            row = [
                str(i + 1),
                bidder['name'],
                f"{bidder['percentage']:+.2f}%",
                f"{estimated_cost:,.0f}",
                f"{bidder['bid_amount']:,.0f}",
                'L1' if i == 0 else ''
            ]
            table_data.append(row)
        
        # Create table with adjusted column widths
        table = Table(table_data, colWidths=[30, 150, 70, 80, 90, 40])
        
        # Table style with borders
        table_style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, 1), colors.lightgrey),
            ('GRID', (0, 0), (-1, -1), 2, colors.black),
            ('BOX', (0, 0), (-1, -1), 3, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ])
        
        # Highlight L1 bidder row
        if len(sorted_bidders) > 0:
            table_style.add('BACKGROUND', (0, 2), (-1, 2), colors.lightgreen)
            table_style.add('FONTNAME', (0, 2), (-1, 2), 'Helvetica-Bold')
        
        table.setStyle(table_style)
        elements.append(table)
        elements.append(Spacer(1, 20))
        
        # Signature section
        signature_text = """
        <br/><br/><br/>
        Executive Engineer&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
        Assistant Engineer&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
        Junior Engineer<br/>
        PWD Electric Division&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
        PWD Electric Division&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
        PWD Electric Division<br/>
        Udaipur&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
        Udaipur&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
        Udaipur
        """
        signature_para = Paragraph(signature_text, self.body_style)
        elements.append(signature_para)
        
        # Build PDF
        doc.build(elements)
        
        pdf_data = buffer.getvalue()
        buffer.close()
        return pdf_data
    
    def generate_scrutiny_sheet_pdf(self, work: Dict[str, Any], bidders: List[Dict[str, Any]]) -> bytes:
        """Generate scrutiny sheet in PDF format."""
        
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, 
                              rightMargin=15*mm, leftMargin=15*mm,
                              topMargin=15*mm, bottomMargin=15*mm)
        
        # Sort bidders by bid amount
        sorted_bidders = sorted(bidders, key=lambda x: x['bid_amount'])
        lowest_bidder = sorted_bidders[0]
        
        # Get work details
        work_name = work['work_name']
        nit_number = work['nit_number']
        work_info = work['work_info']
        estimated_cost = float(work_info['estimated_cost'])
        
        # Parse date
        original_date = work_info['date']
        parsed_date = self.date_utils.parse_date(original_date)
        formatted_date = self.date_utils.format_display_date(parsed_date) if parsed_date else original_date
        
        elements = []
        
        # Title
        title = Paragraph("<u>Scrutiny Sheet of Tender</u>", self.title_style)
        elements.append(title)
        elements.append(Spacer(1, 20))
        
        # Table data
        table_data = [
            ['1', 'Head of Account', 'PWD Electric Works'],
            ['2', 'Name of work', f'{work_name}\nJob No. {nit_number}'],
            ['3', 'Reference of ADM. Sanction\nAmount in Rs.', f'As per administrative approval\nRs. {estimated_cost:.0f}/-'],
            ['4', 'Reference of technical sanction with amount', f'As per technical sanction for Rs. {estimated_cost:.0f}/-'],
            ['5', 'Date of calling NIT', formatted_date],
            ['6', 'Date of receipt of tender', formatted_date],
            ['7', 'Number of tenders received', str(len(bidders))],
            ['8', 'Date of opening of tender', formatted_date],
            ['9', 'Allotment of fund during the current financial year', 'Adequate.'],
            ['10', 'Expenditure up to last bill', 'Nil.'],
            ['11', 'Balance available for the work', f'Rs. {estimated_cost:.0f}/-'],
            ['12', 'Name of lowest tenderer', lowest_bidder['name']],
            ['13', 'Amount of lowest tender', f'Rs. {lowest_bidder["bid_amount"]:,.0f}/-'],
            ['14', 'Percentage above/below the estimate', f'{lowest_bidder["percentage"]:+.2f}%'],
            ['15', 'Recommendation', 'The tender may be accepted as per rules.']
        ]
        
        # Create table
        table = Table(table_data, colWidths=[20, 120, 180])
        
        # Table style with borders
        table_style = TableStyle([
            ('ALIGN', (0, 0), (0, -1), 'CENTER'),
            ('ALIGN', (1, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 2, colors.black),
            ('BOX', (0, 0), (-1, -1), 3, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ])
        
        table.setStyle(table_style)
        elements.append(table)
        elements.append(Spacer(1, 30))
        
        # Signature section
        signature_text = """
        <br/><br/><br/>
        <b>Executive Engineer<br/>
        PWD Electric Division<br/>
        Udaipur</b>
        """
        signature_para = Paragraph(signature_text, 
                                 ParagraphStyle('Signature', parent=self.body_style, 
                                              alignment=TA_CENTER, fontSize=14, fontName='Helvetica-Bold'))
        elements.append(signature_para)
        
        # Build PDF
        doc.build(elements)
        
        pdf_data = buffer.getvalue()
        buffer.close()
        return pdf_data
    
    def generate_letter_of_acceptance_pdf(self, work: Dict[str, Any], bidders: List[Dict[str, Any]]) -> bytes:
        """Generate Letter of Acceptance in PDF format."""
        
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, 
                              rightMargin=15*mm, leftMargin=15*mm,
                              topMargin=15*mm, bottomMargin=15*mm)
        
        # Sort bidders and get L1
        sorted_bidders = sorted(bidders, key=lambda x: x['bid_amount'])
        l1_bidder = sorted_bidders[0]
        
        # Get work details
        work_name = work['work_name']
        nit_number = work['nit_number']
        work_info = work['work_info']
        estimated_cost = float(work_info['estimated_cost'])
        
        # Parse date
        original_date = work_info['date']
        parsed_date = self.date_utils.parse_date(original_date)
        formatted_date = self.date_utils.format_display_date(parsed_date) if parsed_date else original_date
        
        # Calculate stipulated start date (current date + 1 day)
        start_date = self.date_utils.add_days(datetime.now(), 1)
        start_date_str = self.date_utils.format_display_date(start_date)
        
        elements = []
        
        # Office header
        office_header = Paragraph("OFFICE OF THE EXECUTIVE ENGINEER PWD ELECTRIC DIVISION UDAIPUR", self.header_style)
        elements.append(office_header)
        elements.append(Spacer(1, 20))
        
        # Title (centered)
        title = Paragraph("<u>LETTER OF ACCEPTANCE</u>", self.title_style)
        elements.append(title)
        elements.append(Spacer(1, 20))
        
        # Letter content
        letter_content = f"""
        To,<br/>
        <b>{l1_bidder['name']}</b><br/>
        {l1_bidder.get('address', 'Address on file')}<br/><br/>
        
        Subject: Letter of Acceptance for {work_name}<br/>
        Reference: NIT No. {nit_number} dated {formatted_date}<br/><br/>
        
        Sir,<br/><br/>
        
        With reference to your tender dated {formatted_date} for the above mentioned work, 
        I am pleased to inform you that your tender has been accepted for Rs. {l1_bidder['bid_amount']:,.0f}/- 
        ({l1_bidder['percentage']:+.2f}% of estimated cost).<br/><br/>
        
        You are hereby directed to commence the work immediately and complete the same within 
        the stipulated period as per the terms and conditions of the contract.<br/><br/>
        
        The work should be commenced from {start_date_str}.<br/><br/>
        
        Please acknowledge receipt of this letter and submit the required security deposit 
        and other documents as per the contract agreement.<br/><br/>
        
        Yours faithfully,<br/><br/><br/><br/>
        
        <b>Executive Engineer<br/>
        PWD Electric Division<br/>
        Udaipur</b><br/><br/>
        
        Date: {self.date_utils.get_current_date()}
        """
        
        letter_para = Paragraph(letter_content, self.body_style)
        elements.append(letter_para)
        
        # Build PDF
        doc.build(elements)
        
        pdf_data = buffer.getvalue()
        buffer.close()
        return pdf_data
    
    def generate_work_order_pdf(self, work: Dict[str, Any], bidders: List[Dict[str, Any]]) -> bytes:
        """Generate Work Order in PDF format."""
        
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, 
                              rightMargin=15*mm, leftMargin=15*mm,
                              topMargin=15*mm, bottomMargin=15*mm)
        
        # Sort bidders and get L1
        sorted_bidders = sorted(bidders, key=lambda x: x['bid_amount'])
        l1_bidder = sorted_bidders[0]
        
        # Get work details
        work_name = work['work_name']
        nit_number = work['nit_number']
        work_info = work['work_info']
        estimated_cost = float(work_info['estimated_cost'])
        time_completion = work_info['time_of_completion']
        
        # Parse date
        original_date = work_info['date']
        parsed_date = self.date_utils.parse_date(original_date)
        formatted_date = self.date_utils.format_display_date(parsed_date) if parsed_date else original_date
        
        # Calculate stipulated start date (current date + 1 day)
        start_date = self.date_utils.add_days(datetime.now(), 1)
        start_date_str = self.date_utils.format_display_date(start_date)
        
        elements = []
        
        # Office header
        office_header = Paragraph("OFFICE OF THE EXECUTIVE ENGINEER PWD ELECTRIC DIVISION UDAIPUR", self.header_style)
        elements.append(office_header)
        elements.append(Spacer(1, 20))
        
        # Title (centered)
        title = Paragraph("<u>WORK ORDER</u>", self.title_style)
        elements.append(title)
        elements.append(Spacer(1, 20))
        
        # Work order content
        work_order_content = f"""
        Work Order No.: WO/{nit_number}/{datetime.now().year}<br/>
        Date: {self.date_utils.get_current_date()}<br/><br/>
        
        To,<br/>
        <b>{l1_bidder['name']}</b><br/>
        {l1_bidder.get('address', 'Address on file')}<br/><br/>
        
        Subject: Work Order for {work_name}<br/>
        Reference: NIT No. {nit_number} dated {formatted_date}<br/><br/>
        
        Sir,<br/><br/>
        
        You are hereby directed to execute the following work as per the terms and conditions 
        of the contract:<br/><br/>
        
        <b>Work Details:</b><br/>
        Name of Work: {work_name}<br/>
        Contract Amount: Rs. {l1_bidder['bid_amount']:,.0f}/-<br/>
        Time of Completion: {time_completion}<br/>
        Stipulated Date of Start: {start_date_str}<br/>
        Earnest Money: Rs. {l1_bidder['earnest_money']}<br/><br/>
        
        You are directed to commence the work immediately and complete the same within 
        the stipulated time as per the agreement.<br/><br/>
        
        All terms and conditions as per the tender document and contract agreement 
        shall be applicable.<br/><br/>
        
        This work order is issued subject to the fulfillment of all contractual 
        obligations including submission of required security deposit.<br/><br/>
        
        Yours faithfully,<br/><br/><br/><br/>
        
        <b>Executive Engineer<br/>
        PWD Electric Division<br/>
        Udaipur</b>
        """
        
        work_order_para = Paragraph(work_order_content, self.body_style)
        elements.append(work_order_para)
        
        # Build PDF
        doc.build(elements)
        
        pdf_data = buffer.getvalue()
        buffer.close()
        return pdf_data
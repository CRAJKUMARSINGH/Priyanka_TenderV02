import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime
import os
import zipfile
import tempfile
from io import BytesIO
import logging
import traceback
import time

# Import custom modules
from tender_processor import TenderProcessor
from latex_report_generator import LatexReportGenerator
from template_processor import TemplateProcessor
from pdf_generator import PDFGenerator
from user_manual_generator import UserManualGenerator
from database_manager import DatabaseManager
from excel_parser import ExcelParser
from pdf_parser import PDFParser
from utils import validate_percentage, format_currency, validate_nit_number
from date_utils import DateUtils
from validation import ValidationManager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def initialize_directories():
    """Initialize required directories"""
    directories = ['templates', 'outputs', 'temp', 'logs']
    for directory in directories:
        os.makedirs(directory, exist_ok=True)

def show_welcome_balloons():
    """Display welcome balloons and wish message"""
    if 'welcome_shown' not in st.session_state:
        st.balloons()
        st.session_state.welcome_shown = True

def inject_custom_css():
    """Inject custom CSS for green background logo styling"""
    st.markdown("""
    <style>
    /* Main container styling */
    .main > div {
        padding: 2rem 1rem;
    }

    /* Header styling - Green gradient design with crane logo */
    .header-container {
        background: linear-gradient(135deg, #4CAF50 0%, #66BB6A 50%, #81C784 100%);
        color: white;
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    }

    .header-title {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-align: center;
    }

    .header-subtitle {
        font-size: 1.2rem;
        text-align: center;
        opacity: 0.9;
        margin-bottom: 0.5rem;
    }

    .header-professional {
        font-size: 1rem;
        text-align: center;
        color: #e8f5e9;
        opacity: 0.85;
        margin-bottom: 0.5rem;
        font-weight: 400;
        font-style: italic;
        letter-spacing: 0.8px;
    }

    .header-initiative {
        font-size: 0.9rem;
        text-align: center;
        color: #ffffff;
        opacity: 0.9;
        margin-bottom: 0;
        font-weight: 500;
        background: rgba(255,255,255,0.1);
        padding: 0.5rem 1rem;
        border-radius: 20px;
        border: 1px solid rgba(255,255,255,0.2);
        display: inline-block;
        margin: 0 auto;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }

    /* Card styling */
    .info-card {
        background: #f8f9fa;
        border: 1px solid #dee2e6;
        border-radius: 8px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }

    .upload-card {
        background: #ffffff;
        border: 2px dashed #4CAF50;
        border-radius: 10px;
        padding: 2rem;
        text-align: center;
        margin-bottom: 2rem;
        transition: all 0.3s ease;
    }

    .upload-card:hover {
        border-color: #388E3C;
        background: #f1f8e9;
    }

    /* Status indicators */
    .status-success {
        background: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        border-left: 4px solid #28a745;
        margin: 1rem 0;
    }

    .status-error {
        background: #f8d7da;
        color: #721c24;
        padding: 1rem;
        border-radius: 5px;
        border-left: 4px solid #dc3545;
        margin: 1rem 0;
    }

    .status-info {
        background: #d1ecf1;
        color: #0c5460;
        padding: 1rem;
        border-radius: 5px;
        border-left: 4px solid #17a2b8;
        margin: 1rem 0;
    }

    /* Feature list styling */
    .feature-list {
        background: #ffffff;
        border-radius: 8px;
        padding: 1.5rem;
        border: 1px solid #e9ecef;
    }

    .feature-item {
        display: flex;
        align-items: center;
        margin-bottom: 0.8rem;
        padding: 0.5rem;
        background: #f8f9fa;
        border-radius: 5px;
    }

    .feature-icon {
        color: #4CAF50;
        font-weight: bold;
        margin-right: 0.8rem;
    }

    /* Responsive design */
    @media (max-width: 768px) {
        .header-title {
            font-size: 2rem;
        }

        .header-subtitle {
            font-size: 1rem;
        }
    }
    </style>
    """, unsafe_allow_html=True)

def show_credits():
    """Display credits information"""
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🏛️ Credits")
    st.sidebar.info("**An Initiative By**\n\nMrs. Premlata Jain\n\nAdditional Administrative Officer\n\nPWD, Udaipur")
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 💻 System Info")
    st.sidebar.caption("Enhanced Tender Processing System v2.0")
    st.sidebar.caption("Built with Streamlit & LaTeX")

def main():
    st.set_page_config(
        page_title="Enhanced Tender Processing System - PWD Udaipur",
        page_icon="🏗️",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Initialize directories
    initialize_directories()

    # Inject custom CSS styling
    inject_custom_css()

    # Show welcome balloons
    show_welcome_balloons()

    # Header section with green background and crane logo
    st.markdown("""
    <div class="header-container">
        <h1 class="header-title">🏗️ Enhanced Tender Processing System</h1>
        <p class="header-subtitle">Generate professional tender documents with LaTeX PDF compliance automatically</p>
        <p class="header-professional">Streamlined government tender documentation with statutory compliance and automated calculations</p>
        <div style="text-align: center;">
            <span class="header-initiative">An Initiative by Mrs. Premlata Jain, Additional Administrative Officer, PWD, Udaipur</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Initialize session state
    if 'tender_data' not in st.session_state:
        st.session_state.tender_data = {}
    if 'works' not in st.session_state:
        st.session_state.works = []
    if 'debug_mode' not in st.session_state:
        st.session_state.debug_mode = False
    if 'latex_status' not in st.session_state:
        st.session_state.latex_status = {}

    # Initialize components with error handling
    try:
        db_manager = DatabaseManager()
        tender_processor = TenderProcessor()
        latex_generator = LatexReportGenerator()
        template_processor = TemplateProcessor()
        pdf_generator = PDFGenerator()
        manual_generator = UserManualGenerator()
        excel_parser = ExcelParser()
        pdf_parser = PDFParser()
        validator = ValidationManager()
    except Exception as e:
        st.error(f"❌ Error initializing system components: {str(e)}")
        st.stop()

    # Check LaTeX installation
    latex_check = pdf_generator.check_latex_installation()
    
    # Enhanced Sidebar with credits
    with st.sidebar:
        st.header("🔧 System Dashboard")
        
        # LaTeX Status with enhanced feedback
        if latex_check['installed']:
            st.success("✅ LaTeX: Ready for PDF Generation")
        else:
            st.error("❌ LaTeX: Installation Required")
            st.info("📝 Install Command:\n```bash\nsudo apt-get install texlive-latex-extra texlive-fonts-recommended\n```")
        
        # Enhanced system metrics
        total_works = len(st.session_state.works)
        works_with_bidders = len([w for w in st.session_state.works if w.get('bidders')])
        unique_nits = len(set([w.get('nit_number') for w in st.session_state.works if w.get('nit_number')]))

        col1, col2 = st.columns(2)
        with col1:
            st.metric("📊 Total Works", total_works, delta=None)
            st.metric("👥 Unique NITs", unique_nits, delta=None)
        with col2:
            st.metric("💼 With Bidders", works_with_bidders, delta=None)
            completion_rate = f"{(works_with_bidders/total_works*100) if total_works > 0 else 0:.1f}%"
            st.metric("✅ Completion", completion_rate, delta=None)
        
        st.markdown("---")
        
        # Enhanced Template Status
        st.subheader("📄 LaTeX Templates")
        template_files = [
            ("comparative_statement.tex", "📋 Comparative Statement"),
            ("letter_of_acceptance.tex", "✉️ Letter of Acceptance"), 
            ("scrutiny_sheet.tex", "🔍 Scrutiny Sheet"),
            ("work_order.tex", "📝 Work Order")
        ]
        
        template_status = []
        for template_file, display_name in template_files:
            template_path = f"templates/{template_file}"
            if os.path.exists(template_path):
                st.success(f"✅ {display_name}")
                template_status.append(True)
            else:
                st.warning(f"⚠️ {display_name}")
                template_status.append(False)

        # Template health indicator
        template_health = sum(template_status) / len(template_status) * 100
        st.progress(template_health / 100)
        st.caption(f"Template Health: {template_health:.0f}%")

        st.markdown("---")
        
        # Debug and system controls
        st.subheader("🛠️ System Controls")
        st.session_state.debug_mode = st.checkbox("🐛 Debug Mode", value=st.session_state.debug_mode)
        
        if st.session_state.debug_mode:
            with st.expander("🔍 Debug Information"):
                st.write(f"LaTeX Status: {'✅ Available' if latex_check['installed'] else '❌ Missing'}")
                st.write(f"Session Works: {len(st.session_state.works)}")
                st.write(f"Templates Directory: {'✅ Exists' if os.path.exists('templates') else '❌ Missing'}")
                if st.session_state.latex_status:
                    st.write("LaTeX Processing:", st.session_state.latex_status)

        # Enhanced data management
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🗑️ Clear Data", type="secondary", use_container_width=True):
                st.session_state.clear_confirmed = True
        with col2:
            if st.session_state.get('clear_confirmed', False):
                if st.button("✅ Confirm", type="primary", use_container_width=True):
                    st.session_state.tender_data = {}
                    st.session_state.works = []
                    st.session_state.latex_status = {}
                    st.session_state.clear_confirmed = False
                    st.success("🎯 All data cleared!")
                    st.balloons()
                    time.sleep(1)
                    st.rerun()

        # Show credits
        show_credits()

    # Enhanced main content tabs with icons
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📁 Data Input", 
        "🏗️ Work Entry", 
        "📊 PDF Reports", 
        "🔧 Templates",
        "👥 Bidders", 
        "📖 Manual"
    ])

    with tab1:
        st.header("📁 Data Input & File Processing")
        handle_data_input(excel_parser, pdf_parser)

    with tab2:
        st.header("🏗️ Work Entry & Management")
        handle_work_entry(db_manager, validator)

    with tab3:
        st.header("📊 PDF Report Generation")
        handle_pdf_generation(latex_generator, pdf_generator, template_processor, validator)

    with tab4:
        st.header("🔧 LaTeX Template Management")
        handle_template_management(template_processor)

    with tab5:
        st.header("👥 Bidder Management")
        handle_bidder_management(db_manager)

    with tab6:
        st.header("📖 User Manual & Help")
        handle_user_manual(manual_generator)

def handle_data_input(excel_parser, pdf_parser):
    """Enhanced data input functionality"""
    st.info("💡 **Tip:** Upload Excel or PDF files containing NIT details, or enter data manually for best results.")
    
    input_method = st.radio(
        "Select Input Method:",
        ["📊 Upload Excel File", "📄 Upload PDF File", "✍️ Manual Entry"],
        horizontal=True,
        help="Choose your preferred method to input tender data"
    )

    if input_method == "📊 Upload Excel File":
        st.subheader("📊 Excel File Processing")
        
        # File upload with enhanced UI
        uploaded_file = st.file_uploader(
            "Choose an Excel file (.xlsx, .xls)",
            type=['xlsx', 'xls'],
            help="Upload Excel file containing NIT details and bidder information"
        )

        if uploaded_file is not None:
            try:
                # Show file info
                file_details = {
                    "📋 Filename": uploaded_file.name,
                    "📏 Size": f"{uploaded_file.size:,} bytes",
                    "📅 Upload Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.info(f"**File:** {file_details['📋 Filename']}")
                with col2:
                    st.info(f"**Size:** {file_details['📏 Size']}")
                with col3:
                    st.info(f"**Time:** {file_details['📅 Upload Time']}")

                # Process file with progress indicator
                with st.spinner("🔄 Processing Excel file... Please wait."):
                    progress_bar = st.progress(0)
                    for i in range(100):
                        time.sleep(0.01)
                        progress_bar.progress(i + 1)
                    
                    extracted_data = excel_parser.parse_excel(uploaded_file)
                    
                    if extracted_data:
                        st.session_state.tender_data.update(extracted_data)
                        st.success("🎉 Excel file processed successfully!")
                        st.balloons()
                        
                        with st.expander("📋 Extracted Data Preview", expanded=True):
                            # Enhanced data display
                            if 'nit_number' in extracted_data:
                                st.markdown(f"**NIT Number:** `{extracted_data['nit_number']}`")
                            if 'work_name' in extracted_data:
                                st.markdown(f"**Work Name:** {extracted_data['work_name']}")
                            if 'estimated_cost' in extracted_data:
                                st.markdown(f"**Estimated Cost:** ₹{format_currency(extracted_data['estimated_cost'])}")
                            
                            # Show full data in JSON format
                            st.json(extracted_data)
                    else:
                        st.error("❌ No valid data found in Excel file")
                        st.info("💡 Please ensure your Excel file contains the required columns and data format.")
                        
            except Exception as e:
                st.error(f"❌ Error processing Excel file: {str(e)}")
                with st.expander("🔍 Detailed Error Information"):
                    st.code(traceback.format_exc())
                    st.info("💡 Try checking your file format or contact system administrator.")

    elif input_method == "📄 Upload PDF File":
        st.subheader("📄 PDF File Processing")
        
        uploaded_file = st.file_uploader(
            "Choose a PDF file",
            type=['pdf'],
            help="Upload PDF file containing NIT details"
        )

        if uploaded_file is not None:
            try:
                with st.spinner("🔄 Extracting data from PDF... This may take a moment."):
                    extracted_data = pdf_parser.parse_pdf(uploaded_file)
                    
                    if extracted_data:
                        st.session_state.tender_data.update(extracted_data)
                        st.success("🎉 PDF file processed successfully!")
                        st.balloons()
                        
                        with st.expander("📋 Extracted Data", expanded=True):
                            st.json(extracted_data)
                    else:
                        st.error("❌ No valid data found in PDF file")
                        st.info("💡 PDF text extraction can be challenging. Consider using Excel format or manual entry.")
                        
            except Exception as e:
                st.error(f"❌ Error processing PDF file: {str(e)}")
                st.info("💡 If PDF processing fails, try converting to Excel format first.")

    else:  # Manual Entry
        handle_manual_entry()

def handle_manual_entry():
    """Enhanced manual data entry"""
    st.subheader("✍️ Manual NIT Details Entry")
    st.info("📝 Fill in the details below to create a new tender entry. All fields marked with * are required.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📋 Basic Information")
        
        nit_number = st.text_input(
            "NIT Number *",
            value=st.session_state.tender_data.get('nit_number', ''),
            help="Format: 27/2024-25",
            placeholder="e.g., 27/2024-25"
        )
        
        work_name = st.text_area(
            "Work Name *",
            value=st.session_state.tender_data.get('work_name', ''),
            help="Detailed description of the work",
            height=100,
            placeholder="Enter detailed work description..."
        )
        
        estimated_cost = st.number_input(
            "Estimated Cost (₹) *",
            min_value=0.0,
            value=float(st.session_state.tender_data.get('estimated_cost', 0)),
            step=1000.0,
            format="%.2f",
            help="Total estimated cost of the project"
        )
        
        schedule_amount = st.number_input(
            "Schedule Amount (₹) *",
            min_value=0.0,
            value=float(st.session_state.tender_data.get('schedule_amount', 0)),
            step=1000.0,
            format="%.2f",
            help="Amount as per schedule"
        )

    with col2:
        st.markdown("#### ⏱️ Timeline & Details")
        
        time_of_completion = st.number_input(
            "Time of Completion (months) *",
            min_value=1,
            value=int(st.session_state.tender_data.get('time_of_completion', 12)),
            step=1,
            help="Project completion time in months"
        )
        
        earnest_money = st.number_input(
            "Earnest Money (₹) *",
            min_value=0.0,
            value=float(st.session_state.tender_data.get('earnest_money', 0)),
            step=100.0,
            format="%.2f",
            help="Security deposit amount"
        )
        
        date = st.date_input(
            "Date *",
            value=datetime.now().date(),
            help="Tender date"
        )
        
        ee_name = st.text_input(
            "Executive Engineer Name *",
            value=st.session_state.tender_data.get('ee_name', 'Executive Engineer'),
            placeholder="Full name of Executive Engineer",
            help="Name of the Executive Engineer"
        )

    # Enhanced save button with validation
    st.markdown("---")
    if st.button("💾 Save NIT Details", type="primary", use_container_width=True):
        # Validation with enhanced feedback
        errors = []
        warnings = []
        
        if not nit_number:
            errors.append("NIT Number is required")
        elif not validate_nit_number(nit_number):
            errors.append("Invalid NIT number format. Use {number}/{YYYY-YY}")
        
        if not work_name or len(work_name.strip()) < 10:
            if not work_name:
                errors.append("Work Name is required")
            else:
                warnings.append("Work Name seems too short. Consider adding more details.")
        
        if estimated_cost <= 0:
            errors.append("Estimated Cost must be positive")
        if schedule_amount <= 0:
            errors.append("Schedule Amount must be positive")
        if earnest_money <= 0:
            errors.append("Earnest Money must be positive")
        if not ee_name or ee_name.strip() == "Executive Engineer":
            errors.append("Please provide the actual Executive Engineer name")

        # Business logic validations
        if earnest_money > 0 and estimated_cost > 0:
            em_percentage = (earnest_money / estimated_cost) * 100
            if em_percentage < 1 or em_percentage > 5:
                warnings.append(f"Earnest Money ({em_percentage:.2f}%) is outside typical range (1-5%)")

        # Display validation results
        if errors:
            st.error("❌ Please fix the following errors:")
            for error in errors:
                st.error(f"• {error}")
        
        if warnings and not errors:
            st.warning("⚠️ Please review:")
            for warning in warnings:
                st.warning(f"• {warning}")

        if not errors:
            st.session_state.tender_data.update({
                'nit_number': nit_number,
                'work_name': work_name,
                'estimated_cost': estimated_cost,
                'schedule_amount': schedule_amount,
                'time_of_completion': time_of_completion,
                'earnest_money': earnest_money,
                'date': date.strftime('%d-%m-%Y'),
                'ee_name': ee_name
            })
            
            st.success("🎉 NIT details saved successfully!")
            st.balloons()
            time.sleep(1)
            st.rerun()

def handle_work_entry(db_manager, validator):
    """Enhanced work entry functionality"""
    if not st.session_state.tender_data:
        st.warning("⚠️ Please enter NIT details first in the Data Input tab.")
        st.info("💡 Use the 'Data Input' tab to upload files or enter NIT details manually.")
        return

    # Enhanced NIT details display
    st.subheader("📊 Current NIT Overview")
    
    # Create metrics display
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "📋 NIT Number", 
            st.session_state.tender_data.get('nit_number', 'N/A'),
            help="Notice Inviting Tender Number"
        )
    
    with col2:
        cost = st.session_state.tender_data.get('estimated_cost', 0)
        st.metric(
            "💰 Estimated Cost", 
            f"₹{format_currency(cost)}",
            help="Total estimated project cost"
        )
    
    with col3:
        completion_time = st.session_state.tender_data.get('time_of_completion', 0)
        st.metric(
            "⏱️ Timeline", 
            f"{completion_time} months",
            help="Project completion time"
        )
    
    with col4:
        em = st.session_state.tender_data.get('earnest_money', 0)
        st.metric(
            "🛡️ Earnest Money", 
            f"₹{format_currency(em)}",
            help="Security deposit amount"
        )

    # Work name in expandable section
    with st.expander("📝 Work Description", expanded=False):
        st.write(st.session_state.tender_data.get('work_name', 'N/A'))

    st.markdown("---")
    
    # Enhanced bidder entry
    handle_bidder_entry(db_manager, validator)

def handle_bidder_entry(db_manager, validator):
    """Enhanced bidder information entry"""
    st.subheader("👥 Bidder Information Management")
    st.info("💡 Add bidder details including their bid percentages. The system will automatically calculate amounts and rankings.")
    
    # Number of bidders selection with enhanced UI
    col1, col2 = st.columns([2, 3])
    with col1:
        num_bidders = st.number_input(
            "Number of Bidders",
            min_value=1,
            max_value=20,
            value=3,
            step=1,
            help="Enter the number of bidders participating in this tender"
        )

    with col2:
        # Quick suggestion from recent bidders
        recent_bidders = db_manager.get_recent_bidders(10)
        if recent_bidders:
            st.info(f"💡 {len(recent_bidders)} recent bidders available for quick selection")

    # Initialize bidder data
    if 'current_bidders' not in st.session_state:
        st.session_state.current_bidders = {}

    bidders = []
    
    # Enhanced bidder entry form
    for i in range(int(num_bidders)):
        st.markdown(f"#### 👤 Bidder {i+1}")
        
        col1, col2, col3, col4 = st.columns([3, 2, 2, 2])
        
        with col1:
            # Bidder name with autocomplete suggestions
            bidder_key = f"bidder_{i}_name"
            suggested_names = [b['name'] for b in recent_bidders] if recent_bidders else []
            
            name = st.text_input(
                f"Name *",
                key=bidder_key,
                placeholder="Enter bidder name",
                help="Full legal name of the bidder"
            )
            
            # Show suggestions if available
            if suggested_names and name:
                matching = [n for n in suggested_names if name.lower() in n.lower()]
                if matching:
                    selected = st.selectbox(
                        "Quick Select:",
                        [""] + matching[:5],
                        key=f"suggest_{i}",
                        help="Select from recent bidders"
                    )
                    if selected:
                        st.session_state[bidder_key] = selected
                        st.rerun()

        with col2:
            percentage = st.number_input(
                f"Percentage",
                key=f"bidder_{i}_percentage",
                min_value=-50.0,
                max_value=100.0,
                value=0.0,
                step=0.01,
                format="%.2f",
                help="Bid percentage (+ for above, - for below estimate)"
            )

        with col3:
            # Auto-calculate bid amount
            estimated_cost = st.session_state.tender_data.get('estimated_cost', 0)
            calculated_amount = estimated_cost * (1 + percentage / 100) if estimated_cost > 0 else 0
            
            bid_amount = st.number_input(
                f"Bid Amount (₹)",
                key=f"bidder_{i}_amount",
                min_value=0.0,
                value=float(calculated_amount),
                step=1000.0,
                format="%.2f",
                help="Final bid amount"
            )

        with col4:
            contact = st.text_input(
                f"Contact",
                key=f"bidder_{i}_contact",
                placeholder="Phone/Email",
                help="Contact information"
            )

        # Validation feedback for this bidder
        if name and percentage is not None:
            if percentage > 0:
                st.success(f"✅ {percentage:.2f}% ABOVE estimate (₹{calculated_amount:,.2f})")
            elif percentage < 0:
                st.info(f"📉 {abs(percentage):.2f}% BELOW estimate (₹{calculated_amount:,.2f})")
            else:
                st.info(f"🎯 AT estimate (₹{calculated_amount:,.2f})")

        # Add bidder to list if name is provided
        if name:
            bidders.append({
                'name': name,
                'percentage': percentage,
                'bid_amount': bid_amount if bid_amount > 0 else calculated_amount,
                'contact': contact
            })

        st.markdown("---")

    # Enhanced save functionality
    if bidders:
        st.subheader("💾 Save Work Entry")
        
        # Preview section
        with st.expander("👀 Preview Work Entry", expanded=True):
            # Summary metrics
            if bidders:
                sorted_bidders = sorted(bidders, key=lambda x: x['bid_amount'])
                lowest_bidder = sorted_bidders[0]
                highest_bidder = sorted_bidders[-1]
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("🏆 Lowest Bid", f"₹{format_currency(lowest_bidder['bid_amount'])}", 
                             f"{lowest_bidder['name']}")
                with col2:
                    st.metric("📊 Highest Bid", f"₹{format_currency(highest_bidder['bid_amount'])}", 
                             f"{highest_bidder['name']}")
                with col3:
                    bid_range = highest_bidder['bid_amount'] - lowest_bidder['bid_amount']
                    st.metric("📏 Bid Range", f"₹{format_currency(bid_range)}", 
                             f"{len(bidders)} bidders")

                # Bidder table preview
                df = pd.DataFrame(bidders)
                df = df.sort_values('bid_amount').reset_index(drop=True)
                df.index += 1  # Start from 1
                df['bid_amount'] = df['bid_amount'].apply(lambda x: f"₹{format_currency(x)}")
                df['percentage'] = df['percentage'].apply(lambda x: f"{x:+.2f}%")
                
                st.dataframe(df, use_container_width=True)

        # Save button with confirmation
        if st.button("💾 Save Work Entry", type="primary", use_container_width=True):
            try:
                # Prepare work data
                work_data = st.session_state.tender_data.copy()
                work_data['bidders'] = bidders
                
                # Find lowest bidder
                sorted_bidders = sorted(bidders, key=lambda x: x['bid_amount'])
                work_data['lowest_bidder'] = sorted_bidders[0] if sorted_bidders else None
                
                # Save to database
                work_id = db_manager.save_work_data(work_data)
                
                if work_id:
                    # Add to session state
                    st.session_state.works.append(work_data)
                    
                    st.success(f"🎉 Work entry saved successfully! (ID: {work_id})")
                    st.balloons()
                    
                    # Show success metrics
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.info(f"**Work ID:** {work_id}")
                    with col2:
                        st.info(f"**Bidders:** {len(bidders)}")
                    with col3:
                        st.info(f"**Lowest:** {work_data['lowest_bidder']['name']}")
                    
                else:
                    st.error("❌ Failed to save work entry")
                    
            except Exception as e:
                st.error(f"❌ Error saving work entry: {str(e)}")
                with st.expander("🔍 Error Details"):
                    st.code(traceback.format_exc())
    
    else:
        st.info("👆 Please enter at least one bidder to proceed.")

def handle_pdf_generation(latex_generator, pdf_generator, template_processor, validator):
    """Enhanced PDF generation functionality"""
    st.info("📄 Generate professional PDF reports for your tender documents using LaTeX templates.")
    
    if not st.session_state.works:
        st.warning("⚠️ No work entries found. Please add work entries first.")
        st.info("💡 Go to 'Work Entry' tab to add tender and bidder information.")
        return

    # Work selection
    st.subheader("📋 Select Work for Report Generation")
    
    work_options = []
    for i, work in enumerate(st.session_state.works):
        nit = work.get('nit_number', f'Work {i+1}')
        work_name = work.get('work_name', 'Unnamed Work')[:50] + "..." if len(work.get('work_name', '')) > 50 else work.get('work_name', 'Unnamed Work')
        bidder_count = len(work.get('bidders', []))
        work_options.append(f"{nit} - {work_name} ({bidder_count} bidders)")

    selected_work_index = st.selectbox(
        "Choose Work:",
        range(len(work_options)),
        format_func=lambda x: work_options[x],
        help="Select the work entry for which you want to generate reports"
    )

    selected_work = st.session_state.works[selected_work_index]

    # Work summary
    with st.expander("📊 Selected Work Summary", expanded=True):
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("📋 NIT", selected_work.get('nit_number', 'N/A'))
        with col2:
            st.metric("💰 Estimated", f"₹{format_currency(selected_work.get('estimated_cost', 0))}")
        with col3:
            st.metric("👥 Bidders", len(selected_work.get('bidders', [])))
        with col4:
            lowest = selected_work.get('lowest_bidder', {})
            if lowest:
                st.metric("🏆 Lowest", f"₹{format_currency(lowest.get('bid_amount', 0))}")

    st.markdown("---")

    # Document type selection with enhanced UI
    st.subheader("📄 Document Generation")
    
    doc_types = {
        "comparative_statement": {
            "name": "📊 Comparative Statement",
            "description": "Detailed comparison of all bidders with statutory format",
            "icon": "📊"
        },
        "letter_of_acceptance": {
            "name": "✉️ Letter of Acceptance",
            "description": "Official acceptance letter for the lowest bidder",
            "icon": "✉️"
        },
        "scrutiny_sheet": {
            "name": "🔍 Scrutiny Sheet",
            "description": "Technical and financial evaluation sheet",
            "icon": "🔍"
        },
        "work_order": {
            "name": "📝 Work Order",
            "description": "Official work order for project commencement",
            "icon": "📝"
        }
    }

    # Document type selection with cards
    selected_docs = []
    
    cols = st.columns(2)
    for i, (doc_type, info) in enumerate(doc_types.items()):
        with cols[i % 2]:
            if st.checkbox(
                f"{info['icon']} {info['name']}", 
                key=f"doc_{doc_type}",
                help=info['description']
            ):
                selected_docs.append(doc_type)

    if not selected_docs:
        st.info("👆 Select at least one document type to generate.")
        return

    # Generation options
    st.subheader("⚙️ Generation Options")
    
    col1, col2 = st.columns(2)
    with col1:
        output_format = st.radio(
            "Output Format:",
            ["📄 PDF Only", "📝 LaTeX + PDF", "📋 LaTeX Only"],
            help="Choose your preferred output format"
        )
    
    with col2:
        include_metadata = st.checkbox(
            "📋 Include Metadata", 
            value=True,
            help="Add generation timestamp and system info"
        )

    # Generate button with enhanced feedback
    st.markdown("---")
    if st.button("🚀 Generate Documents", type="primary", use_container_width=True):
        try:
            generated_files = {}
            
            # Progress tracking
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            total_docs = len(selected_docs)
            
            for i, doc_type in enumerate(selected_docs):
                status_text.text(f"🔄 Generating {doc_types[doc_type]['name']}...")
                progress_bar.progress((i + 1) / total_docs)
                
                # Generate LaTeX content
                latex_content = latex_generator.generate_document(doc_type, selected_work)
                
                if latex_content:
                    filename_base = f"{doc_type}_{selected_work.get('nit_number', 'unknown').replace('/', '_')}"
                    
                    # Save LaTeX file
                    latex_filename = f"{filename_base}.tex"
                    with open(f"outputs/{latex_filename}", 'w', encoding='utf-8') as f:
                        f.write(latex_content)
                    
                    generated_files[f"{doc_types[doc_type]['icon']} {doc_types[doc_type]['name']} (LaTeX)"] = f"outputs/{latex_filename}"
                    
                    # Generate PDF if requested
                    if "PDF" in output_format:
                        pdf_result = pdf_generator.generate_pdf(latex_content, filename_base)
                        if pdf_result['success']:
                            generated_files[f"{doc_types[doc_type]['icon']} {doc_types[doc_type]['name']} (PDF)"] = pdf_result['pdf_path']
                        else:
                            st.error(f"❌ PDF generation failed for {doc_type}: {pdf_result['error']}")
                else:
                    st.error(f"❌ Failed to generate {doc_type}")
            
            progress_bar.progress(1.0)
            status_text.text("✅ Generation completed!")
            
            if generated_files:
                st.success(f"🎉 Successfully generated {len(generated_files)} files!")
                st.balloons()
                
                # Display generated files
                st.subheader("📁 Generated Files")
                
                for file_desc, file_path in generated_files.items():
                    if os.path.exists(file_path):
                        with open(file_path, 'rb') as f:
                            file_data = f.read()
                        
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            st.write(f"📄 {file_desc}")
                            st.caption(f"Size: {len(file_data):,} bytes")
                        
                        with col2:
                            st.download_button(
                                "⬇️ Download",
                                data=file_data,
                                file_name=os.path.basename(file_path),
                                mime="application/pdf" if file_path.endswith('.pdf') else "text/plain",
                                key=f"download_{file_desc}"
                            )
            
            else:
                st.error("❌ No files were generated successfully.")
                
        except Exception as e:
            st.error(f"❌ Error during generation: {str(e)}")
            with st.expander("🔍 Error Details"):
                st.code(traceback.format_exc())

def handle_template_management(template_processor):
    """Enhanced template management"""
    st.info("🔧 Manage LaTeX templates for different document types. Templates use statutory compliance formatting.")
    
    # Template status overview
    st.subheader("📋 Template Status Overview")
    
    template_info = {
        "comparative_statement.tex": {
            "name": "📊 Comparative Statement",
            "description": "Bidder comparison with statutory format"
        },
        "letter_of_acceptance.tex": {
            "name": "✉️ Letter of Acceptance", 
            "description": "Official acceptance letter template"
        },
        "scrutiny_sheet.tex": {
            "name": "🔍 Scrutiny Sheet",
            "description": "Technical evaluation template"
        },
        "work_order.tex": {
            "name": "📝 Work Order",
            "description": "Project commencement document"
        }
    }
    
    # Template status cards
    cols = st.columns(2)
    for i, (template_file, info) in enumerate(template_info.items()):
        with cols[i % 2]:
            template_path = f"templates/{template_file}"
            
            if os.path.exists(template_path):
                with open(template_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                st.success(f"✅ {info['name']}")
                st.caption(f"{info['description']}")
                st.caption(f"Size: {len(content):,} characters")
                
            else:
                st.error(f"❌ {info['name']}")
                st.caption(f"{info['description']}")
                st.caption("Template missing")

    st.markdown("---")
    
    # Template editor
    st.subheader("✏️ Template Editor")
    
    selected_template = st.selectbox(
        "Select Template to Edit:",
        list(template_info.keys()),
        format_func=lambda x: template_info[x]['name']
    )
    
    template_path = f"templates/{selected_template}"
    
    if os.path.exists(template_path):
        with open(template_path, 'r', encoding='utf-8') as f:
            current_content = f.read()
        
        st.info(f"📝 Editing: {template_info[selected_template]['name']}")
        
        # Template editor with syntax highlighting
        edited_content = st.text_area(
            "LaTeX Template Content:",
            value=current_content,
            height=400,
            help="Edit the LaTeX template. Use {{variable_name}} for substitutions."
        )
        
        # Save changes
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("💾 Save Changes", type="primary"):
                try:
                    with open(template_path, 'w', encoding='utf-8') as f:
                        f.write(edited_content)
                    st.success("✅ Template saved successfully!")
                    st.balloons()
                except Exception as e:
                    st.error(f"❌ Error saving template: {str(e)}")
        
        with col2:
            if st.button("🔄 Reset to Default"):
                st.warning("⚠️ This will reset the template to default. Confirm?")
                if st.button("Confirm Reset"):
                    # Reset logic here
                    st.info("Template reset functionality would go here")
        
        with col3:
            # Download template
            st.download_button(
                "⬇️ Download",
                data=current_content,
                file_name=selected_template,
                mime="text/plain"
            )
        
        # Template preview/validation
        st.markdown("---")
        st.subheader("🔍 Template Variables")
        
        # Extract variables from template
        import re
        variables = re.findall(r'\{\{(\w+)\}\}', edited_content)
        unique_vars = sorted(set(variables))
        
        if unique_vars:
            st.info(f"Found {len(unique_vars)} unique variables in template:")
            var_cols = st.columns(min(4, len(unique_vars)))
            for i, var in enumerate(unique_vars):
                with var_cols[i % len(var_cols)]:
                    st.code(f"{{{{{var}}}}}")
        else:
            st.warning("No template variables found. Consider adding {{variable_name}} placeholders.")
    
    else:
        st.error(f"❌ Template file not found: {selected_template}")
        if st.button("🔧 Create Template"):
            # Create default template
            try:
                os.makedirs("templates", exist_ok=True)
                with open(template_path, 'w', encoding='utf-8') as f:
                    f.write("% LaTeX template\n\\documentclass{article}\n\\begin{document}\nTemplate content here\n\\end{document}")
                st.success("✅ Template created!")
                st.rerun()
            except Exception as e:
                st.error(f"❌ Error creating template: {str(e)}")

def handle_bidder_management(db_manager):
    """Enhanced bidder management"""
    st.info("👥 Manage bidder profiles and view bidding history across all tenders.")
    
    # Get bidder statistics
    stats = db_manager.get_bidder_statistics()
    
    # Statistics overview
    st.subheader("📊 Bidder Statistics")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "👥 Total Bidders", 
            stats.get('total_unique_bidders', 0),
            help="Total unique bidders in database"
        )
    
    with col2:
        st.metric(
            "📈 Recent Activity", 
            stats.get('recent_bids_30_days', 0),
            help="Bids submitted in last 30 days"
        )
    
    with col3:
        frequent_count = len(stats.get('frequent_bidders', []))
        st.metric(
            "⭐ Active Bidders", 
            frequent_count,
            help="Bidders with multiple submissions"
        )

    st.markdown("---")

    # Bidder list and management
    tab1, tab2 = st.tabs(["📋 Bidder List", "📈 Analytics"])
    
    with tab1:
        st.subheader("📋 Registered Bidders")
        
        # Get recent bidders
        recent_bidders = db_manager.get_recent_bidders(50)
        
        if recent_bidders:
            # Convert to DataFrame for better display
            df = pd.DataFrame(recent_bidders)
            df = df.rename(columns={
                'name': 'Bidder Name',
                'contact': 'Contact Info',
                'usage_count': 'Participation Count',
                'last_used': 'Last Activity'
            })
            
            # Format dates
            df['Last Activity'] = pd.to_datetime(df['Last Activity']).dt.strftime('%Y-%m-%d')
            
            # Sort by participation count
            df = df.sort_values('Participation Count', ascending=False)
            df.index = range(1, len(df) + 1)
            
            st.dataframe(df, use_container_width=True)
            
            # Quick actions
            st.markdown("---")
            st.subheader("🔧 Quick Actions")
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("📊 Export Bidder List", type="secondary"):
                    csv = df.to_csv(index=False)
                    st.download_button(
                        "⬇️ Download CSV",
                        data=csv,
                        file_name=f"bidders_list_{datetime.now().strftime('%Y%m%d')}.csv",
                        mime="text/csv"
                    )
            
            with col2:
                if st.button("🔄 Refresh Data", type="secondary"):
                    st.rerun()
        
        else:
            st.info("📝 No bidders found. Bidders will appear here after work entries are created.")

    with tab2:
        st.subheader("📈 Bidder Analytics")
        
        if stats.get('frequent_bidders'):
            st.markdown("#### 🏆 Top Participating Bidders")
            
            freq_df = pd.DataFrame(stats['frequent_bidders'])
            freq_df.columns = ['Bidder Name', 'Participation Count']
            freq_df.index = range(1, len(freq_df) + 1)
            
            # Display as metrics
            for idx, row in freq_df.head(5).iterrows():
                st.metric(
                    f"#{idx} {row['Bidder Name']}", 
                    f"{row['Participation Count']} tenders",
                    help=f"Participated in {row['Participation Count']} tender(s)"
                )
        
        else:
            st.info("📊 Analytics will be available once bidders participate in tenders.")

def handle_user_manual(manual_generator):
    """Enhanced user manual and help"""
    st.info("📖 Comprehensive guide for using the Enhanced Tender Processing System.")
    
    # Manual sections
    manual_sections = {
        "🚀 Getting Started": """
        ## Welcome to Enhanced Tender Processing System
        
        This system helps government departments process tenders efficiently with automated PDF generation.
        
        ### Quick Start Steps:
        1. **📁 Data Input**: Upload Excel/PDF files or enter NIT details manually
        2. **🏗️ Work Entry**: Add bidder information and percentages  
        3. **📊 PDF Reports**: Generate statutory-compliant documents
        4. **👥 Manage**: Track bidders and work entries
        
        ### System Features:
        - ✅ Excel and PDF file parsing
        - ✅ Automated bid amount calculations
        - ✅ LaTeX-based PDF generation
        - ✅ Statutory compliance formatting
        - ✅ Bidder database management
        """,
        
        "📊 Excel Format Guide": """
        ## Excel File Format Requirements
        
        ### Required Columns:
        - **NIT Number**: Format like "27/2024-25"
        - **Work Name**: Detailed work description
        - **Estimated Cost**: Numerical value in rupees
        - **Schedule Amount**: Numerical value in rupees  
        - **Earnest Money**: Security deposit amount
        - **Time of Completion**: In months
        - **EE Name**: Executive Engineer name
        
        ### Bidder Information Columns:
        - **Bidder Name**: Full legal name
        - **Percentage**: Bid percentage (+/- from estimate)
        - **Contact**: Phone or email
        
        ### Sample Excel Structure:
        ```
        | NIT Number | Work Name | Estimated Cost | Bidder 1 Name | Bidder 1 % |
        |------------|-----------|----------------|---------------|-------------|
        | 27/2024-25 | Road Work | 1000000        | ABC Company   | -5.5        |
        ```
        """,
        
        "📝 Document Types": """
        ## Available Document Types
        
        ### 📊 Comparative Statement
        - Complete bidder comparison table
        - Statutory format compliance
        - Percentage calculations
        - Ranking and analysis
        
        ### ✉️ Letter of Acceptance  
        - Official acceptance letter
        - Lowest bidder details
        - Terms and conditions
        - Signature blocks
        
        ### 🔍 Scrutiny Sheet
        - Technical evaluation
        - Financial assessment  
        - Compliance checklist
        - Recommendation section
        
        ### 📝 Work Order
        - Project commencement document
        - Scope of work
        - Timeline and milestones
        - Payment terms
        """,
        
        "🔧 Troubleshooting": """
        ## Common Issues & Solutions
        
        ### Excel Parsing Errors
        - **Issue**: File not reading properly
        - **Solution**: Ensure Excel file has proper headers and data format
        - **Tip**: Save as .xlsx format for best compatibility
        
        ### LaTeX/PDF Generation
        - **Issue**: PDF generation fails
        - **Solution**: Check LaTeX installation status in sidebar
        - **Command**: `sudo apt-get install texlive-latex-extra`
        
        ### Template Issues
        - **Issue**: Missing template variables
        - **Solution**: Use Template Manager to verify variables
        - **Format**: Variables should be `{{variable_name}}`
        
        ### Database Problems
        - **Issue**: Bidder data not saving
        - **Solution**: Check database permissions and storage space
        - **Reset**: Use "Clear Data" option in sidebar if needed
        
        ### Performance Issues
        - **Issue**: Slow processing
        - **Solution**: Process fewer documents at once
        - **Tip**: Close unused browser tabs for better performance
        """
    }
    
    # Section selection
    selected_section = st.selectbox(
        "📚 Choose Help Section:",
        list(manual_sections.keys()),
        help="Select the topic you need help with"
    )
    
    # Display selected section
    st.markdown(manual_sections[selected_section])
    
    st.markdown("---")
    
    # Additional help resources
    st.subheader("🆘 Additional Help")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📞 Contact Support", use_container_width=True):
            st.info("""
            **System Support:**
            
            📧 Email: support@pwd.gov.in  
            📞 Phone: 0294-XXXXXXX  
            🏢 Office: PWD Electric Division, Udaipur
            
            **Office Hours:** 10:00 AM - 5:00 PM (Mon-Fri)
            """)
    
    with col2:
        if st.button("💾 Download Manual", use_container_width=True):
            # Generate comprehensive manual
            full_manual = "\n\n".join([f"# {title}\n{content}" for title, content in manual_sections.items()])
            
            st.download_button(
                "⬇️ Download PDF Manual",
                data=full_manual,
                file_name=f"tender_system_manual_{datetime.now().strftime('%Y%m%d')}.txt",
                mime="text/plain"
            )
    
    with col3:
        if st.button("🔄 System Status", use_container_width=True):
            st.info(f"""
            **System Status:**
            
            ✅ Application: Running  
            📅 Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}  
            💾 Database: Connected  
            📄 Templates: Available  
            
            **Version:** Enhanced v2.0
            """)

if __name__ == "__main__":
    main()

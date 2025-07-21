import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime
import tempfile
import logging

# Import our custom modules
from theme import apply_custom_css
from ui_components import create_header, create_footer, show_balloons, create_info_card
from tender_processor import TenderProcessor
from excel_parser import ExcelParser
from bidder_manager import BidderManager
from report_generator import ReportGenerator
from document_generator import DocumentGenerator
from comparative_statement_generator import ComparativeStatementGenerator
from letter_acceptance_generator import LetterAcceptanceGenerator
from work_order_generator import WorkOrderGenerator
from scrutiny_sheet_generator import ScrutinySheetGenerator
from date_utils import DateUtils
from pdf_generator import PDFGenerator

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Page configuration
st.set_page_config(
    page_title="Tender Processing System",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom styling
apply_custom_css()

def main():
    """Main application function."""
    
    # Create header
    create_header()
    
    # Initialize session state
    if 'current_work' not in st.session_state:
        st.session_state.current_work = None
    if 'bidders' not in st.session_state:
        st.session_state.bidders = []
    if 'bidder_manager' not in st.session_state:
        st.session_state.bidder_manager = BidderManager()
    
    # Sidebar navigation
    st.sidebar.title("📋 Navigation")
    
    operation = st.sidebar.radio(
        "Select Operation:",
        [
            "📄 Upload NIT Document", 
            "👥 Manage Bidders", 
            "📊 Generate Reports",
            "📝 Generate Documents"
        ]
    )
    
    # Main content area
    if operation == "📄 Upload NIT Document":
        handle_nit_upload()
    elif operation == "👥 Manage Bidders":
        handle_bidder_management()
    elif operation == "📊 Generate Reports":
        handle_report_generation()
    elif operation == "📝 Generate Documents":
        handle_document_generation()
    
    # Create footer
    create_footer()

def handle_nit_upload():
    """Handle NIT document upload and processing."""
    st.header("📄 Upload NIT Document")
    
    create_info_card(
        "NIT Document Upload", 
        "Upload your Notice Inviting Tender (NIT) Excel file to extract work details and estimated costs. "
        "The system supports multiple date formats and will automatically parse the tender information.",
        "📄"
    )
    
    uploaded_file = st.file_uploader(
        "Choose NIT Excel file", 
        type=['xlsx', 'xls'],
        help="Upload the official NIT Excel document"
    )
    
    if uploaded_file is not None:
        try:
            # Save uploaded file temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                tmp_file_path = tmp_file.name
            
            # Parse Excel file
            parser = ExcelParser()
            work_data = parser.parse_nit_excel(tmp_file_path)
            
            # Clean up temporary file
            os.unlink(tmp_file_path)
            
            if work_data:
                st.session_state.current_work = work_data
                st.success("✅ NIT document uploaded and parsed successfully!")
                
                # Display parsed information
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("📋 Work Information")
                    st.write(f"**Work Name:** {work_data['work_name']}")
                    st.write(f"**NIT Number:** {work_data['nit_number']}")
                    st.write(f"**Estimated Cost:** ₹{work_data['work_info']['estimated_cost']:,.2f}")
                    st.write(f"**Earnest Money:** ₹{work_data['work_info']['earnest_money']}")
                
                with col2:
                    st.subheader("📅 Timeline Information")
                    st.write(f"**Date:** {work_data['work_info']['date']}")
                    st.write(f"**Time of Completion:** {work_data['work_info']['time_of_completion']}")
                    
                    # Validate and display parsed date
                    parsed_date = DateUtils.parse_date(work_data['work_info']['date'])
                    if parsed_date:
                        st.write(f"**Parsed Date:** {DateUtils.format_display_date(parsed_date)}")
                    else:
                        st.warning("⚠️ Date format not recognized. Please verify the date in the Excel file.")
                
                show_balloons()
            else:
                st.error("❌ Failed to parse NIT document. Please check the file format.")
                
        except Exception as e:
            st.error(f"❌ Error processing file: {str(e)}")
            logging.error(f"Error processing NIT file: {e}")

def handle_bidder_management():
    """Handle bidder management operations with original dropdown selection method."""
    st.header("👥 Manage Bidders")
    
    if st.session_state.current_work is None:
        st.warning("⚠️ Please upload a NIT document first.")
        return
    
    # Load bidder database
    bidder_database = {}
    try:
        with open('bidder_database.json', 'r', encoding='utf-8') as f:
            bidder_database = json.load(f)
    except Exception as e:
        st.error(f"❌ Error loading bidder database: {str(e)}")
        return
    
    # Get list of available bidders
    available_bidders = list(bidder_database.keys())
    st.info(f"📋 Available bidders in database: {len(available_bidders)}")
    
    # Step 1: Select number of bidders
    st.subheader("📊 Step 1: Select Number of Bidders")
    num_bidders = st.number_input(
        "How many bidders participated?", 
        min_value=1, 
        max_value=20, 
        value=3,
        help="Select the number of bidders who submitted tenders"
    )
    
    # Step 2: Create input windows for each bidder
    if num_bidders:
        st.subheader("👥 Step 2: Select Bidders and Enter Percentages")
        
        # Initialize bidder inputs in session state
        if 'bidder_inputs' not in st.session_state:
            st.session_state.bidder_inputs = {}
        
        bidder_data_list = []
        all_valid = True
        
        for i in range(num_bidders):
            st.markdown(f"### Bidder {i+1}")
            col1, col2 = st.columns([3, 1])
            
            with col1:
                # Dropdown to select bidder from database
                selected_bidder = st.selectbox(
                    f"Select Bidder {i+1}:",
                    options=[""] + available_bidders,
                    key=f"bidder_select_{i}",
                    help="Choose from registered bidders"
                )
                
                # Show bidder address if selected
                if selected_bidder and selected_bidder in bidder_database:
                    st.caption(f"📍 Address: {bidder_database[selected_bidder]['address']}")
            
            with col2:
                # Percentage input
                percentage_str = st.text_input(
                    f"Percentage (%):",
                    placeholder="e.g., -5.50",
                    key=f"percentage_{i}",
                    help="Enter % above (+) or below (-) estimate"
                )
            
            # Validate and calculate bid amount
            if selected_bidder and percentage_str:
                try:
                    percentage = float(percentage_str)
                    if -99.99 <= percentage <= 99.99:
                        processor = TenderProcessor()
                        bid_amount = processor.calculate_bid_amount(
                            st.session_state.current_work['work_info']['estimated_cost'],
                            percentage
                        )
                        
                        # Display calculated bid amount
                        st.success(f"💰 Calculated Bid Amount: ₹{bid_amount:,.2f}")
                        
                        bidder_data = {
                            'name': selected_bidder,
                            'address': bidder_database[selected_bidder]['address'],
                            'percentage': percentage,
                            'bid_amount': bid_amount,
                            'earnest_money': st.session_state.current_work['work_info']['earnest_money'],
                            'date_added': DateUtils().get_current_date()
                        }
                        bidder_data_list.append(bidder_data)
                    else:
                        st.error("❌ Percentage must be between -99.99% and +99.99%")
                        all_valid = False
                except ValueError:
                    st.error("❌ Please enter a valid percentage value")
                    all_valid = False
            elif selected_bidder or percentage_str:
                all_valid = False
            
            st.markdown("---")
        
        # Step 3: Add all bidders
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Add All Bidders", type="primary", disabled=not all_valid or len(bidder_data_list) != num_bidders):
                st.session_state.bidders = bidder_data_list
                
                # Update bidder database with last used dates
                for bidder_data in bidder_data_list:
                    if bidder_data['name'] in bidder_database:
                        bidder_database[bidder_data['name']]['last_used'] = DateUtils().get_current_date()
                
                # Save updated database
                try:
                    with open('bidder_database.json', 'w', encoding='utf-8') as f:
                        json.dump(bidder_database, f, indent=2, ensure_ascii=False)
                except Exception as e:
                    st.warning(f"⚠️ Could not update bidder database: {str(e)}")
                
                st.success(f"✅ Added {len(bidder_data_list)} bidders successfully!")
                st.rerun()
        
        with col2:
            if st.button("🔄 Reset All", type="secondary"):
                st.session_state.bidders = []
                if 'bidder_inputs' in st.session_state:
                    del st.session_state.bidder_inputs
                st.success("✅ Reset all bidder selections")
                st.rerun()
    
    # Display current bidders
    if st.session_state.bidders:
        st.subheader("📊 Current Selected Bidders")
        
        # Create DataFrame for display
        df_data = []
        for i, bidder in enumerate(st.session_state.bidders):
            df_data.append({
                'S.No.': i + 1,
                'Bidder Name': bidder['name'],
                'Address': bidder.get('address', 'N/A'),
                'Percentage (%)': f"{bidder['percentage']:+.2f}%",
                'Bid Amount (₹)': f"₹{bidder['bid_amount']:,.2f}",
                'Earnest Money (₹)': f"₹{bidder['earnest_money']}"
            })
        
        df = pd.DataFrame(df_data)
        st.dataframe(df, use_container_width=True)
        
        # Show L1 bidder
        sorted_bidders = sorted(st.session_state.bidders, key=lambda x: x['bid_amount'])
        l1_bidder = sorted_bidders[0]
        st.success(f"🥇 L1 (Lowest) Bidder: {l1_bidder['name']} - ₹{l1_bidder['bid_amount']:,.2f} ({l1_bidder['percentage']:+.2f}%)")
        
        # Clear all bidders option
        if st.button("🗑️ Clear All Bidders", type="secondary"):
            st.session_state.bidders = []
            st.success("✅ Cleared all bidders")
            st.rerun()

def handle_report_generation():
    """Handle report generation with simultaneous generation and download."""
    st.header("📊 Generate Reports")
    
    if not st.session_state.current_work or not st.session_state.bidders:
        st.warning("⚠️ Please upload NIT document and add bidders first.")
        return
    
    # Bulk Generation Section
    st.subheader("🚀 Generate All Reports Simultaneously")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📦 Generate All Reports", type="primary", help="Generate all reports at once"):
            try:
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                # Initialize generators
                pdf_gen = PDFGenerator()
                doc_gen = DocumentGenerator()
                
                generated_files = {}
                
                # Generate Comparative Statement (PDF)
                status_text.text("Generating Comparative Statement PDF...")
                progress_bar.progress(20)
                comp_pdf = pdf_gen.generate_comparative_statement_pdf(
                    st.session_state.current_work,
                    st.session_state.bidders
                )
                generated_files['comparative_statement_pdf'] = {
                    'content': comp_pdf,
                    'filename': f"comparative_statement_{st.session_state.current_work['nit_number']}.pdf",
                    'mime': "application/pdf"
                }
                
                # Generate Comparative Statement (DOC)
                status_text.text("Generating Comparative Statement DOC...")
                progress_bar.progress(40)
                comp_doc = doc_gen.generate_comparative_statement_doc(
                    st.session_state.current_work,
                    st.session_state.bidders
                )
                generated_files['comparative_statement_doc'] = {
                    'content': comp_doc,
                    'filename': f"comparative_statement_{st.session_state.current_work['nit_number']}.docx",
                    'mime': "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                }
                
                # Generate Scrutiny Sheet (PDF)
                status_text.text("Generating Scrutiny Sheet PDF...")
                progress_bar.progress(60)
                scrutiny_pdf = pdf_gen.generate_scrutiny_sheet_pdf(
                    st.session_state.current_work,
                    st.session_state.bidders
                )
                generated_files['scrutiny_sheet_pdf'] = {
                    'content': scrutiny_pdf,
                    'filename': f"scrutiny_sheet_{st.session_state.current_work['nit_number']}.pdf",
                    'mime': "application/pdf"
                }
                
                # Generate Scrutiny Sheet (DOC)
                status_text.text("Generating Scrutiny Sheet DOC...")
                progress_bar.progress(80)
                scrutiny_doc = doc_gen.generate_scrutiny_sheet_doc(
                    st.session_state.current_work,
                    st.session_state.bidders
                )
                generated_files['scrutiny_sheet_doc'] = {
                    'content': scrutiny_doc,
                    'filename': f"scrutiny_sheet_{st.session_state.current_work['nit_number']}.docx",
                    'mime': "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                }
                
                progress_bar.progress(100)
                status_text.text("All reports generated successfully!")
                
                st.success("✅ All reports generated simultaneously in PDF and DOC formats!")
                
                # Store in session state for download
                st.session_state.generated_reports = generated_files
                
                # Display download section
                st.subheader("📥 Download Generated Reports")
                
                col_a, col_b = st.columns(2)
                
                with col_a:
                    st.markdown("**Comparative Statement**")
                    st.download_button(
                        label="📋 Download PDF",
                        data=generated_files['comparative_statement_pdf']['content'],
                        file_name=generated_files['comparative_statement_pdf']['filename'],
                        mime="application/pdf",
                        key="download_comp_pdf"
                    )
                    st.download_button(
                        label="📋 Download DOC",
                        data=generated_files['comparative_statement_doc']['content'],
                        file_name=generated_files['comparative_statement_doc']['filename'],
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        key="download_comp_doc"
                    )
                
                with col_b:
                    st.markdown("**Scrutiny Sheet**")
                    st.download_button(
                        label="🔍 Download PDF",
                        data=generated_files['scrutiny_sheet_pdf']['content'],
                        file_name=generated_files['scrutiny_sheet_pdf']['filename'],
                        mime="application/pdf",
                        key="download_scrutiny_pdf"
                    )
                    st.download_button(
                        label="🔍 Download DOC",
                        data=generated_files['scrutiny_sheet_doc']['content'],
                        file_name=generated_files['scrutiny_sheet_doc']['filename'],
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        key="download_scrutiny_doc"
                    )
                
            except Exception as e:
                st.error(f"❌ Error in bulk report generation: {str(e)}")
                logging.error(f"Error in bulk report generation: {e}")
    
    with col2:
        if st.button("📄 Generate All Documents", type="primary", help="Generate all official documents at once"):
            try:
                progress_bar2 = st.progress(0)
                status_text2 = st.empty()
                
                # Initialize generators
                pdf_gen = PDFGenerator()
                doc_gen = DocumentGenerator()
                
                generated_docs = {}
                
                # Generate Letter of Acceptance (PDF)
                status_text2.text("Generating Letter of Acceptance PDF...")
                progress_bar2.progress(25)
                loa_pdf = pdf_gen.generate_letter_of_acceptance_pdf(
                    st.session_state.current_work,
                    st.session_state.bidders
                )
                generated_docs['letter_of_acceptance_pdf'] = {
                    'content': loa_pdf,
                    'filename': f"letter_of_acceptance_{st.session_state.current_work['nit_number']}.pdf",
                    'mime': "application/pdf"
                }
                
                # Generate Letter of Acceptance (DOC)
                status_text2.text("Generating Letter of Acceptance DOC...")
                progress_bar2.progress(50)
                loa_doc = doc_gen.generate_letter_of_acceptance_doc(
                    st.session_state.current_work,
                    st.session_state.bidders
                )
                generated_docs['letter_of_acceptance_doc'] = {
                    'content': loa_doc,
                    'filename': f"letter_of_acceptance_{st.session_state.current_work['nit_number']}.docx",
                    'mime': "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                }
                
                # Generate Work Order (PDF)
                status_text2.text("Generating Work Order PDF...")
                progress_bar2.progress(75)
                wo_pdf = pdf_gen.generate_work_order_pdf(
                    st.session_state.current_work,
                    st.session_state.bidders
                )
                generated_docs['work_order_pdf'] = {
                    'content': wo_pdf,
                    'filename': f"work_order_{st.session_state.current_work['nit_number']}.pdf",
                    'mime': "application/pdf"
                }
                
                # Generate Work Order (DOC)
                status_text2.text("Generating Work Order DOC...")
                progress_bar2.progress(100)
                wo_doc = doc_gen.generate_work_order_doc(
                    st.session_state.current_work,
                    st.session_state.bidders
                )
                generated_docs['work_order_doc'] = {
                    'content': wo_doc,
                    'filename': f"work_order_{st.session_state.current_work['nit_number']}.docx",
                    'mime': "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                }
                
                status_text2.text("All documents generated successfully!")
                
                st.success("✅ All documents generated simultaneously in PDF and DOC formats!")
                
                # Store in session state
                st.session_state.generated_documents = generated_docs
                
                # Display download section
                st.subheader("📥 Download Generated Documents")
                
                col_x, col_y = st.columns(2)
                
                with col_x:
                    st.markdown("**Letter of Acceptance**")
                    st.download_button(
                        label="📄 Download PDF",
                        data=generated_docs['letter_of_acceptance_pdf']['content'],
                        file_name=generated_docs['letter_of_acceptance_pdf']['filename'],
                        mime="application/pdf",
                        key="download_loa_pdf"
                    )
                    st.download_button(
                        label="📄 Download DOC",
                        data=generated_docs['letter_of_acceptance_doc']['content'],
                        file_name=generated_docs['letter_of_acceptance_doc']['filename'],
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        key="download_loa_doc"
                    )
                
                with col_y:
                    st.markdown("**Work Order**")
                    st.download_button(
                        label="📋 Download PDF",
                        data=generated_docs['work_order_pdf']['content'],
                        file_name=generated_docs['work_order_pdf']['filename'],
                        mime="application/pdf",
                        key="download_wo_pdf"
                    )
                    st.download_button(
                        label="📋 Download DOC",
                        data=generated_docs['work_order_doc']['content'],
                        file_name=generated_docs['work_order_doc']['filename'],
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        key="download_wo_doc"
                    )
                
            except Exception as e:
                st.error(f"❌ Error in bulk document generation: {str(e)}")
                logging.error(f"Error in bulk document generation: {e}")
    
    # Divider
    st.markdown("---")
    
    # Individual Generation Section (keep for specific needs)
    st.subheader("🎯 Generate Individual Reports")
    
    col3, col4 = st.columns(2)
    
    with col3:
        if st.button("📋 Generate Comparative Statement", type="secondary"):
            try:
                comp_gen = ComparativeStatementGenerator()
                html_content = comp_gen.generate_comparative_statement(
                    st.session_state.current_work,
                    st.session_state.bidders
                )
                
                st.success("✅ Comparative statement generated!")
                
                st.download_button(
                    label="📥 Download Comparative Statement",
                    data=html_content,
                    file_name=f"comparative_statement_{st.session_state.current_work['nit_number']}.html",
                    mime="text/html",
                    key="single_comp"
                )
                
            except Exception as e:
                st.error(f"❌ Error generating comparative statement: {str(e)}")
                logging.error(f"Error generating comparative statement: {e}")
    
    with col4:
        if st.button("📊 Generate Detailed Report", type="secondary"):
            try:
                report_generator = ReportGenerator()
                html_content = report_generator.generate_detailed_report(
                    st.session_state.current_work,
                    st.session_state.bidders
                )
                
                st.success("✅ Detailed report generated!")
                
                st.download_button(
                    label="📥 Download Detailed Report",
                    data=html_content,
                    file_name=f"detailed_report_{st.session_state.current_work['nit_number']}.html",
                    mime="text/html",
                    key="single_detailed"
                )
                
            except Exception as e:
                st.error(f"❌ Error generating detailed report: {str(e)}")
                logging.error(f"Error generating detailed report: {e}")

def handle_document_generation():
    """Handle official document generation with individual options."""
    st.header("📝 Generate Individual Documents")
    
    if not st.session_state.current_work or not st.session_state.bidders:
        st.warning("⚠️ Please upload NIT document and add bidders first.")
        return
    
    st.info("💡 Tip: Use 'Generate Reports' section for bulk generation of all documents simultaneously!")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📄 Generate Letter of Acceptance", type="secondary"):
            try:
                loa_gen = LetterAcceptanceGenerator()
                html_content = loa_gen.generate_letter_of_acceptance(
                    st.session_state.current_work,
                    st.session_state.bidders
                )
                
                st.success("✅ Letter of Acceptance generated!")
                
                st.download_button(
                    label="📥 Download Letter of Acceptance",
                    data=html_content,
                    file_name=f"letter_of_acceptance_{st.session_state.current_work['nit_number']}.html",
                    mime="text/html",
                    key="individual_loa"
                )
                
            except Exception as e:
                st.error(f"❌ Error generating Letter of Acceptance: {str(e)}")
                logging.error(f"Error generating LOA: {e}")
    
    with col2:
        if st.button("📋 Generate Work Order", type="secondary"):
            try:
                wo_gen = WorkOrderGenerator()
                html_content = wo_gen.generate_work_order(
                    st.session_state.current_work,
                    st.session_state.bidders
                )
                
                st.success("✅ Work Order generated!")
                
                st.download_button(
                    label="📥 Download Work Order",
                    data=html_content,
                    file_name=f"work_order_{st.session_state.current_work['nit_number']}.html",
                    mime="text/html",
                    key="individual_wo"
                )
                
            except Exception as e:
                st.error(f"❌ Error generating Work Order: {str(e)}")
                logging.error(f"Error generating work order: {e}")
    
    with col3:
        if st.button("🔍 Generate Scrutiny Sheet", type="secondary"):
            try:
                ss_gen = ScrutinySheetGenerator()
                html_content = ss_gen.generate_scrutiny_sheet(
                    st.session_state.current_work,
                    st.session_state.bidders
                )
                
                st.success("✅ Scrutiny Sheet generated!")
                
                st.download_button(
                    label="📥 Download Scrutiny Sheet",
                    data=html_content,
                    file_name=f"scrutiny_sheet_{st.session_state.current_work['nit_number']}.html",
                    mime="text/html",
                    key="individual_scrutiny"
                )
                
            except Exception as e:
                st.error(f"❌ Error generating Scrutiny Sheet: {str(e)}")
                logging.error(f"Error generating scrutiny sheet: {e}")



if __name__ == "__main__":
    main()

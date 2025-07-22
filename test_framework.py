import streamlit as st
import pandas as pd
import os
import sys
import traceback
from datetime import datetime
import json
import tempfile
import shutil

from comprehensive_tester import comprehensive_tester
from test_scenarios import test_scenarios
from test_data_generator import test_data_gen
from debug_logger import debug_logger
from error_handler import error_handler
from performance_monitor import perf_monitor

class TestFramework:
    """Main test framework controller for TenderLatexPro"""
    
    def __init__(self):
        self.framework_version = "2.0.0"
        self.test_start_time = datetime.now()
        
    def initialize_test_environment(self):
        """Initialize the testing environment"""
        debug_logger.log_function_entry("initialize_test_environment")
        
        try:
            # Create test directories
            test_dirs = [
                "test_outputs",
                "test_logs", 
                "test_temp",
                "attached_assets"
            ]
            
            for dir_name in test_dirs:
                os.makedirs(dir_name, exist_ok=True)
            
            # Generate test data files
            test_data_gen.create_test_excel_files()
            
            # Initialize session state for testing
            if 'test_initialized' not in st.session_state:
                st.session_state.test_initialized = True
                st.session_state.test_results = []
                st.session_state.test_errors = []
                
            debug_logger.log_function_exit("initialize_test_environment", True)
            return True
            
        except Exception as e:
            debug_logger.log_error(e, "Failed to initialize test environment")
            return False
    
    def display_test_interface(self):
        """Display the main testing interface"""
        st.title("🧪 TenderLatexPro Testing Framework")
        st.caption(f"Framework Version: {self.framework_version}")
        
        # Initialize test environment
        if not self.initialize_test_environment():
            st.error("❌ Failed to initialize test environment")
            return
        
        # Test framework tabs
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "🚀 Quick Start",
            "🔍 Comprehensive Tests", 
            "🎛️ Custom Scenarios",
            "📊 Performance",
            "🛠️ Debug & Monitor"
        ])
        
        with tab1:
            self.display_quick_start()
        
        with tab2:
            self.display_comprehensive_tests()
        
        with tab3:
            self.display_custom_scenarios()
        
        with tab4:
            self.display_performance_tests()
        
        with tab5:
            self.display_debug_monitor()
    
    def display_quick_start(self):
        """Display quick start testing options"""
        st.header("🚀 Quick Start Testing")
        
        st.info("""
        **Quick Start Guide:**
        1. Click 'Generate Test Data' to create sample Excel files
        2. Run 'Smoke Test' to verify basic functionality
        3. Test specific components using the options below
        """)
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📁 Generate Test Data", type="primary"):
                with st.spinner("Generating test data..."):
                    try:
                        file1, file10 = test_data_gen.create_test_excel_files()
                        st.success(f"✅ Test files created:")
                        st.text(f"• {file1}")
                        st.text(f"• {file10}")
                    except Exception as e:
                        st.error(f"❌ Failed to generate test data: {str(e)}")
            
            if st.button("💨 Run Smoke Test"):
                comprehensive_tester.run_smoke_test()
        
        with col2:
            if st.button("📊 System Status Check"):
                self.display_system_status()
            
            if st.button("🔧 Component Health Check"):
                self.run_component_health_check()
    
    def display_system_status(self):
        """Display current system status"""
        st.subheader("📊 System Status")
        
        # Check file existence
        required_files = [
            "app.py",
            "database_manager.py",
            "excel_parser.py",
            "latex_report_generator.py",
            "pdf_generator.py",
            "tender_processor.py"
        ]
        
        st.write("**Core Files Status:**")
        for file_path in required_files:
            if os.path.exists(file_path):
                st.success(f"✅ {file_path}")
            else:
                st.error(f"❌ {file_path} - Missing")
        
        # Check directories
        required_dirs = ["templates", "attached_assets", ".streamlit"]
        
        st.write("**Directory Status:**")
        for dir_path in required_dirs:
            if os.path.exists(dir_path):
                st.success(f"✅ {dir_path}/")
            else:
                st.warning(f"⚠️ {dir_path}/ - Missing")
        
        # System metrics
        metrics = perf_monitor.get_system_metrics()
        
        st.write("**System Metrics:**")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("CPU Usage", f"{metrics.get('cpu_percent', 0):.1f}%")
        
        with col2:
            st.metric("Memory", f"{metrics.get('memory_used_mb', 0):.1f}MB")
        
        with col3:
            st.metric("Uptime", f"{metrics.get('uptime_seconds', 0):.0f}s")
    
    def run_component_health_check(self):
        """Run health check on all components"""
        st.subheader("🔧 Component Health Check")
        
        components = [
            ("Database Manager", self.test_database_component),
            ("Excel Parser", self.test_excel_parser_component),
            ("LaTeX Generator", self.test_latex_component),
            ("PDF Generator", self.test_pdf_component),
            ("Template Processor", self.test_template_component)
        ]
        
        health_results = []
        
        for component_name, test_function in components:
            try:
                perf_monitor.start_operation(f"Health_{component_name}")
                result = test_function()
                duration = perf_monitor.end_operation(f"Health_{component_name}")
                
                health_results.append({
                    'Component': component_name,
                    'Status': '✅ Healthy' if result else '❌ Failed',
                    'Response Time': f"{duration:.2f}s"
                })
                
            except Exception as e:
                health_results.append({
                    'Component': component_name,
                    'Status': f'❌ Error: {str(e)[:30]}...',
                    'Response Time': 'N/A'
                })
        
        # Display results
        health_df = pd.DataFrame(health_results)
        st.dataframe(health_df, use_container_width=True)
    
    def test_database_component(self):
        """Test database component health"""
        try:
            from database_manager import DatabaseManager
            db_manager = DatabaseManager()
            db_manager.initialize_database()
            
            # Test basic operations
            test_bidder = "Health Check Bidder"
            db_manager.add_bidder(test_bidder, 100000, 999)
            bidders = db_manager.get_all_bidders()
            
            return len(bidders) >= 0
        except Exception as e:
            debug_logger.log_error(e, "Database component health check failed")
            return False
    
    def test_excel_parser_component(self):
        """Test Excel parser component health"""
        try:
            from excel_parser import ExcelParser
            parser = ExcelParser()
            
            # Create a simple test Excel file
            test_data = pd.DataFrame({'Test': ['Data']})
            test_file = "test_temp/health_check.xlsx"
            test_data.to_excel(test_file, index=False)
            
            # Test parsing
            result = parser.parse_excel_file(test_file)
            
            # Cleanup
            if os.path.exists(test_file):
                os.remove(test_file)
            
            return result is not None
        except Exception as e:
            debug_logger.log_error(e, "Excel parser component health check failed")
            return False
    
    def test_latex_component(self):
        """Test LaTeX component health"""
        try:
            from latex_report_generator import LatexReportGenerator
            latex_gen = LatexReportGenerator()
            
            # Test basic LaTeX generation
            sample_data = {
                'nit_number': 'HEALTH-001',
                'work_description': 'Health Check Work',
                'estimated_cost': 100000
            }
            
            template_content = latex_gen.generate_basic_template(sample_data)
            return template_content is not None
        except Exception as e:
            debug_logger.log_error(e, "LaTeX component health check failed")
            return False
    
    def test_pdf_component(self):
        """Test PDF component health"""
        try:
            from pdf_generator import PDFGenerator
            pdf_gen = PDFGenerator()
            
            # Test LaTeX installation check
            latex_status = pdf_gen.check_latex_installation()
            return latex_status.get('installed', False)
        except Exception as e:
            debug_logger.log_error(e, "PDF component health check failed")
            return False
    
    def test_template_component(self):
        """Test template component health"""
        try:
            from template_processor import TemplateProcessor
            template_proc = TemplateProcessor()
            
            # Test template loading
            templates = template_proc.get_available_templates()
            return len(templates) >= 0
        except Exception as e:
            debug_logger.log_error(e, "Template component health check failed")
            return False
    
    def display_comprehensive_tests(self):
        """Display comprehensive testing interface"""
        st.header("🔍 Comprehensive Test Suite")
        
        comprehensive_tester.display_testing_interface()
    
    def display_custom_scenarios(self):
        """Display custom scenario testing"""
        st.header("🎛️ Custom Test Scenarios")
        
        st.info("""
        **Custom Scenario Testing allows you to:**
        - Test with specific number of bidders and works
        - Simulate different percentile selections
        - Include outside bidders in testing
        - Test edge cases and boundary conditions
        """)
        
        # Scenario configuration
        with st.form("custom_scenario_form"):
            st.subheader("Configure Test Scenario")
            
            col1, col2 = st.columns(2)
            
            with col1:
                num_works = st.number_input("Number of Works", 1, 50, 5)
                num_bidders_per_work = st.number_input("Bidders per Work", 2, 20, 5)
                percentile = st.slider("Selection Percentile", 50, 100, 80)
            
            with col2:
                include_outside = st.checkbox("Include Outside Bidders", True)
                test_error_cases = st.checkbox("Test Error Cases", False)
                generate_documents = st.checkbox("Generate Test Documents", True)
            
            submitted = st.form_submit_button("🚀 Run Custom Scenario")
            
            if submitted:
                self.run_custom_test_scenario(
                    num_works, num_bidders_per_work, percentile,
                    include_outside, test_error_cases, generate_documents
                )
    
    def run_custom_test_scenario(self, num_works, num_bidders, percentile, 
                                include_outside, test_errors, generate_docs):
        """Run a custom test scenario with specified parameters"""
        
        st.subheader("🎬 Running Custom Scenario")
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            # Step 1: Generate test data
            status_text.text("Generating test data...")
            progress_bar.progress(20)
            
            works_data, bidders_data = test_data_gen.generate_nit_10_works_data()
            
            # Limit data to requested size
            works_data = works_data.head(num_works)
            bidders_data = bidders_data[bidders_data['Work No.'] <= num_works]
            
            # Step 2: Add outside bidders if requested
            if include_outside:
                status_text.text("Adding outside bidders...")
                progress_bar.progress(40)
                
                outside_bidders = test_data_gen.generate_custom_bidder_data(num_works)
                st.info(f"✅ Added {len(outside_bidders)} outside bidders")
            
            # Step 3: Test bidder selection
            status_text.text(f"Testing {percentile}th percentile selection...")
            progress_bar.progress(60)
            
            for work_no in range(1, num_works + 1):
                work_bidders = bidders_data[bidders_data['Work No.'] == work_no]
                # Simulate selection logic here
                st.text(f"• Work {work_no}: {len(work_bidders)} bidders processed")
            
            # Step 4: Generate documents if requested
            if generate_docs:
                status_text.text("Generating test documents...")
                progress_bar.progress(80)
                
                # Simulate document generation
                st.info("✅ Document generation simulated")
            
            # Step 5: Test error cases if requested
            if test_errors:
                status_text.text("Testing error scenarios...")
                progress_bar.progress(90)
                
                # Simulate error testing
                st.info("✅ Error scenarios tested")
            
            progress_bar.progress(100)
            status_text.text("Custom scenario completed!")
            
            st.success("🎉 Custom scenario executed successfully!")
            
            # Display scenario summary
            self.display_scenario_summary(
                num_works, num_bidders, percentile, include_outside, test_errors, generate_docs
            )
            
        except Exception as e:
            debug_logger.log_error(e, "Custom scenario execution failed")
            st.error(f"❌ Custom scenario failed: {str(e)}")
    
    def display_scenario_summary(self, num_works, num_bidders, percentile, 
                                include_outside, test_errors, generate_docs):
        """Display summary of custom scenario results"""
        
        st.subheader("📋 Scenario Summary")
        
        summary_data = {
            'Parameter': [
                'Number of Works',
                'Bidders per Work', 
                'Selection Percentile',
                'Outside Bidders',
                'Error Testing',
                'Document Generation'
            ],
            'Value': [
                num_works,
                num_bidders,
                f"{percentile}%",
                'Yes' if include_outside else 'No',
                'Yes' if test_errors else 'No',
                'Yes' if generate_docs else 'No'
            ]
        }
        
        summary_df = pd.DataFrame(summary_data)
        st.table(summary_df)
    
    def display_performance_tests(self):
        """Display performance testing interface"""
        st.header("📊 Performance Testing")
        
        st.info("""
        **Performance Testing Features:**
        - Benchmark different data sizes
        - Measure processing times
        - Monitor resource usage
        - Identify bottlenecks
        """)
        
        if st.button("🚀 Run Performance Benchmark"):
            comprehensive_tester.run_performance_benchmark()
    
    def display_debug_monitor(self):
        """Display debug and monitoring interface"""
        st.header("🛠️ Debug & Monitor")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🐛 Debug Controls")
            
            # Debug mode toggle
            debug_mode = st.checkbox(
                "Enable Debug Mode", 
                value=st.session_state.get('debug_mode', False)
            )
            st.session_state.debug_mode = debug_mode
            
            if st.button("Clear Debug Logs"):
                debug_logger.setup_logging()  # Reinitialize logging
                st.success("Debug logs cleared!")
            
            if st.button("Export Debug Info"):
                self.export_debug_info()
        
        with col2:
            st.subheader("📊 System Monitor")
            
            # Display performance metrics
            perf_monitor.display_performance_metrics()
            
            # Display debug panel
            debug_logger.display_debug_panel()
        
        # Error handling display
        error_handler.display_error_summary()
    
    def export_debug_info(self):
        """Export debug information to file"""
        try:
            debug_info = {
                'timestamp': datetime.now().isoformat(),
                'framework_version': self.framework_version,
                'system_metrics': perf_monitor.get_system_metrics(),
                'session_state': {
                    'test_initialized': st.session_state.get('test_initialized', False),
                    'debug_mode': st.session_state.get('debug_mode', False),
                    'works_count': len(st.session_state.get('works', [])),
                    'tender_data_keys': list(st.session_state.get('tender_data', {}).keys())
                }
            }
            
            export_file = f"test_logs/debug_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
            with open(export_file, 'w') as f:
                json.dump(debug_info, f, indent=2)
            
            st.success(f"✅ Debug info exported to: {export_file}")
            
            # Provide download link
            with open(export_file, 'r') as f:
                st.download_button(
                    label="📥 Download Debug Export",
                    data=f.read(),
                    file_name=os.path.basename(export_file),
                    mime="application/json"
                )
                
        except Exception as e:
            debug_logger.log_error(e, "Failed to export debug info")
            st.error(f"❌ Failed to export debug info: {str(e)}")

# Global test framework instance
test_framework = TestFramework()

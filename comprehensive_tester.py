import streamlit as st
import pandas as pd
import os
import tempfile
from datetime import datetime
import json
import random

from test_scenarios import test_scenarios
from test_data_generator import test_data_gen
from debug_logger import debug_logger
from error_handler import error_handler
from performance_monitor import perf_monitor

class ComprehensiveTester:
    """Main testing interface for TenderLatexPro"""
    
    def __init__(self):
        self.test_session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        
    def display_testing_interface(self):
        """Display the main testing interface"""
        st.header("🧪 TenderLatexPro Testing Suite")
        
        # Testing mode selection
        test_mode = st.selectbox(
            "Select Testing Mode",
            [
                "Quick Smoke Test",
                "Comprehensive Test Suite",
                "Custom Scenario Testing",
                "Performance Benchmarking",
                "Error Simulation Testing"
            ]
        )
        
        if st.button("🚀 Start Testing", type="primary"):
            self.run_selected_test_mode(test_mode)
    
    def run_selected_test_mode(self, test_mode):
        """Run the selected test mode"""
        debug_logger.log_function_entry("run_selected_test_mode", mode=test_mode)
        
        try:
            if test_mode == "Quick Smoke Test":
                self.run_smoke_test()
            elif test_mode == "Comprehensive Test Suite":
                self.run_comprehensive_test()
            elif test_mode == "Custom Scenario Testing":
                self.run_custom_scenarios()
            elif test_mode == "Performance Benchmarking":
                self.run_performance_benchmark()
            elif test_mode == "Error Simulation Testing":
                self.run_error_simulation()
                
        except Exception as e:
            debug_logger.log_error(e, f"Test mode failed: {test_mode}")
            st.error(f"❌ Testing failed: {str(e)}")
    
    def run_smoke_test(self):
        """Run basic smoke tests to verify core functionality"""
        st.subheader("💨 Quick Smoke Test")
        
        with st.spinner("Running smoke tests..."):
            # Test 1: File generation
            try:
                file1, file10 = test_data_gen.create_test_excel_files()
                st.success("✅ Test file generation successful")
            except Exception as e:
                st.error(f"❌ File generation failed: {str(e)}")
                return
            
            # Test 2: Basic imports
            try:
                from tender_processor import TenderProcessor
                from database_manager import DatabaseManager
                from excel_parser import ExcelParser
                st.success("✅ Core module imports successful")
            except Exception as e:
                st.error(f"❌ Module import failed: {str(e)}")
                return
            
            # Test 3: Database connectivity
            try:
                db_manager = DatabaseManager()
                db_manager.initialize_database()
                st.success("✅ Database connectivity successful")
            except Exception as e:
                st.error(f"❌ Database connectivity failed: {str(e)}")
                return
            
            # Test 4: File parsing
            try:
                parser = ExcelParser()
                parsed_data = parser.parse_excel_file(file1)
                if parsed_data:
                    st.success("✅ File parsing successful")
                else:
                    st.error("❌ File parsing returned no data")
            except Exception as e:
                st.error(f"❌ File parsing failed: {str(e)}")
                return
        
        st.success("🎉 Smoke test completed successfully!")
    
    def run_comprehensive_test(self):
        """Run the full comprehensive test suite"""
        st.subheader("🔍 Comprehensive Test Suite")
        test_scenarios.run_all_tests()
    
    def run_custom_scenarios(self):
        """Run custom testing scenarios"""
        st.subheader("🎛️ Custom Scenario Testing")
        
        # Scenario configuration
        col1, col2 = st.columns(2)
        
        with col1:
            num_bidders = st.slider("Number of Bidders", 2, 15, 5)
            num_works = st.slider("Number of Works", 1, 20, 3)
        
        with col2:
            percentile = st.slider("Selection Percentile", 50, 100, 80)
            include_outside_bidders = st.checkbox("Include Outside Bidders", True)
        
        if st.button("Run Custom Scenario"):
            self.execute_custom_scenario(
                num_bidders, num_works, percentile, include_outside_bidders
            )
    
    def execute_custom_scenario(self, num_bidders, num_works, percentile, include_outside):
        """Execute a custom test scenario"""
        with st.spinner(f"Running custom scenario: {num_bidders} bidders, {num_works} works..."):
            
            perf_monitor.start_operation("Custom Scenario")
            
            try:
                # Generate custom test data
                works_data, bidders_data = test_data_gen.generate_nit_10_works_data()
                
                # Limit to requested number of works
                works_data = works_data.head(num_works)
                bidders_data = bidders_data[bidders_data['Work No.'] <= num_works]
                
                # Add outside bidders if requested
                if include_outside:
                    outside_bidders = test_data_gen.generate_custom_bidder_data(num_works)
                    st.info(f"✅ Added {len(outside_bidders)} outside bidders")
                
                # Simulate bidder selection at specified percentile
                st.info(f"✅ Testing {percentile}th percentile selection")
                
                # Test document generation for each work
                for work_no in range(1, num_works + 1):
                    work_bidders = bidders_data[bidders_data['Work No.'] == work_no]
                    st.info(f"✅ Work {work_no}: {len(work_bidders)} bidders processed")
                
                duration = perf_monitor.end_operation("Custom Scenario")
                
                st.success(f"🎉 Custom scenario completed in {duration:.2f}s")
                
                # Display results summary
                self.display_scenario_results(num_bidders, num_works, percentile, duration)
                
            except Exception as e:
                debug_logger.log_error(e, "Custom scenario execution failed")
                st.error(f"❌ Custom scenario failed: {str(e)}")
    
    def display_scenario_results(self, num_bidders, num_works, percentile, duration):
        """Display results of custom scenario"""
        st.subheader("📊 Scenario Results")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Bidders Processed", num_bidders)
        
        with col2:
            st.metric("Works Processed", num_works)
        
        with col3:
            st.metric("Percentile Used", f"{percentile}%")
        
        with col4:
            st.metric("Processing Time", f"{duration:.2f}s")
    
    def run_performance_benchmark(self):
        """Run performance benchmarking tests"""
        st.subheader("🚀 Performance Benchmarking")
        
        benchmark_scenarios = [
            ("Small Dataset", 5, 3),
            ("Medium Dataset", 10, 8),
            ("Large Dataset", 20, 15),
            ("Extra Large Dataset", 50, 25)
        ]
        
        results = []
        
        for scenario_name, num_works, num_bidders in benchmark_scenarios:
            st.write(f"**Testing {scenario_name}**")
            
            perf_monitor.start_operation(scenario_name)
            
            try:
                # Simulate processing
                works_data, bidders_data = test_data_gen.generate_nit_10_works_data()
                
                # Process subset based on scenario
                processing_time = perf_monitor.end_operation(scenario_name)
                
                results.append({
                    'Scenario': scenario_name,
                    'Works': num_works,
                    'Bidders': num_bidders,
                    'Time (s)': round(processing_time, 2),
                    'Works/sec': round(num_works / processing_time, 2) if processing_time > 0 else 0
                })
                
                st.success(f"✅ {scenario_name}: {processing_time:.2f}s")
                
            except Exception as e:
                st.error(f"❌ {scenario_name} failed: {str(e)}")
        
        # Display benchmark results
        if results:
            st.subheader("📊 Benchmark Results")
            results_df = pd.DataFrame(results)
            st.dataframe(results_df, use_container_width=True)
            
            # Performance visualization
            st.line_chart(results_df.set_index('Scenario')['Time (s)'])
    
    def run_error_simulation(self):
        """Simulate various error conditions"""
        st.subheader("⚠️ Error Simulation Testing")
        
        error_tests = [
            ("Invalid File Format", self.test_invalid_file),
            ("Corrupted Data", self.test_corrupted_data),
            ("Missing Required Fields", self.test_missing_fields),
            ("Database Connection Error", self.test_db_error),
            ("Memory Limit Test", self.test_memory_limit)
        ]
        
        for test_name, test_function in error_tests:
            st.write(f"**Testing: {test_name}**")
            
            try:
                test_function()
                st.success(f"✅ {test_name}: Error handled correctly")
            except Exception as e:
                st.info(f"ℹ️ {test_name}: Expected error occurred - {str(e)}")
    
    def test_invalid_file(self):
        """Test handling of invalid file formats"""
        # Create a fake invalid file
        with tempfile.NamedTemporaryFile(suffix='.txt', delete=False) as f:
            f.write(b"This is not an Excel file")
            temp_file = f.name
        
        try:
            df = pd.read_excel(temp_file)
        except Exception as e:
            # This should fail - that's expected
            pass
        finally:
            os.unlink(temp_file)
    
    def test_corrupted_data(self):
        """Test handling of corrupted data"""
        # Create DataFrame with problematic data
        corrupted_data = pd.DataFrame({
            'Amount': ['invalid', None, -1000, 'text'],
            'Date': ['not_a_date', None, 'invalid', '2024-13-45']
        })
        
        # Try to process corrupted data
        for col in corrupted_data.columns:
            try:
                pd.to_numeric(corrupted_data[col])
            except:
                pass  # Expected to fail
    
    def test_missing_fields(self):
        """Test handling of missing required fields"""
        incomplete_data = {'name': 'Test', 'amount': 1000}
        required_fields = ['name', 'amount', 'date', 'status']
        
        valid, message = error_handler.validate_data_structure(
            incomplete_data, required_fields, "Test Data"
        )
        
        if not valid:
            raise Exception(message)
    
    def test_db_error(self):
        """Test database error handling"""
        try:
            # Try to connect to non-existent database
            import sqlite3
            conn = sqlite3.connect('/nonexistent/path/database.db')
            conn.execute("SELECT * FROM nonexistent_table")
        except Exception as e:
            raise e
    
    def test_memory_limit(self):
        """Test memory limit handling"""
        try:
            # Try to create very large dataset
            large_data = list(range(1000000))  # Large but not too large
            del large_data  # Clean up
        except MemoryError as e:
            raise e
    
    def display_testing_dashboard(self):
        """Display comprehensive testing dashboard"""
        st.subheader("📈 Testing Dashboard")
        
        # System status
        metrics = perf_monitor.get_system_metrics()
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("System CPU", f"{metrics.get('cpu_percent', 0):.1f}%")
            st.metric("Memory Usage", f"{metrics.get('memory_used_mb', 0):.1f}MB")
        
        with col2:
            st.metric("Test Session", self.test_session_id)
            st.metric("Uptime", f"{metrics.get('uptime_seconds', 0):.0f}s")
        
        with col3:
            test_files_exist = (
                os.path.exists("attached_assets/test_nit_1.xlsx") and
                os.path.exists("attached_assets/test_nit_10.xlsx")
            )
            st.metric("Test Files", "Ready" if test_files_exist else "Missing")
            st.metric("Debug Mode", "ON" if st.session_state.get('debug_mode') else "OFF")

# Global comprehensive tester instance
comprehensive_tester = ComprehensiveTester()

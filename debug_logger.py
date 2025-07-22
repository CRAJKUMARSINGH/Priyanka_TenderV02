import logging
import streamlit as st
import traceback
import sys
from datetime import datetime
import os

class DebugLogger:
    """Enhanced debug logging system for TenderLatexPro"""
    
    def __init__(self):
        self.log_file = "logs/debug.log"
        self.setup_logging()
        
    def setup_logging(self):
        """Setup comprehensive logging configuration"""
        os.makedirs("logs", exist_ok=True)
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # File handler
        file_handler = logging.FileHandler(self.log_file)
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.DEBUG)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        console_handler.setLevel(logging.INFO)
        
        # Root logger
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
    def log_function_entry(self, func_name, **kwargs):
        """Log function entry with parameters"""
        logging.info(f"ENTERING: {func_name} with params: {kwargs}")
        
    def log_function_exit(self, func_name, result=None):
        """Log function exit with result"""
        logging.info(f"EXITING: {func_name} with result: {type(result)}")
        
    def log_error(self, error, context=""):
        """Log detailed error information"""
        error_info = {
            'error_type': type(error).__name__,
            'error_message': str(error),
            'context': context,
            'traceback': traceback.format_exc(),
            'timestamp': datetime.now().isoformat()
        }
        
        logging.error(f"ERROR: {error_info}")
        
        # Also display in Streamlit if in debug mode
        if hasattr(st.session_state, 'debug_mode') and st.session_state.debug_mode:
            with st.expander(f"🐛 Debug Error: {error_info['error_type']}", expanded=False):
                st.error(f"**Error:** {error_info['error_message']}")
                st.text(f"**Context:** {error_info['context']}")
                st.code(error_info['traceback'], language='python')
                
    def log_warning(self, message, context=""):
        """Log warning with context"""
        logging.warning(f"WARNING: {message} - Context: {context}")
        
    def log_performance(self, operation, duration, details=None):
        """Log performance metrics"""
        perf_info = {
            'operation': operation,
            'duration_seconds': duration,
            'details': details or {},
            'timestamp': datetime.now().isoformat()
        }
        logging.info(f"PERFORMANCE: {perf_info}")
        
    def log_data_validation(self, data_type, validation_result, errors=None):
        """Log data validation results"""
        validation_info = {
            'data_type': data_type,
            'valid': validation_result,
            'errors': errors or [],
            'timestamp': datetime.now().isoformat()
        }
        logging.info(f"VALIDATION: {validation_info}")
        
    def display_debug_panel(self):
        """Display debug information panel in Streamlit"""
        if hasattr(st.session_state, 'debug_mode') and st.session_state.debug_mode:
            with st.sidebar:
                st.markdown("---")
                st.subheader("🐛 Debug Panel")
                
                # Show recent logs
                if os.path.exists(self.log_file):
                    with open(self.log_file, 'r') as f:
                        lines = f.readlines()
                        recent_logs = lines[-20:] if len(lines) > 20 else lines
                    
                    with st.expander("Recent Logs", expanded=False):
                        for line in recent_logs:
                            st.text(line.strip())
                
                # Clear logs button
                if st.button("Clear Debug Logs"):
                    if os.path.exists(self.log_file):
                        os.remove(self.log_file)
                    st.success("Debug logs cleared!")
                    st.rerun()

# Global debug logger instance
debug_logger = DebugLogger()

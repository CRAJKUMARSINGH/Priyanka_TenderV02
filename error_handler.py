import streamlit as st
import traceback
import functools
from debug_logger import debug_logger

class ErrorHandler:
    """Comprehensive error handling system"""
    
    @staticmethod
    def handle_with_retry(max_retries=3, delay=1):
        """Decorator for handling functions with retry logic"""
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                for attempt in range(max_retries):
                    try:
                        return func(*args, **kwargs)
                    except Exception as e:
                        debug_logger.log_error(e, f"Attempt {attempt + 1}/{max_retries} failed for {func.__name__}")
                        if attempt == max_retries - 1:
                            raise e
                        import time
                        time.sleep(delay)
                return None
            return wrapper
        return decorator
    
    @staticmethod
    def safe_execute(func, error_message="An error occurred", show_traceback=False):
        """Safely execute a function with error handling"""
        try:
            return func()
        except Exception as e:
            debug_logger.log_error(e, f"Safe execution failed: {func.__name__}")
            st.error(f"❌ {error_message}: {str(e)}")
            
            if show_traceback or (hasattr(st.session_state, 'debug_mode') and st.session_state.debug_mode):
                with st.expander("🔍 Error Details", expanded=False):
                    st.code(traceback.format_exc(), language='python')
            return None
    
    @staticmethod
    def validate_file_upload(uploaded_file, allowed_extensions=None, max_size_mb=10):
        """Validate uploaded file"""
        if uploaded_file is None:
            return False, "No file uploaded"
        
        # Check file extension
        if allowed_extensions:
            file_extension = uploaded_file.name.split('.')[-1].lower()
            if file_extension not in allowed_extensions:
                return False, f"Invalid file type. Allowed: {', '.join(allowed_extensions)}"
        
        # Check file size
        if uploaded_file.size > max_size_mb * 1024 * 1024:
            return False, f"File too large. Maximum size: {max_size_mb}MB"
        
        return True, "Valid file"
    
    @staticmethod
    def validate_data_structure(data, required_fields, data_name="Data"):
        """Validate data structure has required fields"""
        missing_fields = []
        
        if not isinstance(data, dict):
            return False, f"{data_name} must be a dictionary"
        
        for field in required_fields:
            if field not in data:
                missing_fields.append(field)
        
        if missing_fields:
            return False, f"Missing required fields in {data_name}: {', '.join(missing_fields)}"
        
        return True, f"{data_name} structure is valid"
    
    @staticmethod
    def display_error_summary():
        """Display error summary in sidebar"""
        if 'error_count' not in st.session_state:
            st.session_state.error_count = 0
        
        if 'warning_count' not in st.session_state:
            st.session_state.warning_count = 0
        
        with st.sidebar:
            if st.session_state.error_count > 0 or st.session_state.warning_count > 0:
                st.markdown("---")
                st.subheader("⚠️ Error Summary")
                
                if st.session_state.error_count > 0:
                    st.error(f"Errors: {st.session_state.error_count}")
                
                if st.session_state.warning_count > 0:
                    st.warning(f"Warnings: {st.session_state.warning_count}")
                
                if st.button("Reset Error Counters"):
                    st.session_state.error_count = 0
                    st.session_state.warning_count = 0
                    st.rerun()

error_handler = ErrorHandler()

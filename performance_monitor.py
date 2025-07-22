import time
import streamlit as st
import psutil
import os
from datetime import datetime
from debug_logger import debug_logger

class PerformanceMonitor:
    """Monitor application performance and resource usage"""
    
    def __init__(self):
        self.start_time = time.time()
        self.operation_times = {}
        
    def start_operation(self, operation_name):
        """Start timing an operation"""
        self.operation_times[operation_name] = time.time()
        debug_logger.log_function_entry(f"PERF_START: {operation_name}")
        
    def end_operation(self, operation_name):
        """End timing an operation and log results"""
        if operation_name in self.operation_times:
            duration = time.time() - self.operation_times[operation_name]
            debug_logger.log_performance(operation_name, duration)
            
            # Display in UI if debug mode
            if hasattr(st.session_state, 'debug_mode') and st.session_state.debug_mode:
                st.info(f"⏱️ {operation_name}: {duration:.2f}s")
            
            del self.operation_times[operation_name]
            return duration
        return 0
    
    def get_system_metrics(self):
        """Get current system metrics"""
        try:
            process = psutil.Process(os.getpid())
            
            metrics = {
                'cpu_percent': psutil.cpu_percent(interval=1),
                'memory_percent': psutil.virtual_memory().percent,
                'memory_used_mb': process.memory_info().rss / 1024 / 1024,
                'memory_available_mb': psutil.virtual_memory().available / 1024 / 1024,
                'disk_usage_percent': psutil.disk_usage('/').percent,
                'uptime_seconds': time.time() - self.start_time
            }
            
            return metrics
        except Exception as e:
            debug_logger.log_error(e, "Failed to get system metrics")
            return {}
    
    def display_performance_metrics(self):
        """Display performance metrics in sidebar"""
        if hasattr(st.session_state, 'debug_mode') and st.session_state.debug_mode:
            with st.sidebar:
                st.markdown("---")
                st.subheader("📊 Performance Metrics")
                
                metrics = self.get_system_metrics()
                
                if metrics:
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.metric("CPU %", f"{metrics.get('cpu_percent', 0):.1f}")
                        st.metric("Memory %", f"{metrics.get('memory_percent', 0):.1f}")
                    
                    with col2:
                        st.metric("Memory MB", f"{metrics.get('memory_used_mb', 0):.1f}")
                        st.metric("Uptime", f"{metrics.get('uptime_seconds', 0):.0f}s")
                
                # Active operations
                if self.operation_times:
                    st.write("**Active Operations:**")
                    for op, start_time in self.operation_times.items():
                        duration = time.time() - start_time
                        st.text(f"• {op}: {duration:.1f}s")
    
    def monitor_memory_usage(self, threshold_mb=500):
        """Monitor memory usage and warn if threshold exceeded"""
        metrics = self.get_system_metrics()
        memory_used = metrics.get('memory_used_mb', 0)
        
        if memory_used > threshold_mb:
            debug_logger.log_warning(
                f"High memory usage: {memory_used:.1f}MB",
                f"Threshold: {threshold_mb}MB"
            )
            
            if hasattr(st.session_state, 'debug_mode') and st.session_state.debug_mode:
                st.warning(f"⚠️ High memory usage: {memory_used:.1f}MB")

# Global performance monitor instance
perf_monitor = PerformanceMonitor()

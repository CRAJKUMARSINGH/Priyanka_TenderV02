import streamlit as st
from datetime import datetime
from date_utils import DateUtils

def create_header():
    """Create the enhanced application header with professional styling."""
    st.markdown("""
    <div style="
        text-align: center; 
        padding: 25px; 
        background: linear-gradient(135deg, #1f77b4, #2c3e50); 
        border-radius: 12px; 
        margin-bottom: 30px;
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
    ">
        <h1 style="
            color: white; 
            margin: 0; 
            font-size: 2.8em; 
            font-weight: 700;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        ">
            🏗️ Tender Processing System
        </h1>
        <p style="
            color: #ecf0f1; 
            margin: 15px 0 0 0; 
            font-size: 1.3em;
            font-weight: 500;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
        ">
            PWD Electric Division - Government Engineering Office
        </p>
        <div style="
            margin-top: 15px;
            padding: 8px 16px;
            background: rgba(255,255,255,0.1);
            border-radius: 20px;
            display: inline-block;
        ">
            <span style="color: #ffffff; font-size: 0.9em; font-weight: 500;">
                🔐 Secure • 📊 Efficient • 🎯 Accurate • 🌐 Modern • 📅 Enhanced Date Handling
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

def create_footer():
    """Create the enhanced application footer with professional styling and date utilities."""
    date_utils = DateUtils()
    current_date = date_utils.get_current_date()
    current_time = datetime.now().strftime('%H:%M:%S')
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        st.markdown(f"""
        <div style="
            text-align: center; 
            padding: 15px;
            background: linear-gradient(135deg, #f8f9fa, #e9ecef);
            border-radius: 10px;
            border-left: 4px solid #17a2b8;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        ">
            <p style="color: #495057; font-size: 0.9em; margin: 0; font-weight: 600;">
                🕒 Current Time<br>
                <strong style="color: #2c3e50;">{current_date}</strong><br>
                <strong style="color: #2c3e50;">{current_time}</strong>
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="
            text-align: center; 
            padding: 25px; 
            background: linear-gradient(135deg, #667eea, #764ba2); 
            border-radius: 12px; 
            border-left: 4px solid #1f77b4;
            box-shadow: 0 4px 8px rgba(0,0,0,0.15);
        ">
            <h4 style="color: white; margin-bottom: 15px; font-weight: 700;">📋 System Information</h4>
            <p style="
                color: #f8f9fa; 
                line-height: 1.8;
                margin: 0;
                font-size: 1.05em;
                font-weight: 600;
            ">
                Professional Tender Processing System<br>
                Enhanced Date Handling & Document Generation<br>
                PWD Electric Division - Udaipur
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="
            text-align: center; 
            padding: 15px;
            background: linear-gradient(135deg, #28a745, #20c997);
            border-radius: 10px;
            border-left: 4px solid #28a745;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        ">
            <p style="color: white; font-size: 0.9em; margin: 0; font-weight: 600;">
                💼 System Version<br>
                <strong style="font-size: 1.1em;">v2.1.1</strong><br>
                <span style="font-size: 0.8em; opacity: 0.9;">Date-Fixed Pro</span>
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Enhanced copyright and additional info
    st.markdown("""
    <div style="
        text-align: center; 
        padding: 20px; 
        color: #6c757d; 
        font-size: 0.85em; 
        border-top: 2px solid #dee2e6; 
        margin-top: 30px;
        background: linear-gradient(135deg, #f8f9fa, #ffffff);
        border-radius: 8px;
    ">
        <p style="margin: 5px 0; font-weight: 600;">
            © 2024 PWD Electric Division Tender Processing System | Designed for Government Engineering Offices
        </p>
        <p style="margin: 10px 0; font-weight: 500;">
            🔒 Secure • 📊 Efficient • 🎯 Accurate • 🌐 Modern • 📅 Multi-Format Date Support • 📈 Enhanced Reporting
        </p>
        <p style="margin: 5px 0; font-size: 0.8em; color: #868e96;">
            Built with ❤️ for engineers, by engineers | Powered by Streamlit & Python | Date Bugs Fixed ✅
        </p>
    </div>
    """, unsafe_allow_html=True)

def show_balloons():
    """Show celebration balloons with enhanced custom message."""
    st.balloons()
    
    # Enhanced celebration message with better styling
    st.markdown("""
    <div style="
        text-align: center; 
        padding: 20px; 
        background: linear-gradient(135deg, #ff6b6b, #feca57); 
        border-radius: 12px; 
        margin: 15px 0;
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
        animation: pulse 2s infinite;
    ">
        <h3 style="
            color: white; 
            margin: 0; 
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            font-weight: 700;
            font-size: 1.8em;
        ">
            🎉 Congratulations! 🎉
        </h3>
        <p style="
            color: white; 
            margin: 10px 0 0 0; 
            font-size: 1.2em; 
            text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
            font-weight: 600;
        ">
            Operation completed successfully with enhanced date handling accuracy!
        </p>
        <div style="
            margin-top: 15px;
            font-size: 0.9em;
            opacity: 0.9;
        ">
            <span style="color: white;">✨ Professional • 🎯 Accurate • ⚡ Fast • 📅 Date-Safe</span>
        </div>
    </div>
    
    <style>
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    </style>
    """, unsafe_allow_html=True)

def create_info_card(title: str, content: str, icon: str = "ℹ️"):
    """Create an enhanced informational card with professional styling."""
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 25px;
        border-radius: 12px;
        margin: 20px 0;
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
        transition: transform 0.3s ease;
    " onmouseover="this.style.transform='translateY(-3px)'; this.style.boxShadow='0 8px 16px rgba(0,0,0,0.2)'" 
       onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 6px 12px rgba(0,0,0,0.15)'">
        <h4 style="
            color: white; 
            margin: 0 0 15px 0;
            font-weight: 700;
            font-size: 1.3em;
        ">
            {icon} {title}
        </h4>
        <p style="
            color: #f8f9fa; 
            margin: 0; 
            line-height: 1.7;
            font-size: 1.05em;
            font-weight: 500;
        ">
            {content}
        </p>
    </div>
    """, unsafe_allow_html=True)

def create_success_message(message: str):
    """Create an enhanced styled success message."""
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #28a745, #20c997);
        padding: 18px;
        border-radius: 10px;
        margin: 15px 0;
        border-left: 5px solid #155724;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        animation: slideIn 0.5s ease;
    ">
        <p style="
            color: white; 
            margin: 0; 
            font-weight: 700;
            font-size: 1.1em;
            display: flex;
            align-items: center;
        ">
            <span style="font-size: 1.2em; margin-right: 10px;">✅</span>
            {message}
        </p>
    </div>
    
    <style>
    @keyframes slideIn {{
        from {{ transform: translateX(-100%); opacity: 0; }}
        to {{ transform: translateX(0); opacity: 1; }}
    }}
    </style>
    """, unsafe_allow_html=True)

def create_warning_message(message: str):
    """Create an enhanced styled warning message."""
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #ffc107, #fd7e14);
        padding: 18px;
        border-radius: 10px;
        margin: 15px 0;
        border-left: 5px solid #856404;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        animation: slideIn 0.5s ease;
    ">
        <p style="
            color: white; 
            margin: 0; 
            font-weight: 700;
            font-size: 1.1em;
            display: flex;
            align-items: center;
        ">
            <span style="font-size: 1.2em; margin-right: 10px;">⚠️</span>
            {message}
        </p>
    </div>
    
    <style>
    @keyframes slideIn {{
        from {{ transform: translateX(-100%); opacity: 0; }}
        to {{ transform: translateX(0); opacity: 1; }}
    }}
    </style>
    """, unsafe_allow_html=True)

def create_error_message(message: str):
    """Create an enhanced styled error message."""
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #dc3545, #c82333);
        padding: 18px;
        border-radius: 10px;
        margin: 15px 0;
        border-left: 5px solid #721c24;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        animation: slideIn 0.5s ease;
    ">
        <p style="
            color: white; 
            margin: 0; 
            font-weight: 700;
            font-size: 1.1em;
            display: flex;
            align-items: center;
        ">
            <span style="font-size: 1.2em; margin-right: 10px;">❌</span>
            {message}
        </p>
    </div>
    
    <style>
    @keyframes slideIn {{
        from {{ transform: translateX(-100%); opacity: 0; }}
        to {{ transform: translateX(0); opacity: 1; }}
    }}
    </style>
    """, unsafe_allow_html=True)

def create_metric_card(label: str, value: str, delta: str = None, icon: str = "📊"):
    """Create an enhanced metric display card with professional styling."""
    delta_html = f"""
    <p style='
        color: #28a745; 
        font-size: 0.95em; 
        margin: 8px 0 0 0;
        font-weight: 600;
    '>
        {delta}
    </p>
    """ if delta else ""
    
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #ffffff, #f8f9fa);
        padding: 25px;
        border-radius: 12px;
        margin: 15px 0;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        border-left: 4px solid #1f77b4;
        text-align: center;
        transition: all 0.3s ease;
    " onmouseover="this.style.transform='translateY(-3px)'; this.style.boxShadow='0 6px 16px rgba(0,0,0,0.15)'" 
       onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 4px 8px rgba(0,0,0,0.1)'">
        <p style="
            color: #6c757d; 
            margin: 0; 
            font-size: 0.95em;
            font-weight: 600;
        ">
            {icon} {label}
        </p>
        <h3 style="
            color: #2c3e50; 
            margin: 15px 0 0 0;
            font-weight: 700;
            font-size: 2em;
        ">
            {value}
        </h3>
        {delta_html}
    </div>
    """, unsafe_allow_html=True)

def create_progress_indicator(current_step: int, total_steps: int, step_names: list):
    """Create an enhanced visual progress indicator with professional styling."""
    progress_percentage = (current_step / total_steps) * 100
    
    steps_html = ""
    for i, step_name in enumerate(step_names):
        if i < current_step:
            color = "#28a745"  # Green for completed
            icon = "✅"
            font_weight = "bold"
            opacity = "1"
        elif i == current_step:
            color = "#007bff"  # Blue for current
            icon = "🔄"
            font_weight = "bold"
            opacity = "1"
        else:
            color = "#dee2e6"  # Gray for pending
            icon = "⭕"
            font_weight = "normal"
            opacity = "0.7"
        
        steps_html += f"""
        <div style="
            display: flex; 
            align-items: center; 
            margin: 12px 0;
            opacity: {opacity};
        ">
            <span style="
                color: {color}; 
                font-size: 1.2em; 
                margin-right: 10px;
            ">
                {icon}
            </span>
            <span style="
                color: {color}; 
                font-weight: {font_weight};
                font-size: 1em;
            ">
                {step_name}
            </span>
        </div>
        """
    
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #f8f9fa, #ffffff);
        padding: 25px;
        border-radius: 12px;
        margin: 20px 0;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        border-left: 4px solid #1f77b4;
    ">
        <h4 style="
            color: #2c3e50; 
            margin: 0 0 20px 0;
            font-weight: 700;
        ">
            📋 Process Progress
        </h4>
        
        <div style="
            background: #dee2e6; 
            border-radius: 10px; 
            height: 8px; 
            margin: 20px 0;
            overflow: hidden;
        ">
            <div style="
                background: linear-gradient(90deg, #1f77b4, #28a745); 
                height: 100%; 
                width: {progress_percentage}%;
                border-radius: 10px;
                transition: width 0.5s ease;
            "></div>
        </div>
        
        <div style="margin-top: 20px;">
            {steps_html}
        </div>
        
        <p style="
            text-align: center; 
            color: #6c757d; 
            font-size: 0.9em; 
            margin-top: 20px;
            font-weight: 600;
        ">
            Step {current_step + 1} of {total_steps} ({progress_percentage:.1f}% Complete)
        </p>
    </div>
    """, unsafe_allow_html=True)

def show_date_parsing_status(original_date: str, parsed_date: datetime = None, formatted_date: str = ""):
    """Show date parsing status with visual feedback using DateUtils."""
    date_utils = DateUtils()
    
    if not parsed_date:
        parsed_date = date_utils.parse_date(original_date)
    
    if not formatted_date and parsed_date:
        formatted_date = date_utils.format_display_date(parsed_date)
    
    if parsed_date:
        status_html = f"""
        <div style="
            background: linear-gradient(135deg, #d4edda, #c3e6cb);
            padding: 15px;
            border-radius: 8px;
            border-left: 4px solid #28a745;
            margin: 10px 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        ">
            <p style="margin: 0; color: #155724; font-weight: 600;">
                ✅ Date Successfully Parsed & Validated
            </p>
            <div style="
                margin-top: 8px; 
                font-size: 0.9em; 
                background: rgba(255,255,255,0.3);
                padding: 8px;
                border-radius: 4px;
            ">
                <div style="color: #155724; margin: 2px 0;">
                    <strong>Original:</strong> {original_date}
                </div>
                <div style="color: #155724; margin: 2px 0;">
                    <strong>Formatted:</strong> {formatted_date}
                </div>
                <div style="color: #155724; margin: 2px 0;">
                    <strong>Parsed Date:</strong> {parsed_date.strftime('%B %d, %Y')}
                </div>
            </div>
        </div>
        """
    else:
        status_html = f"""
        <div style="
            background: linear-gradient(135deg, #f8d7da, #f5c6cb);
            padding: 15px;
            border-radius: 8px;
            border-left: 4px solid #dc3545;
            margin: 10px 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        ">
            <p style="margin: 0; color: #721c24; font-weight: 600;">
                ❌ Date Parsing Failed
            </p>
            <div style="
                margin-top: 8px; 
                font-size: 0.9em; 
                background: rgba(255,255,255,0.3);
                padding: 8px;
                border-radius: 4px;
            ">
                <div style="color: #721c24; margin: 2px 0;">
                    <strong>Original:</strong> {original_date}
                </div>
                <div style="color: #721c24; margin: 2px 0;">
                    <strong>Supported Formats:</strong> DD/MM/YYYY, DD-MM-YYYY, YYYY-MM-DD, DD.MM.YYYY
                </div>
            </div>
        </div>
        """
    
    st.markdown(status_html, unsafe_allow_html=True)

def create_date_input_with_validation(label: str, key: str = None, help_text: str = None):
    """Create a date input with enhanced validation and format support."""
    if help_text is None:
        help_text = "Supports multiple formats: DD/MM/YYYY, DD-MM-YYYY, YYYY-MM-DD, DD.MM.YYYY"
    
    date_str = st.text_input(label, key=key, help=help_text, placeholder="e.g., 25/12/2024 or 25-12-2024")
    
    if date_str:
        show_date_parsing_status(date_str)
    
    return date_str

def show_system_info():
    """Show enhanced system information with date handling capabilities."""
    date_utils = DateUtils()
    
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #e3f2fd, #bbdefb);
        padding: 20px;
        border-radius: 12px;
        margin: 20px 0;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        border-left: 4px solid #2196f3;
    ">
        <h4 style="
            color: #1565c0; 
            margin: 0 0 15px 0;
            font-weight: 700;
        ">
            🔧 System Information
        </h4>
        
        <div style="color: #1565c0; line-height: 1.6;">
            <p><strong>📅 Date Utils Version:</strong> Enhanced Multi-Format Support</p>
            <p><strong>🔄 Supported Date Formats:</strong> {len(date_utils.SUPPORTED_FORMATS)} formats</p>
            <p><strong>📤 Output Format:</strong> {date_utils.OUTPUT_FORMAT}</p>
            <p><strong>🖥️ Display Format:</strong> {date_utils.DISPLAY_FORMAT}</p>
            <p><strong>⏰ Current System Date:</strong> {date_utils.get_current_date()}</p>
        </div>
        
        <div style="
            margin-top: 15px;
            padding: 10px;
            background: rgba(255,255,255,0.3);
            border-radius: 6px;
            font-size: 0.9em;
        ">
            <strong>Supported Formats:</strong><br>
            • DD/MM/YYYY (25/12/2024)<br>
            • DD-MM-YYYY (25-12-2024)<br>
            • YYYY-MM-DD (2024-12-25)<br>
            • DD.MM.YYYY (25.12.2024)<br>
            • MM/DD/YYYY (12/25/2024)
        </div>
    </div>
    """, unsafe_allow_html=True)

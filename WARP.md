# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Overview

This is TenderLatexPro Enhanced v3.0 - A comprehensive tender processing system designed for government engineering offices, specifically for PWD (Public Works Department) operations. The system is built with Python and Streamlit, providing a web-based interface for processing tenders, managing bidders, and generating professional documents.

## Key Architecture Components

### Core Processing Pipeline
1. **Data Input Layer**: Excel/PDF parsers (`excel_parser.py`, `pdf_parser.py`)
2. **Processing Engine**: Tender processor (`tender_processor.py`) handles validation and calculations
3. **Document Generation**: LaTeX report generator (`latex_report_generator.py`) and PDF generator (`pdf_generator.py`)
4. **UI Layer**: Streamlit-based interface with custom themes (`app.py`, `ui_components.py`, `theme.py`)
5. **Storage Layer**: Database manager (`database_manager.py`) with SQLite backend

### Specialized Modules
- **Date Handling**: Enhanced date parsing with multiple format support (`date_utils.py`)
- **Template System**: Dynamic template processing (`template_processor.py`)
- **Validation Engine**: Comprehensive data validation (`validation.py`)
- **Performance Monitoring**: System performance tracking (`performance_monitor.py`)
- **Error Handling**: Centralized error management (`error_handler.py`)

## Common Development Commands

### Environment Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Alternative installation with dev dependencies
pip install -e ".[development]"
```

### Running the Application
```bash
# Start the Streamlit application
streamlit run app.py

# Run with custom port
streamlit run app.py --server.port 5000

# Run in headless mode (production)
streamlit run app.py --server.headless true
```

### Testing
```bash
# Run comprehensive tests
python -m pytest

# Run specific test modules
python test_framework.py
python comprehensive_tester.py

# Generate test data
python test_data_generator.py

# Run with coverage
pytest --cov=src --cov-report=html
```

### Code Quality
```bash
# Format code
black . --line-length 100

# Lint code
flake8 .

# Type checking
mypy src/
```

### Build and Package
```bash
# Build package
python -m build

# Install in development mode
pip install -e .
```

## Project Structure Patterns

### Module Organization
- **Single-purpose modules**: Each `.py` file handles a specific domain (tender processing, PDF generation, etc.)
- **Factory pattern**: Template processor uses factory pattern for different document types
- **Observer pattern**: Performance monitor observes system metrics
- **Strategy pattern**: Multiple date parsing strategies in `date_utils.py`

### Data Flow
1. Files uploaded → Parsed by appropriate parser → Validated → Processed → Stored → Reports generated
2. Bidder data → Validation → Analysis → Ranking → Document generation
3. Templates → Processing with data → LaTeX compilation → PDF output

### Configuration Management
- Streamlit config: `.streamlit/config.toml` (server settings, theme)
- Project metadata: `pyproject.toml` (dependencies, build config)
- Application settings: Stored in session state and database

## Critical Development Notes

### Date Handling
The system has enhanced date parsing capabilities supporting multiple formats:
- DD/MM/YYYY, DD-MM-YYYY, YYYY-MM-DD, DD.MM.YYYY, MM/DD/YYYY
- Always use `DateUtils` class for date operations - it handles format variations automatically
- Test date parsing thoroughly when modifying date-related functionality

### Database Operations  
- Uses SQLite with SQLAlchemy ORM
- Database manager handles all DB operations - don't bypass it
- Automatic backup and recovery features are built-in
- Session state maintains current operation context

### Template System
- LaTeX templates in `templates/` directory
- Jinja2 templating engine for dynamic content
- Multiple output formats: PDF, Word, Excel
- Template validation before processing

### Error Handling Strategy
- Centralized error handling via `error_handler.py`
- Debug logging throughout the application
- Performance monitoring with metrics collection
- User-friendly error messages in UI

### UI Patterns
- Component-based UI with `ui_components.py`
- Consistent theming via `theme.py`
- Responsive design with column layouts
- Progress indicators for long-running operations

## Testing Strategy

### Test Framework Structure
- `test_framework.py`: Main test coordinator
- `test_scenarios.py`: Specific test scenarios
- `test_data_generator.py`: Generate sample data for testing
- `comprehensive_tester.py`: Full system testing

### Test Types
- Unit tests for individual modules
- Integration tests for data flow
- UI tests for Streamlit components
- Performance tests for large datasets

### Sample Data
- `TEST_FILES/` contains sample Excel and PDF files
- `bidder_database.json` contains sample bidder data
- Generated test data available through test framework

## Performance Considerations

### Optimization Points
- File upload size limits (10MB default)
- Database query optimization for large datasets
- Memory management for PDF generation
- Caching for frequently accessed data

### Monitoring
- Built-in performance monitor tracks CPU, memory, disk usage
- Session-based metrics collection
- Error count and response time tracking
- System health indicators in sidebar

## Deployment Notes

### Production Setup
- Headless mode configuration ready
- Environment variables for sensitive settings
- Backup and recovery procedures built-in
- Health check endpoints available

### Security Considerations
- Input validation for all user data
- File type restrictions for uploads
- SQL injection protection via SQLAlchemy
- No hardcoded credentials in source code

## Special Files and Directories

### Key Directories
- `templates/`: LaTeX and document templates
- `outputs/`: Generated documents and reports
- `TEST_FILES/`: Sample files for testing
- `attached_assets/`: Static assets and resources
- `SAMPLE_OUTPUT/`: Example generated documents

### Configuration Files
- `.streamlit/config.toml`: Streamlit server and theme settings
- `pyproject.toml`: Project metadata and dependencies
- `requirements.txt`: Python package requirements

This system is specifically designed for government tender processing workflows and includes domain-specific validations, document templates, and business logic for PWD operations.

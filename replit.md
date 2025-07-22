# TenderLatexPro - Replit Development Guide

## Overview

TenderLatexPro is a comprehensive Streamlit-based application for processing tender documents, managing bidder data, and generating professional reports. The system handles Excel/PDF file uploads, parses tender information, manages bidder data, and generates LaTeX-based PDF reports with comprehensive testing and monitoring capabilities.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Framework**: Streamlit web application with custom CSS styling
- **UI Components**: File upload widgets, data tables, forms, and progress indicators
- **State Management**: Streamlit session state for maintaining user data across interactions
- **User Interface**: Single-page application with modular components for different functionalities

### Backend Architecture
- **Core Application**: Python-based modular architecture with specialized processors
- **Data Processing**: Separate modules for Excel parsing, PDF parsing, and template processing
- **Document Generation**: LaTeX-based report generation with PDF output
- **Testing Framework**: Comprehensive testing suite with performance monitoring and error handling

### Data Storage Solutions
- **Primary Database**: SQLite for lightweight, file-based data storage
- **Data Models**: Pandas DataFrames for in-memory data manipulation
- **File Storage**: Local filesystem for templates, outputs, and temporary files
- **Session Storage**: Streamlit session state for temporary user data

## Key Components

### Core Processing Modules
1. **TenderProcessor**: Main business logic for tender data processing
2. **ExcelParser**: Handles Excel file parsing and data extraction
3. **PDFParser**: Processes PDF documents for data extraction
4. **TemplateProcessor**: Manages document templates and customization
5. **LatexReportGenerator**: Generates professional PDF reports using LaTeX
6. **PDFGenerator**: Handles PDF creation and formatting
7. **UserManualGenerator**: Creates user documentation

### Data Management
1. **DatabaseManager**: SQLite database operations and data persistence
2. **ValidationManager**: Input validation and data integrity checks
3. **DateUtils**: Date formatting and manipulation utilities
4. **Utils**: General utility functions for formatting and validation

### Testing and Monitoring
1. **TestFramework**: Main testing controller and orchestration
2. **ComprehensiveTester**: Advanced testing interface and execution
3. **TestScenarios**: Predefined test cases and scenarios
4. **TestDataGenerator**: Generates test data for various scenarios
5. **DebugLogger**: Enhanced logging and debugging capabilities
6. **ErrorHandler**: Comprehensive error handling with retry logic
7. **PerformanceMonitor**: System performance tracking and metrics

## Data Flow

1. **File Upload**: Users upload Excel/PDF files containing tender data
2. **Data Parsing**: Appropriate parser extracts structured data from uploaded files
3. **Data Validation**: ValidationManager ensures data integrity and format compliance
4. **Data Processing**: TenderProcessor applies business logic and calculations
5. **Database Storage**: DatabaseManager persists processed data to SQLite
6. **Report Generation**: LatexReportGenerator creates professional PDF reports
7. **Output Delivery**: Generated documents are made available for download

## External Dependencies

### Core Dependencies
- **Streamlit**: Web application framework
- **Pandas**: Data manipulation and analysis
- **SQLite3**: Database operations (built-in Python)
- **LaTeX**: Document generation system (external dependency)

### Additional Libraries
- **psutil**: System performance monitoring
- **tempfile**: Temporary file management
- **zipfile**: Archive file handling
- **logging**: Application logging
- **datetime**: Date and time operations

### File System Dependencies
- **Templates Directory**: Stores document templates
- **Outputs Directory**: Generated documents storage
- **Logs Directory**: Application logs and debug information
- **Test Directories**: Testing outputs and temporary files

## Deployment Strategy

### Local Development
- Streamlit development server for rapid iteration
- Local SQLite database for development data
- File-based storage for simplicity
- Integrated testing framework for validation

### Production Considerations
- The application currently uses local file storage and SQLite
- For production deployment, consider:
  - Database migration to PostgreSQL for scalability
  - Cloud storage for file management
  - Load balancing for multiple users
  - Enhanced security for file uploads

### Testing Strategy
- Comprehensive test framework with multiple test modes
- Performance monitoring and benchmarking
- Error simulation and recovery testing
- Automated test data generation
- Debug logging for troubleshooting

### Directory Structure
```
/
├── app.py (main application)
├── templates/ (document templates)
├── outputs/ (generated documents)
├── logs/ (application logs)
├── test_outputs/ (testing artifacts)
├── test_logs/ (test execution logs)
└── temp/ (temporary files)
```

The architecture prioritizes modularity, testability, and maintainability while providing a comprehensive solution for tender document processing and report generation.
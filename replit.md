# Tender Processing System

## Overview

This is a Streamlit-based web application designed for processing tender-related documents for the PWD Electric Division. The system handles Notice Inviting Tender (NIT) documents, manages bidder information, generates official reports, and produces various tender-related documents in compliance with government standards.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

The application follows a modular Python architecture built on Streamlit for the frontend interface. The system is designed as a single-page application with multiple processing modules handling different aspects of tender management.

### Frontend Architecture
- **Framework**: Streamlit web framework providing rapid UI development
- **Layout**: Wide layout with expandable sidebar navigation for optimal user experience
- **UI Components**: Modular component system with custom themes and professional styling
- **Styling**: Custom CSS overlays that enhance Streamlit's default styling while maintaining usability
- **Interactive Elements**: File uploaders, form inputs, balloon animations, and success/warning messages

### Backend Architecture
- **Processing Engine**: Object-oriented Python classes handling core business logic
- **Session Management**: Streamlit session state for maintaining application state across user interactions
- **File Processing**: Temporary file handling for uploaded Excel and PDF documents
- **Document Generation**: Multiple output formats including HTML reports, Word documents, and PDF files
- **Data Persistence**: JSON-based storage for bidder database management

## Key Components

### Core Processing Modules
1. **TenderProcessor**: Main business logic handler for tender calculations, percentage validation, and bid amount computations
2. **ExcelParser**: NIT Excel file parsing with robust data extraction and validation
3. **BidderManager**: Complete bidder database management with CRUD operations and statistics tracking
4. **ReportGenerator**: HTML-based report generation with professional styling and formatting
5. **DocumentGenerator**: Word document generation for official tender documentation
6. **ComparativeStatementGenerator**: Official PWD format comparative statement generation
7. **LetterAcceptanceGenerator**: Generates official PWD format Letter of Acceptance
8. **WorkOrderGenerator**: Generates official PWD format Work Orders
9. **ScrutinySheetGenerator**: Generates official PWD format scrutiny sheets

### UI Component System
1. **Header Component**: Professional gradient header with branding and system title
2. **Footer Component**: Timestamped footer with system information
3. **Theme System**: Custom CSS styling that preserves Streamlit's core design principles
4. **Navigation**: Sidebar-based navigation with radio button selection for different operations

### Data Processing Components
1. **DateUtils**: Centralized date utility class for handling multiple date formats and operations
2. **Validation System**: Comprehensive input validation for percentages (-99.99% to +99.99%), currency amounts, and required fields
3. **Calculation Engine**: Precise bid amount calculations using estimated costs and percentage adjustments
4. **Format Handling**: Currency formatting with proper Indian number formatting and data sanitization
5. **File Parsers**: Support for Excel (.xlsx) file processing with pattern matching

## Data Flow

1. **File Upload**: Users upload NIT Excel files through the Streamlit file uploader
2. **Data Extraction**: ExcelParser processes the uploaded file and extracts work information including NIT numbers, dates, and cost estimates
3. **Bidder Management**: BidderManager handles bidder information storage and retrieval from JSON database
4. **Calculation Processing**: TenderProcessor calculates bid amounts based on estimated costs and percentage variations
5. **Document Generation**: Various generators create official PWD format documents (comparative statements, letters of acceptance, work orders, etc.)
6. **Report Output**: Final documents are generated as HTML/PDF for download or printing

## External Dependencies

### Python Libraries
- **streamlit**: Web application framework for the user interface
- **pandas**: Data manipulation and analysis for Excel file processing
- **json**: Data serialization for bidder database storage
- **datetime**: Date and time handling operations
- **tempfile**: Temporary file handling for uploads
- **logging**: Application logging and error tracking

### File Formats Supported
- **Input**: Excel (.xlsx) files for NIT data
- **Output**: HTML reports, PDF documents (via browser printing)
- **Storage**: JSON files for bidder database persistence

### Date Handling
- **Multiple Input Formats**: DD/MM/YYYY, DD-MM-YYYY, YYYY-MM-DD, DD.MM.YYYY, MM/DD/YYYY
- **Standardized Output**: DD/MM/YYYY for data storage, DD-MM-YYYY for document display
- **Enhanced Parsing**: Robust date validation and format conversion through DateUtils class

## Deployment Strategy

### Local Development
- Streamlit development server for rapid prototyping and testing
- File-based storage using JSON for bidder database
- Temporary file handling for document processing

### Production Considerations
- Session state management for multi-user scenarios
- File upload size limits and validation
- Error handling and logging for production stability
- Browser-based PDF generation for document output

### Data Persistence
- JSON-based bidder database with automatic backup
- Session state for temporary work data
- File-based configuration for system settings

### Security Considerations
- Input validation for all user inputs
- File type validation for uploads
- Session isolation for multiple users
- Sanitized HTML output for document generation

## Key Architectural Decisions

### Problem: Date Format Standardization
**Solution**: Centralized DateUtils class with multiple format support
**Rationale**: Government documents require consistent date formatting, but input sources may vary
**Pros**: Reliable date handling, consistent output formatting
**Cons**: Additional complexity for simple date operations

### Problem: Document Generation Requirements
**Solution**: Separate generator classes for each document type
**Rationale**: Each PWD document has specific formatting requirements
**Pros**: Maintainable code, accurate format compliance
**Cons**: Multiple classes to maintain

### Problem: Data Persistence
**Solution**: JSON-based file storage for bidder database
**Rationale**: Simple deployment without database dependencies
**Pros**: Easy backup, human-readable format, no external database required
**Cons**: Limited scalability for large datasets

### Problem: User Interface Complexity
**Solution**: Streamlit with custom CSS enhancements
**Rationale**: Rapid development while maintaining professional appearance
**Pros**: Quick development, built-in widgets, responsive design
**Cons**: Limited customization compared to full web frameworks
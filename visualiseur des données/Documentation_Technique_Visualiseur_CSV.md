# Documentation Technique Visualiseur CSV

## Author Information
- **Author:** Your Name
- **Email:** your.email@example.com

## Overview
This document provides a comprehensive technical documentation for the CSV Data Visualizer, a tool designed to process and visualize CSV data efficiently.

## Architecture
The architecture of the CSV Data Visualizer is multi-layered, featuring the following components:
1. **Input Layer:** Handles reading CSV files.
2. **Processing Layer:** Contains the business logic for data manipulation and analysis.
3. **Presentation Layer:** Responsible for rendering visualizations.

## Attributes
- **FilePath:** Path to the input CSV file.
- **Delimiter:** Character used to separate values in the CSV file.
- **DataFrame:** A data structure to hold the CSV data.

## Methods
- `load_csv(file_path)`: Loads data from the specified CSV file.
- `clean_data()`: Cleans the input data for processing.
- `visualize_data()`: Renders visual charts based on user specifications.

## Dependencies
- **Pandas:** For data manipulation.
- **Matplotlib:** For plotting graphs.
- **NumPy:** For numerical calculations.

## Execution Flow
1. User specifies the CSV file.
2. The application loads the data using `load_csv`.
3. Data is cleaned and pre-processed with `clean_data`.
4. The data visualization method is called to render the charts.

## Supported Formats
- CSV (Comma-Separated Values)
- XLSX (Excel Files)

## Available Chart Types
- Bar Chart
- Line Chart
- Pie Chart

## Data Management
The application handles data efficiently using a combination of in-memory storage and file I/O operations. It's crucial to ensure data integrity during the processing stages.

## Important Technical Points
- Ensure proper exception handling during file loading.
- Implement validation checks for CSV formats.

## Main Entry
The application entry point is controlled through the `main.py` file, which integrates all components and processes.

## Exception Handling
Robust mechanisms are put in place to handle:
- FileNotFoundError
- ValueErrors
- TypeErrors

## Known Limitations
- Currently supports only CSV and XLSX formats.
- Limited to datasets that fit into memory.

---

*Generated on 2026-03-14 10:08:50 UTC*
# Sales Analysis Report Generator

A simple Python program that analyzes sample sales data and generates reports.

## Features

- Analyzes sales data across different dimensions (categories, regions, months)
- Identifies top selling products
- Generates formatted console output
- Creates a CSV report file

## Requirements

- Python 3.6+
- No external dependencies (uses only standard library)

## Usage

Run the program with:

```
python sales_analysis.py
```

This will:
1. Load the sample data
2. Perform analysis
3. Print a report to the console
4. Generate a CSV file named `sales_report.csv`

## Sample Output

The program will generate a console report like:

```
==================================================
 SALES ANALYSIS REPORT 
==================================================

Total Sales: $5560.00

Sales by Category:
  Electronics: $4700.00
  Furniture: $860.00

Sales by Region:
  North: $2125.00
  South: $1635.00
  East: $650.00
  West: $600.00

Sales by Month:
  2023-01: $2150.00
  2023-02: $1825.00
  2023-03: $1585.00

Top Products by Sales:
  1. Laptop: $2500.00
  2. Smartphone: $1550.00
  3. Tablet: $500.00
  4. Desk: $350.00
  5. Bookshelf: $250.00

==================================================
```

And a CSV file with similar information.

## Extending the Program

You can extend this program by:
- Loading data from external sources (CSV, database, API)
- Adding more analysis metrics
- Creating additional report formats (HTML, PDF, etc.)
- Implementing a command-line interface with options 
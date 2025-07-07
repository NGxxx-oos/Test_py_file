import argparse
import csv
import sys
from typing import List, Dict, Any, Optional, Union
from tabulate import tabulate


class CSVProcessor:
    """Main class for processing CSV files with filtering and aggregation."""
    
    def __init__(self, filepath: str):
        """Initialize processor with CSV file path."""
        self.filepath = filepath
        self.data: List[Dict[str, str]] = []
        self.headers: List[str] = []
        
    def load_data(self) -> None:
        """Load CSV data from file."""
        try:
            with open(self.filepath, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                self.headers = reader.fieldnames or []
                self.data = list(reader)
        except FileNotFoundError:
            print(f"Error: File '{self.filepath}' not found.")
            sys.exit(1)
        except Exception as e:
            print(f"Error reading file: {e}")
            sys.exit(1)
    
    def filter_data(self, column: str, operator: str, value: str) -> List[Dict[str, str]]:
        """Filter data based on column, operator, and value."""
        if column not in self.headers:
            print(f"Error: Column '{column}' not found in CSV file.")
            sys.exit(1)
        
        filtered_data = []
        
        for row in self.data:
            row_value = row[column]
            
            
            try:
                numeric_row_value = float(row_value)
                numeric_filter_value = float(value)
                
                if operator == '>' and numeric_row_value > numeric_filter_value:
                    filtered_data.append(row)
                elif operator == '<' and numeric_row_value < numeric_filter_value:
                    filtered_data.append(row)
                elif operator == '=' and numeric_row_value == numeric_filter_value:
                    filtered_data.append(row)
                    
            except ValueError:
                
                if operator == '=' and row_value == value:
                    filtered_data.append(row)
                elif operator == '>' and row_value > value:
                    filtered_data.append(row)
                elif operator == '<' and row_value < value:
                    filtered_data.append(row)
        
        return filtered_data
    
    def aggregate_data(self, column: str, operation: str) -> Dict[str, Any]:
        """Aggregate data based on column and operation."""
        if column not in self.headers:
            print(f"Error: Column '{column}' not found in CSV file.")
            sys.exit(1)
        
        
        numeric_values = []
        for row in self.data:
            try:
                numeric_values.append(float(row[column]))
            except ValueError:
                print(f"Error: Column '{column}' contains non-numeric values. Aggregation requires numeric data.")
                sys.exit(1)
        
        if not numeric_values:
            print(f"Error: No numeric values found in column '{column}'.")
            sys.exit(1)
        
        result = {}
        
        if operation == 'avg':
            result['operation'] = 'Average'
            result['column'] = column
            result['value'] = sum(numeric_values) / len(numeric_values)
        elif operation == 'min':
            result['operation'] = 'Minimum'
            result['column'] = column
            result['value'] = min(numeric_values)
        elif operation == 'max':
            result['operation'] = 'Maximum'
            result['column'] = column
            result['value'] = max(numeric_values)
        else:
            print(f"Error: Unknown aggregation operation '{operation}'. Supported: avg, min, max.")
            sys.exit(1)
        
        return result
    
    def display_table(self, data: List[Dict[str, str]]) -> None:
        """Display data as formatted table."""
        if not data:
            print("No data to display.")
            return
        
        
        table_data = []
        for row in data:
            table_data.append([row.get(header, '') for header in self.headers])
        
        print(tabulate(table_data, headers=self.headers, tablefmt='grid'))
    
    def display_aggregation(self, result: Dict[str, Any]) -> None:
        """Display aggregation result."""
        table_data = [
            ['Operation', result['operation']],
            ['Column', result['column']],
            ['Value', f"{result['value']:.2f}"]
        ]
        print(tabulate(table_data, headers=['Metric', 'Value'], tablefmt='grid'))


def parse_filter_condition(condition: str) -> tuple[str, str, str]:
    """Parse filter condition string into column, operator, and value."""
    operators = ['>=', '<=', '>', '<', '=']
    
    for op in operators:
        if op in condition:
            parts = condition.split(op, 1)
            if len(parts) == 2:
                return parts[0].strip(), op, parts[1].strip()
    
    print(f"Error: Invalid filter condition '{condition}'. Use format: column=value, column>value, column<value")
    sys.exit(1)


def parse_aggregate_condition(condition: str) -> tuple[str, str]:
    """Parse aggregate condition string into column and operation."""
    if '=' not in condition:
        print(f"Error: Invalid aggregate condition '{condition}'. Use format: column=operation")
        sys.exit(1)
    
    parts = condition.split('=', 1)
    if len(parts) != 2:
        print(f"Error: Invalid aggregate condition '{condition}'. Use format: column=operation")
        sys.exit(1)
    
    column = parts[0].strip()
    operation = parts[1].strip()
    
    if operation not in ['avg', 'min', 'max']:
        print(f"Error: Unknown operation '{operation}'. Supported: avg, min, max")
        sys.exit(1)
    
    return column, operation


def main():
    """Main function to handle command line arguments and process CSV."""
    parser = argparse.ArgumentParser(
        description='Process CSV files with filtering and aggregation capabilities.'
    )
    
    parser.add_argument(
        'file',
        help='Path to the CSV file to process'
    )
    
    parser.add_argument(
        '--where',
        help='Filter condition (e.g., "price>100", "brand=apple", "rating<4.5")',
        default=None
    )
    
    parser.add_argument(
        '--aggregate',
        help='Aggregation condition (e.g., "price=avg", "rating=min", "price=max")',
        default=None
    )
    
    args = parser.parse_args()
    
   
    if args.where and args.aggregate:
        print("Error: Cannot use both --where and --aggregate simultaneously.")
        sys.exit(1)
    
    if not args.where and not args.aggregate:
        print("Error: Must specify either --where or --aggregate option.")
        sys.exit(1)
    
    
    processor = CSVProcessor(args.file)
    processor.load_data()
    
    
    if args.where:
        column, operator, value = parse_filter_condition(args.where)
        filtered_data = processor.filter_data(column, operator, value)
        print(f"Filtered results for: {column} {operator} {value}")
        print(f"Found {len(filtered_data)} records:")
        print()
        processor.display_table(filtered_data)
    
    elif args.aggregate:
        column, operation = parse_aggregate_condition(args.aggregate)
        result = processor.aggregate_data(column, operation)
        print(f"Aggregation results:")
        print()
        processor.display_aggregation(result)


if __name__ == '__main__':
    main()

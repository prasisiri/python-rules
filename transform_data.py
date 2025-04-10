#!/usr/bin/env python3

import pandas as pd
import argparse
import os
import datetime


def load_data(sales_file, customer_file, product_file):
    """Load the raw data files"""
    try:
        print(f"Loading sales data from {sales_file}")
        sales_data = pd.read_csv(sales_file)
        print(f"Successfully loaded sales data with {len(sales_data)} rows")
        
        print(f"Loading customer data from {customer_file}")
        customer_data = pd.read_csv(customer_file)
        print(f"Successfully loaded customer data with {len(customer_data)} rows")
        
        print(f"Loading product data from {product_file}")
        product_data = pd.read_csv(product_file)
        print(f"Successfully loaded product data with {len(product_data)} rows")
        
        return sales_data, customer_data, product_data
    except Exception as e:
        print(f"Error loading data: {str(e)}")
        raise


def transform_data(sales_data, customer_data, product_data):
    """Transform and merge the data"""
    print("Transforming and merging data...")
    
    # Create a copy to avoid modifying the original
    transformed_data = sales_data.copy()
    
    # Add customer information
    if 'customer_id' in transformed_data.columns and 'customer_id' in customer_data.columns:
        transformed_data = pd.merge(
            transformed_data, 
            customer_data, 
            on='customer_id', 
            how='left',
            suffixes=('', '_customer')
        )
    
    # Add product information
    if 'product_id' in transformed_data.columns and 'product_id' in product_data.columns:
        transformed_data = pd.merge(
            transformed_data, 
            product_data, 
            on='product_id', 
            how='left',
            suffixes=('', '_product')
        )
    
    # Handle missing values
    for column in transformed_data.columns:
        if transformed_data[column].dtype == 'object':
            # Fill missing text values
            transformed_data[column] = transformed_data[column].fillna('Unknown')
        else:
            # Fill missing numeric values with 0
            transformed_data[column] = transformed_data[column].fillna(0)
    
    # Add calculated fields
    if 'price' in transformed_data.columns and 'quantity' in transformed_data.columns:
        transformed_data['total_amount'] = transformed_data['price'] * transformed_data['quantity']
    
    # Add date-related fields
    if 'date' in transformed_data.columns:
        transformed_data['date'] = pd.to_datetime(transformed_data['date'])
        transformed_data['year'] = transformed_data['date'].dt.year
        transformed_data['month'] = transformed_data['date'].dt.month
        transformed_data['day'] = transformed_data['date'].dt.day
        transformed_data['weekday'] = transformed_data['date'].dt.dayofweek
    
    print(f"Transformation complete. Output has {len(transformed_data)} rows and {len(transformed_data.columns)} columns")
    return transformed_data


def save_transformed_data(data, output_file):
    """Save the transformed data to a CSV file"""
    print(f"Saving transformed data to {output_file}")
    
    # Create output directory if it doesn't exist
    output_dir = os.path.dirname(output_file)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Save to CSV
    data.to_csv(output_file, index=False)
    print(f"Transformed data saved to {output_file}")


def main():
    parser = argparse.ArgumentParser(description="Transform and merge data from multiple sources")
    parser.add_argument("--sales", required=True, help="Path to the sales data file")
    parser.add_argument("--customers", required=True, help="Path to the customer data file")
    parser.add_argument("--products", required=True, help="Path to the product data file")
    parser.add_argument("--output", "-o", required=True, help="Path for the output transformed data")
    
    args = parser.parse_args()
    
    # Load, transform, and save data
    sales_data, customer_data, product_data = load_data(args.sales, args.customers, args.products)
    transformed_data = transform_data(sales_data, customer_data, product_data)
    save_transformed_data(transformed_data, args.output)
    
    print("Data transformation completed successfully")
    return 0


if __name__ == "__main__":
    exit(main()) 
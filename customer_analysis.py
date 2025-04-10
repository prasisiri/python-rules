#!/usr/bin/env python3

import pandas as pd
import argparse
import os
import datetime


def load_data(input_file):
    """Load the transformed data file"""
    try:
        print(f"Loading data from {input_file}")
        data = pd.read_csv(input_file)
        print(f"Successfully loaded data with {len(data)} rows")
        return data
    except Exception as e:
        print(f"Error loading data: {str(e)}")
        raise


def analyze_customer_data(data):
    """Perform customer-specific analysis on the data"""
    print("Performing customer analysis...")
    
    # Calculate metrics by customer
    customer_metrics = {
        "total_customers": data["customer_id"].nunique(),
        "sales_by_customer": data.groupby("customer_id")["price"].sum().to_dict(),
        "orders_by_customer": data.groupby("customer_id")["order_id"].nunique().to_dict(),
        "avg_order_value_by_customer": data.groupby("customer_id")["price"].mean().to_dict(),
        "total_sales": data["price"].sum(),
        "average_sales": data["price"].mean(),
    }
    
    # Calculate customer segments
    if "price" in data.columns:
        price_quantiles = data.groupby("customer_id")["price"].sum().quantile([0.25, 0.5, 0.75]).to_dict()
        low_value = price_quantiles[0.25]
        med_value = price_quantiles[0.5]
        high_value = price_quantiles[0.75]
        
        # Create segments based on total spend
        segments = {}
        for customer, total in customer_metrics["sales_by_customer"].items():
            if total < low_value:
                segments[customer] = "Low Value"
            elif total < med_value:
                segments[customer] = "Medium-Low Value"
            elif total < high_value:
                segments[customer] = "Medium-High Value"
            else:
                segments[customer] = "High Value"
                
        customer_metrics["customer_segments"] = segments
    
    print("Customer analysis completed")
    return customer_metrics


def generate_report(metrics, output_file):
    """Generate a CSV report with the analysis results"""
    print(f"Generating customer report: {output_file}")
    
    # Create a DataFrame for the customer segments
    if "customer_segments" in metrics:
        segments_df = pd.DataFrame.from_dict(
            metrics["customer_segments"], 
            orient="index", 
            columns=["Segment"]
        )
        segments_df.index.name = "customer_id"
        
        # Add total spend
        segments_df["Total Spend"] = segments_df.index.map(metrics["sales_by_customer"])
        
        # Add order count
        segments_df["Order Count"] = segments_df.index.map(metrics["orders_by_customer"])
        
        # Add average order value
        segments_df["Avg Order Value"] = segments_df.index.map(metrics["avg_order_value_by_customer"])
        
        # Sort by total spend descending
        segments_df = segments_df.sort_values("Total Spend", ascending=False)
        
        # Save to CSV
        segments_df.to_csv(output_file)
        print(f"Customer report saved to {output_file}")
        
        # Also save a summary file
        summary_file = os.path.splitext(output_file)[0] + "_summary.csv"
        with open(summary_file, "w") as f:
            f.write("Metric,Value\n")
            f.write(f"Report Date,{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total Customers,{metrics['total_customers']}\n")
            f.write(f"Total Sales,{metrics['total_sales']:.2f}\n")
            f.write(f"Average Sales per Customer,{metrics['total_sales']/metrics['total_customers']:.2f}\n")
            
            # Count customers by segment
            segment_counts = segments_df["Segment"].value_counts()
            for segment, count in segment_counts.items():
                f.write(f"Customers in {segment} segment,{count}\n")
                
        print(f"Customer summary report saved to {summary_file}")
    else:
        print("No customer segments available for reporting")


def main():
    parser = argparse.ArgumentParser(description="Analyze customer data and generate report")
    parser.add_argument("--input", "-i", required=True, help="Path to the input transformed data file")
    parser.add_argument("--output", "-o", required=True, help="Path for the output customer report")
    
    args = parser.parse_args()
    
    # Create output directory if it doesn't exist
    output_dir = os.path.dirname(args.output)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Load and analyze data
    data = load_data(args.input)
    metrics = analyze_customer_data(data)
    generate_report(metrics, args.output)
    
    print("Customer analysis completed successfully")
    return 0


if __name__ == "__main__":
    exit(main()) 
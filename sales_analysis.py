import csv
import datetime
from collections import defaultdict

# Sample sales data (in a real application, this might come from a file or database)
SAMPLE_DATA = [
    {"id": 1, "product": "Laptop", "category": "Electronics", "price": 1200, "date": "2023-01-15", "region": "North"},
    {"id": 2, "product": "Smartphone", "category": "Electronics", "price": 800, "date": "2023-01-20", "region": "South"},
    {"id": 3, "product": "Headphones", "category": "Electronics", "price": 150, "date": "2023-01-25", "region": "East"},
    {"id": 4, "product": "Desk", "category": "Furniture", "price": 350, "date": "2023-02-05", "region": "West"},
    {"id": 5, "product": "Chair", "category": "Furniture", "price": 175, "date": "2023-02-10", "region": "North"},
    {"id": 6, "product": "Laptop", "category": "Electronics", "price": 1300, "date": "2023-02-15", "region": "South"},
    {"id": 7, "product": "Tablet", "category": "Electronics", "price": 500, "date": "2023-03-01", "region": "East"},
    {"id": 8, "product": "Bookshelf", "category": "Furniture", "price": 250, "date": "2023-03-10", "region": "West"},
    {"id": 9, "product": "Smartphone", "category": "Electronics", "price": 750, "date": "2023-03-15", "region": "North"},
    {"id": 10, "product": "Lamp", "category": "Furniture", "price": 85, "date": "2023-03-20", "region": "South"},
]

def load_data():
    """Load sample sales data (simulating data loading from external source)"""
    return SAMPLE_DATA

def analyze_data(data):
    """Perform analysis on the sales data"""
    results = {
        "total_sales": 0,
        "sales_by_category": defaultdict(float),
        "sales_by_region": defaultdict(float),
        "sales_by_month": defaultdict(float),
        "top_products": [],
    }
    
    product_sales = defaultdict(float)
    
    for item in data:
        price = item["price"]
        category = item["category"]
        region = item["region"]
        date = datetime.datetime.strptime(item["date"], "%Y-%m-%d")
        month = date.strftime("%Y-%m")
        product = item["product"]
        
        # Calculate metrics
        results["total_sales"] += price
        results["sales_by_category"][category] += price
        results["sales_by_region"][region] += price
        results["sales_by_month"][month] += price
        product_sales[product] += price
    
    # Calculate top products by sales
    results["top_products"] = sorted(product_sales.items(), key=lambda x: x[1], reverse=True)
    
    return results

def generate_console_report(results):
    """Generate a formatted report for console output"""
    print("\n" + "="*50)
    print(" SALES ANALYSIS REPORT ")
    print("="*50)
    
    print(f"\nTotal Sales: ${results['total_sales']:.2f}")
    
    print("\nSales by Category:")
    for category, amount in results["sales_by_category"].items():
        print(f"  {category}: ${amount:.2f}")
    
    print("\nSales by Region:")
    for region, amount in results["sales_by_region"].items():
        print(f"  {region}: ${amount:.2f}")
    
    print("\nSales by Month:")
    for month, amount in sorted(results["sales_by_month"].items()):
        print(f"  {month}: ${amount:.2f}")
    
    print("\nTop Products by Sales:")
    for i, (product, amount) in enumerate(results["top_products"][:5], 1):
        print(f"  {i}. {product}: ${amount:.2f}")
    
    print("\n" + "="*50 + "\n")

def generate_csv_report(results, filename="sales_report.csv"):
    """Generate a CSV report file"""
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        
        # Write header and total
        writer.writerow(["Sales Analysis Report", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
        writer.writerow([])
        writer.writerow(["Total Sales", f"${results['total_sales']:.2f}"])
        writer.writerow([])
        
        # Write category sales
        writer.writerow(["Sales by Category"])
        for category, amount in results["sales_by_category"].items():
            writer.writerow([category, f"${amount:.2f}"])
        writer.writerow([])
        
        # Write region sales
        writer.writerow(["Sales by Region"])
        for region, amount in results["sales_by_region"].items():
            writer.writerow([region, f"${amount:.2f}"])
        writer.writerow([])
        
        # Write monthly sales
        writer.writerow(["Sales by Month"])
        for month, amount in sorted(results["sales_by_month"].items()):
            writer.writerow([month, f"${amount:.2f}"])
        writer.writerow([])
        
        # Write top products
        writer.writerow(["Top Products by Sales"])
        for i, (product, amount) in enumerate(results["top_products"][:5], 1):
            writer.writerow([f"{i}. {product}", f"${amount:.2f}"])
    
    print(f"CSV report generated: {filename}")

def main():
    # Load data
    data = load_data()
    
    # Analyze data
    results = analyze_data(data)
    
    # Generate reports
    generate_console_report(results)
    generate_csv_report(results)
    
    return results

if __name__ == "__main__":
    main() 
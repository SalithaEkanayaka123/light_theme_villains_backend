"""
Convert date column in CSV to dd-MM-yyyy format
"""

import pandas as pd

# File path
input_file = r'c:\Users\egekanayak\OneDrive - Wiley\Desktop\IIT\Big data Analysis\weatherData.csv'
output_file = r'c:\Users\egekanayak\OneDrive - Wiley\Desktop\IIT\Big data Analysis\weatherData_formatted1.csv'

try:
    # Read the CSV file
    print("Reading CSV file...")
    df = pd.read_csv(input_file)
    
    # Display available columns
    print(f"\nAvailable columns: {list(df.columns)}")
    
    # Display original date format (first 5 rows)
    print("\nOriginal date column (first 5 rows):")
    print(df.iloc[:, 0].head())  # Assuming date is first column
    
    # Convert date column to datetime, then format to dd-MM-yyyy
    # Adjust column name if needed (assuming first column is date)
    date_column = df.columns[1]
    
    print(f"\nConverting '{date_column}' column to dd-MM-yyyy format...")
    # Specify exact input format: dd-MM-yyyy with hyphens
    df[date_column] = pd.to_datetime(df[date_column], format='%d-%m-%Y').dt.strftime('%d-%m-%Y')
    
    # Display converted dates
    print("\nConverted date column (first 5 rows):")
    print(df[date_column].head())
    
    # Save to new CSV file
    df.to_csv(output_file, index=False)
    
    print(f"\n✅ Success! File saved to: {output_file}")
    
except FileNotFoundError:
    print(f"❌ Error: File not found at {input_file}")
    print("Please check the file path and try again.")
    
except Exception as e:
    print(f"❌ Error: {str(e)}")

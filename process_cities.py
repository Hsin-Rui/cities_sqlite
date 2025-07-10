#!/usr/bin/env python3
"""
GeoNames Cities Data Processor

This script reads data from the GeoNames cities15000.txt file and creates a SQLite database
containing only a curated subset of the data with specific columns.

Input: cities15000.txt (UTF-8 encoded TSV file with no header)
Output: cities.sqlite (SQLite database with 'cities' table)

Required columns from input (1-based index):
- Column 2: name (city name)
- Column 5: latitude (decimal degrees)
- Column 6: longitude (decimal degrees)
- Column 9: country_code (ISO 3166-1 alpha-2)
- Column 15: population (population count)
- Column 18: timezone (IANA timezone identifier)
"""

import sqlite3
import csv
import os
import sys

def main():
    # Define file names
    input_filename = 'cities15000.txt'
    output_filename = 'cities.sqlite'
    
    print("Starting GeoNames cities data processing...")
    
    # Check if input file exists
    try:
        if not os.path.exists(input_filename):
            raise FileNotFoundError(f"Input file '{input_filename}' not found")
        
        print(f"Found input file: {input_filename}")
        
        # Remove existing database file if it exists
        if os.path.exists(output_filename):
            os.remove(output_filename)
            print(f"Removed existing database file: {output_filename}")
        
        print("Creating database...")
        
        # Connect to SQLite database (creates new file)
        conn = sqlite3.connect(output_filename)
        cursor = conn.cursor()
        
        # Create the cities table with exact schema specified
        cursor.execute('''
            CREATE TABLE cities (
                name TEXT,
                country_code TEXT,
                latitude REAL,
                longitude REAL,
                timezone TEXT,
                population INTEGER
            )
        ''')
        
        print("Database table 'cities' created successfully")
        print("Processing data...")
        
        # Open and process the TSV file
        with open(input_filename, 'r', encoding='utf-8') as file:
            # Configure CSV reader for tab-delimited files
            csv_reader = csv.reader(file, delimiter='\t')
            
            record_count = 0
            
            for row in csv_reader:
                try:
                    # Extract required columns (convert to 0-based indexing)
                    # Column 2 (index 1): name
                    # Column 5 (index 4): latitude  
                    # Column 6 (index 5): longitude
                    # Column 9 (index 8): country_code
                    # Column 15 (index 14): population
                    # Column 18 (index 17): timezone
                    
                    if len(row) >= 18:  # Ensure row has enough columns
                        name = row[1].strip()
                        latitude = float(row[4]) if row[4].strip() else None
                        longitude = float(row[5]) if row[5].strip() else None
                        country_code = row[8].strip()
                        
                        # Handle population - may be empty
                        population_str = row[14].strip()
                        population = int(population_str) if population_str else None
                        
                        timezone = row[17].strip()
                        
                        # Insert data using parameterized query
                        cursor.execute('''
                            INSERT INTO cities (name, country_code, latitude, longitude, timezone, population)
                            VALUES (?, ?, ?, ?, ?, ?)
                        ''', (name, country_code, latitude, longitude, timezone, population))
                        
                        record_count += 1
                        
                        # Progress indicator for large files
                        if record_count % 1000 == 0:
                            print(f"Processed {record_count} records...")
                    
                except (ValueError, IndexError) as e:
                    # Skip malformed rows and continue processing
                    print(f"Warning: Skipping malformed row (error: {e})")
                    continue
        
        # Commit the transaction
        conn.commit()
        
        print(f"Data processing completed successfully!")
        print(f"Database '{output_filename}' created successfully with {record_count} records.")
        
        # Close database connection
        conn.close()
        
    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
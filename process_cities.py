#!/usr/bin/env python3
"""
GeoNames Cities Data Processor

This script reads data from the GeoNames cities15000.txt and countryInfo.txt files 
and creates a SQLite database with three tables: cities, countries, and timezones.

Input: 
- cities15000.txt (UTF-8 encoded TSV file with no header)
- countryInfo.txt (UTF-8 encoded TSV file with header)
Output: cities.sqlite (SQLite database with 'cities', 'countries', and 'timezones' tables)

Cities table columns from input (1-based index):
- Column 2: name (city name)
- Column 5: latitude (decimal degrees)
- Column 6: longitude (decimal degrees)
- Column 9: country_code (ISO 3166-1 alpha-2)
- Column 18: timezone (IANA timezone identifier)

Countries table columns from countryInfo.txt:
- country_code (ISO 3166-1 alpha-2)
- country_name

Timezones table:
- timezone_id (auto-generated primary key)
- timezone (IANA timezone identifier)
"""

import sqlite3
import csv
import os
import sys

def parse_country_info(filename):
    """Parse countryInfo.txt to extract country codes and names."""
    countries = {}
    
    if not os.path.exists(filename):
        print(f"Warning: {filename} not found. Countries table will be empty.")
        return countries
    
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                # Skip comments and empty lines
                if line.startswith('#') or not line:
                    continue
                
                # Split by tab
                parts = line.split('\t')
                if len(parts) >= 5:  # Ensure we have enough columns
                    country_code = parts[0].strip()
                    country_name = parts[4].strip()  # Column 5 is country name
                    if country_code and country_name:
                        countries[country_code] = country_name
    
    except Exception as e:
        print(f"Warning: Error reading {filename}: {e}")
    
    return countries

def main():
    # Define file names
    cities_input_filename = 'cities15000.txt'
    countries_input_filename = 'countryInfo.txt'
    output_filename = 'cities.sqlite'
    
    print("Starting GeoNames cities data processing...")
    
    # Check if input files exist
    try:
        if not os.path.exists(cities_input_filename):
            raise FileNotFoundError(f"Input file '{cities_input_filename}' not found")
        
        print(f"Found input file: {cities_input_filename}")
        
        # Parse country information
        print("Parsing country information...")
        countries = parse_country_info(countries_input_filename)
        print(f"Found {len(countries)} countries")
        
        # Remove existing database file if it exists
        if os.path.exists(output_filename):
            os.remove(output_filename)
            print(f"Removed existing database file: {output_filename}")
        
        print("Creating database...")
        
        # Connect to SQLite database (creates new file)
        conn = sqlite3.connect(output_filename)
        cursor = conn.cursor()
        
        # Create the countries table
        cursor.execute('''
            CREATE TABLE countries (
                country_code TEXT PRIMARY KEY,
                country_name TEXT
            )
        ''')
        
        # Create the timezones table
        cursor.execute('''
            CREATE TABLE timezones (
                timezone_id INTEGER PRIMARY KEY AUTOINCREMENT,
                timezone TEXT UNIQUE
            )
        ''')
        
        # Create the cities table (with timezone_id instead of timezone)
        cursor.execute('''
            CREATE TABLE cities (
                name TEXT,
                country_code TEXT,
                latitude REAL,
                longitude REAL,
                timezone_id INTEGER,
                FOREIGN KEY (country_code) REFERENCES countries (country_code),
                FOREIGN KEY (timezone_id) REFERENCES timezones (timezone_id)
            )
        ''')
        
        print("Database tables 'countries', 'timezones', and 'cities' created successfully")
        
        # Insert country data
        print("Inserting country data...")
        for country_code, country_name in countries.items():
            cursor.execute('''
                INSERT INTO countries (country_code, country_name)
                VALUES (?, ?)
            ''', (country_code, country_name))
        
        print(f"Inserted {len(countries)} countries")
        
        print("Processing cities data...")
        
        # Track unique timezones and their IDs
        timezone_cache = {}
        
        # Open and process the cities TSV file
        with open(cities_input_filename, 'r', encoding='utf-8') as file:
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
                    # Column 18 (index 17): timezone
                    
                    if len(row) >= 18:  # Ensure row has enough columns
                        name = row[1].strip()
                        latitude = float(row[4]) if row[4].strip() else None
                        longitude = float(row[5]) if row[5].strip() else None
                        country_code = row[8].strip()
                        timezone = row[17].strip()
                        
                        # Get or create timezone_id
                        if timezone not in timezone_cache:
                            # Insert new timezone
                            cursor.execute('''
                                INSERT OR IGNORE INTO timezones (timezone)
                                VALUES (?)
                            ''', (timezone,))
                            
                            # Get the timezone_id
                            cursor.execute('''
                                SELECT timezone_id FROM timezones WHERE timezone = ?
                            ''', (timezone,))
                            timezone_id = cursor.fetchone()[0]
                            timezone_cache[timezone] = timezone_id
                        else:
                            timezone_id = timezone_cache[timezone]
                        
                        # Insert city data using timezone_id
                        cursor.execute('''
                            INSERT INTO cities (name, country_code, latitude, longitude, timezone_id)
                            VALUES (?, ?, ?, ?, ?)
                        ''', (name, country_code, latitude, longitude, timezone_id))
                        
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
        
        # Get timezone count
        cursor.execute("SELECT COUNT(*) FROM timezones")
        timezone_count = cursor.fetchone()[0]
        
        print(f"Data processing completed successfully!")
        print(f"Database '{output_filename}' created successfully with:")
        print(f"  - {len(countries)} countries")
        print(f"  - {timezone_count} timezones")
        print(f"  - {record_count} cities")
        
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
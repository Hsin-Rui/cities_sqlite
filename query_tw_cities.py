
import sqlite3
import csv

db_file = 'cities.sqlite'
output_csv_file = 'taiwan_cities.csv'
country_code_to_select = 'TW'

# Connect to the SQLite database
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

# Execute the query
cursor.execute("SELECT name, country_code, latitude, longitude, timezone_id FROM cities WHERE country_code = ?", (country_code_to_select,))

# Fetch all the rows
rows = cursor.fetchall()

# Get the column names from the cursor description
column_names = [description[0] for description in cursor.description]

# Write the data to a CSV file
with open(output_csv_file, 'w', newline='', encoding='utf-8') as csvfile:
    csv_writer = csv.writer(csvfile)
    
    # Write the header
    csv_writer.writerow(column_names)
    
    # Write the data rows
    csv_writer.writerows(rows)

# Close the connection
conn.close()

print(f"Successfully exported {len(rows)} cities for country code '{country_code_to_select}' to '{output_csv_file}'")

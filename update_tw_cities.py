
import sqlite3
import csv

db_file = 'cities.sqlite'
input_csv_file = 'taiwan_cities.csv'
country_code_to_update = 'TW'

# Connect to the SQLite database
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

try:
    # 1. Delete existing 'TW' cities
    print(f"Deleting existing cities for country code '{country_code_to_update}'...")
    cursor.execute("DELETE FROM cities WHERE country_code = ?", (country_code_to_update,))
    deleted_count = cursor.rowcount
    print(f"Deleted {deleted_count} existing cities.")

    # 2. Read the CSV file and insert new cities
    print(f"Reading data from '{input_csv_file}' and inserting into database...")
    with open(input_csv_file, 'r', newline='', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        header = next(csv_reader)  # Skip header row

        inserted_count = 0
        for row in csv_reader:
            # Assuming the order of columns in CSV is: name, country_code, latitude, longitude, timezone_id
            name = row[0]
            country_code = row[1]
            latitude = float(row[2]) if row[2] else None
            longitude = float(row[3]) if row[3] else None
            timezone_id = int(row[4]) if row[4] else None

            cursor.execute('''
                INSERT INTO cities (name, country_code, latitude, longitude, timezone_id)
                VALUES (?, ?, ?, ?, ?)
            ''', (name, country_code, latitude, longitude, timezone_id))
            inserted_count += 1

    conn.commit()
    print(f"Successfully inserted {inserted_count} new cities from '{input_csv_file}'.")
    print("Database update complete.")

except Exception as e:
    conn.rollback()
    print(f"An error occurred: {e}")

finally:
    conn.close()

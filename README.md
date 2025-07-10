# GeoNames Cities Data Processor

This project processes GeoNames cities data from a TSV file and creates a SQLite database with a curated subset of the data.

## Files

- `process_cities.py` - Main Python script that processes the data
- `run_cities_processor.sh` - Shell script to run the processor in a virtual environment
- `cities15000.txt` - Input TSV file from GeoNames (UTF-8 encoded, no header)
- `cities.sqlite` - Output SQLite database (created by the script)
- `cities_env/` - Python virtual environment directory

## Requirements

- Python 3.x
- No external dependencies (uses only standard libraries)

## Usage

### Option 1: Using the shell script (recommended)
```bash
./run_cities_processor.sh
```

### Option 2: Manual virtual environment activation
```bash
# Create virtual environment (if not exists)
python3 -m venv cities_env

# Activate virtual environment
source cities_env/bin/activate

# Run the script
python process_cities.py

# Deactivate when done
deactivate
```

### Option 3: Direct execution (without virtual environment)
```bash
python3 process_cities.py
```

## Input Data Format

The script expects two input files:

### cities15000.txt
A tab-separated values file with the following columns (1-based indexing):
- Column 2: City name
- Column 5: Latitude (decimal degrees)
- Column 6: Longitude (decimal degrees)
- Column 9: Country code (ISO 3166-1 alpha-2)
- Column 18: Timezone (IANA identifier)

### countryInfo.txt
A tab-separated values file with country information:
- Column 1: Country code (ISO 3166-1 alpha-2)
- Column 5: Country name

## Output Database Schema

The `cities.sqlite` database contains three tables:

### countries table
```sql
CREATE TABLE countries (
    country_code TEXT PRIMARY KEY,
    country_name TEXT
);
```

### timezones table
```sql
CREATE TABLE timezones (
    timezone_id INTEGER PRIMARY KEY AUTOINCREMENT,
    timezone TEXT UNIQUE
);
```

### cities table
```sql
CREATE TABLE cities (
    name TEXT,
    country_code TEXT,
    latitude REAL,
    longitude REAL,
    timezone_id INTEGER,
    FOREIGN KEY (country_code) REFERENCES countries (country_code),
    FOREIGN KEY (timezone_id) REFERENCES timezones (timezone_id)
);
```

## Features

- ✅ UTF-8 encoding support
- ✅ Parameterized SQL queries (SQL injection prevention)
- ✅ Error handling for malformed data
- ✅ Progress indicators during processing
- ✅ Automatic cleanup of existing database files
- ✅ Virtual environment isolation

## Example Output

```
Starting GeoNames cities data processing...
Found input file: cities15000.txt
Creating database...
Database table 'cities' created successfully
Processing data...
Processed 1000 records...
...
Data processing completed successfully!
Database 'cities.sqlite' created successfully with 31534 records.
```
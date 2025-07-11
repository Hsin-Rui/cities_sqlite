# GeoNames Cities Data 

This project processes GeoNames cities data from a TSV file and creates a SQLite database with a curated subset of the data. Additionally, it provides scripts to query and update Taiwan city data within the same database.

## Files

- `process_cities.py` - Main Python script that processes GeoNames data and populates the `cities.sqlite` database.
- `run_cities_processor.sh` - Shell script to run the `process_cities.py` in a virtual environment.
- `query_tw_cities.py` - Python script to query Taiwan cities from `cities.sqlite` and export them to `taiwan_cities.csv`.
- `update_tw_cities.py` - Python script to update Taiwan city data in `cities.sqlite` based on `taiwan_cities.csv`.
- `cities15000.txt` - Input TSV file from GeoNames (UTF-8 encoded, no header).
- `taiwan_cities.csv` - CSV file containing Taiwan city data, used for querying and updating.
- `cities.sqlite` - Output SQLite database (created by `process_cities.py`).

## Requirements

- Python 3.x
- No external dependencies (uses only standard libraries)

## Usage

### 1. Process GeoNames Data

#### Option 1. Manual virtual environment activation
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

#### Option 2: Direct execution (without virtual environment)
```bash
python3 process_cities.py
```

### 2. Query Taiwan Cities

To extract Taiwan city data from `cities.sqlite` into `taiwan_cities.csv`:

```bash
python query_tw_cities.py
```

### 3. Update Taiwan Cities

To update Taiwan city data in `cities.sqlite` using `taiwan_cities.csv` as the source:

```bash
python update_tw_cities.py
```

## Input Data Format

The `process_cities.py` script expects two input files:

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
- ✅ Query and update functionalities for specific country data (e.g., Taiwan)

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

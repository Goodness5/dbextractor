# Database Data Extractor

## Overview

The Database Data Extractor is a versatile utility designed to connect to various databases, retrieve table or collection data, and export it to CSV or XLSX (Excel) files. It supports PostgreSQL, SQLite, and MongoDB databases (MongoDB support is coming soon).

## Features

- **Database Connection:** Supports multiple connection methods:
  - Database URI
  - Raw connection details
  - PostgreSQL command (coming soon)
- **Data Filtering:** 
  - Filter data using column-based query parameters
  - Exclude specific records using exceptions (via CSV file or pasted data)
- **Data Export:** Exports data to CSV or XLSX files
- **Interactive User Interface:** Guides users through the connection, filtering, and export process

## Requirements

- Python 3.x
- Required Python packages: `psycopg2`, `sqlite3`, `pymongo`, `openpyxl`
- Access to the respective database servers.

## Installation

Install the required Python packages using pip:

```bash
pip install psycopg2 pymongo openpyxl
```

## Usage

### Connecting to a Database

You can connect to the database in multiple ways:

1. **Database URI** (Option 3):
   - PostgreSQL: `postgresql://username:password@host:port/database`
   - SQLite: `sqlite:///path/to/database.db`

2. **Raw Entry** (Option 2):
   - Manually enter host, database name, username, and password

3. **PostgreSQL Command** (Option 1 - Coming Soon):
   - Paste your PostgreSQL connection command

### Running the Tool

1. **Start the Script:**
   ```bash
   python3 main.py
   ```

2. **Select Connection Method:**
   Choose between:
   - Option 1: PostgreSQL command (coming soon)
   - Option 2: Raw connection details
   - Option 3: Database URI

3. **Select Table/Collection:**
   - Choose from the list of available tables

4. **Apply Filters (Optional):**
   - Enter column names and values to filter the data
   - Specify exclusions by column and provide exceptions via:
     - CSV file
     - Pasted data

5. **Choose Export Format:**
   - CSV (enter `c`)
   - XLSX (enter `x`)

## Functions

### `parse_database_uri(database_uri)`

- **Purpose:** Parses the SQLAlchemy database URI and extracts connection parameters.
- **Parameters:** `database_uri` (str) - The database URI.
- **Returns:** Dictionary containing `host`, `database`, `user`, and `password`.

### `connect_sqlite(db_path)`

- **Purpose:** Connects to a SQLite database.
- **Parameters:** `db_path` (str) - Path to the SQLite database file.
- **Returns:** SQLite connection object.

### `get_table_names(connection)`

- **Purpose:** Retrieves the names of all tables/collections from the connected database.
- **Parameters:** `connection` - Database connection object.
- **Returns:** List of table/collection names.

### `export_to_csv(connection, collection_or_table_name, csv_file, query_params, exception_field, exceptions)`

- **Purpose:** Exports filtered data from the specified table/collection to a CSV file
- **Parameters:**
  - `connection` - Database connection object
  - `collection_or_table_name` (str) - Name of the table/collection to export
  - `csv_file` (str) - Path to the output CSV file
  - `query_params` (dict) - Column-based filters to apply
  - `exception_field` (str) - Column name for exclusions
  - `exceptions` (list) - Values to exclude

### `convert_csv_to_xlsx(csv_file_path, xlsx_file_path)`

- **Purpose:** Converts a CSV file to an XLSX file.
- **Parameters:**
  - `csv_file_path` (str) - Path to the input CSV file.
  - `xlsx_file_path` (str) - Path to the output XLSX file.

### `read_exceptions_from_csv_or_input()`

- **Purpose:** Reads exception values from either a CSV file or pasted text
- **Returns:** List of exception values

### `main()`

- **Purpose:** Main function that prompts the user for input and coordinates the export process.

## Notes

- **MongoDB Support:** Currently, MongoDB export functionality is not implemented. Support for MongoDB is coming soon.
- **Temporary Files:** When exporting to XLSX, a temporary CSV file is created and then deleted after conversion.

## Troubleshooting

- **Database Connection Errors:** Ensure that the database URI is correctly formatted and that the database server is accessible.
- **Invalid Input:** Follow the prompts carefully and enter valid numbers and choices.

## Contributing

If you would like to contribute to this tool or report any issues, please create a pull request or issue on the project's GitHub repository or contact me on Twitter [@goodnesskolapo](https://twitter.com/goodnesskolapo) or Telegram [@goodnesskolapo](https://t.me/goodnesskolapo)
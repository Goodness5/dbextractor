# Database Export Tool Documentation

## Overview

The Database Export Tool is a versatile utility designed to connect to various databases, retrieve table or collection data, and export it to CSV or XLSX (Excel) files. It supports PostgreSQL, SQLite, and MongoDB databases (MongoDB support is coming soon).

## Features

- **Database Connection:** Connects to PostgreSQL, SQLite, and MongoDB databases.
- **Data Retrieval:** Retrieves data from specified tables or collections.
- **Data Export:** Exports data to CSV or XLSX files.
- **Interactive User Interface:** Prompts users for necessary inputs and guides them through the export process.

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

1. **Database URI:**
   - PostgreSQL: `postgresql://username:password@host:port/database`
   - SQLite: `sqlite:///path/to/database.db`
   - MongoDB: `mongodb+srv://username:password@host:port/database` (Support coming soon)

### Running the Tool

1. **Start the Script:**
   - Run the script from the command line:

     ```bash
     python3 export_tool.py
     ```

2. **Enter Database URI:**
   - When prompted, enter your database URI. The tool will automatically detect the type of database based on the URI.

3. **Select Table/Collection:**
   - The tool will list all available tables (for SQL databases) or collections (for MongoDB). Select the desired table/collection by entering the corresponding number.

4. **Choose Export Format:**
   - Choose between CSV (enter `c`) or XLSX (enter `x`) as the export format.

5. **Export Data:**
   - The tool will export the data from the selected table/collection to the specified format and save it in the current directory.

### Example Workflow

1. Run the tool:

   ```bash
   python main.py
   ```

2. Enter your database URI:

   ```bash
   Enter your database URI: postgresql://username:password@localhost:5432/mydatabase
   ```

3. Select a table:

   ```bash
   Available tables/collections:
   1. table1
   2. table2
   Select a table/collection by number: 1
   ```

4. Choose the export format:

   ```bash
   Do you want to export to CSV (c) or XLSX (x)? c
   ```

5. Export complete:

   ```bash
   Data from table/collection 'table1' has been successfully exported to table1.csv
   ```

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

### `export_to_csv(connection, collection_or_table_name, csv_file)`

- **Purpose:** Exports data from the specified table/collection to a CSV file.
- **Parameters:**
  - `connection` - Database connection object.
  - `collection_or_table_name` (str) - Name of the table/collection to export.
  - `csv_file` (str) - Path to the output CSV file.

### `convert_csv_to_xlsx(csv_file_path, xlsx_file_path)`

- **Purpose:** Converts a CSV file to an XLSX file.
- **Parameters:**
  - `csv_file_path` (str) - Path to the input CSV file.
  - `xlsx_file_path` (str) - Path to the output XLSX file.

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
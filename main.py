import csv
import os
import psycopg2
import sqlite3
from openpyxl import Workbook
from urllib.parse import urlparse


# Function to parse the SQLAlchemy Database URI
def parse_database_uri(database_uri):
    result = urlparse(database_uri)
    print("parsed url:", result)
    return {
        "host": result.hostname,
        "database": result.path[1:],  # Skip the leading '/'
        "user": result.username,
        "password": result.password,
    }


# Function to connect to a SQLite database
def connect_sqlite(db_path):
    conn = sqlite3.connect(db_path)
    return conn


def convert_csv_to_xlsx(csv_file_path, xlsx_file_path):
    wb = Workbook()
    ws = wb.active

    with open(csv_file_path, mode="r", encoding="utf-8") as csv_file:
        csv_reader = csv.reader(csv_file)
        headers = next(csv_reader)  # Store the header row

        for row in csv_reader:
            ws.append(row)  # Append each row to the worksheet

    # Write the headers to the first row of the worksheet
    for col_num, header in enumerate(headers, 1):
        ws.cell(row=1, column=col_num, value=header)

    wb.save(xlsx_file_path)
    print(
        f"CSV file '{csv_file_path}' has been converted to Excel file '{xlsx_file_path}'"
    )


# Function to get table names from the database
def get_table_names(connection):
    if isinstance(connection, psycopg2.extensions.connection):
        cursor = connection.cursor()
        cursor.execute(
            "SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND table_type='BASE TABLE';"
        )
        tables = cursor.fetchall()
        table_names = [table[0] for table in tables]
    elif isinstance(connection, sqlite3.Connection):
        cursor = connection.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        table_names = [table[0] for table in tables]
    else:
        raise Exception("Unsupported database type")
    return table_names


# Function to export data from a selected collection/table to a CSV file, excluding exceptions
def export_to_csv(connection, collection_or_table_name, csv_file, query_params, exception_field=None, exceptions=None):
    cursor = None 

    if isinstance(connection, psycopg2.extensions.connection):
        query = f"SELECT * FROM public.{collection_or_table_name}"
        conditions = []

        # Add query parameters if provided
        if query_params:
            conditions += [f"{key} = '{value}'" for key, value in query_params.items()]

        # Add exceptions if provided
        if exception_field and exceptions:
            exclusion_list = "', '".join(exceptions)
            conditions.append(f"{exception_field} NOT IN ('{exclusion_list}')")

        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        query += ";"

        cursor = connection.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        headers = [desc[0] for desc in cursor.description]

        with open(csv_file, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(headers)
            writer.writerows(rows)

    elif isinstance(connection, sqlite3.Connection):
        query = f"SELECT * FROM {collection_or_table_name}"
        conditions = []

        # Add query parameters if provided
        if query_params:
            conditions += [f"{key} = '{value}'" for key, value in query_params.items()]

        # Add exceptions if provided
        if exception_field and exceptions:
            exclusion_list = "', '".join(exceptions)
            conditions.append(f"{exception_field} NOT IN ('{exclusion_list}')")

        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        query += ";"

        cursor = connection.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        headers = [desc[0] for desc in cursor.description]

        with open(csv_file, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(headers)
            writer.writerows(rows)

    else:
        raise Exception("Unsupported database type")

    if cursor:  
        cursor.close()  # Close the cursor after use
    print(
        f"Data from collection/table '{collection_or_table_name}' has been successfully exported to {csv_file}"
    )


# Function to read exceptions from a CSV or pasted text
def read_exceptions_from_csv_or_input():
    exceptions = []
    exception_input_type = input("Do you want to provide exceptions via a CSV file (c) or paste data (p)? ").lower()

    if exception_input_type == "c":
        file_path = input("Enter the path to the exceptions CSV file: ")
        if os.path.exists(file_path):
            with open(file_path, mode="r", encoding="utf-8") as file:
                reader = csv.reader(file)
                exceptions = [row[0] for row in reader]  # Assuming exceptions are in the first column
        else:
            print("File not found. No exceptions will be applied.")
    elif exception_input_type == "p":
        pasted_data = input("Paste the exceptions data (one per line): ")
        exceptions = [line.strip() for line in pasted_data.split("\n") if line.strip()]

    return exceptions


def main():
    # Prompt the user for the type of input
    input_type = input("Select input type (1: PSQL command, 2: Raw entry, 3: Database URI): ")

    connection = None

    if input_type == "1":
        # TODO:
        # Allow user to paste a PostgreSQL command
        psql_command = input("Paste your PostgreSQL command: ")
        # Extract connection details from the command (this is a placeholder, implement parsing logic)
        # connection = parse_psql_command(psql_command) 

    elif input_type == "2":
        # Basic raw entry of host, user, password, etc.
        host = input("Enter the host: ")
        database = input("Enter the database name: ")
        user = input("Enter the user: ")
        password = input("Enter the password: ")
        connection = psycopg2.connect(host=host, database=database, user=user, password=password)

    elif input_type == "3":
        # Database URI input
        database_uri = input("Enter your database URI: ")
        connection_params = parse_database_uri(database_uri)
        connection = psycopg2.connect(**connection_params)

    else:
        print("Invalid input type selected.")
        return

    # Get table/collection names
    tables = get_table_names(connection)
    if not tables:
        print("No tables/collections found in the database.")
        return

    # Display the tables/collections and let the user select one
    print("Available tables/collections:")
    for i, table in enumerate(tables, start=1):
        print(f"{i}. {table}")

    try:
        table_index = int(input("Select a table/collection by number: ")) - 1
        if table_index < 0 or table_index >= len(tables):
            print("Invalid selection.")
            return

        table_name = tables[table_index]

        # Prompt the user for query parameters
        query_params = {}
        while True:
            key = input("Enter the column name to filter by (or press Enter to finish): ")
            if not key:
                break
            value = input(f"Enter the value for {key}: ")
            query_params[key] = value

        # Prompt the user for exceptions
        exception_field = input("Enter the column name for exclusions (or press Enter to skip): ")
        exceptions = []
        if exception_field:
            exceptions = read_exceptions_from_csv_or_input()

        # Ask the user what type of file they want to export
        file_format = input("Do you want to export to CSV (c) or XLSX (x)? ").lower()
        if file_format not in ["c", "x"]:
            print("Invalid choice. Exiting.")
            return

        # Construct the output file name based on the user's choice
        if file_format == "c":
            output_file = f"{table_name}.csv"
        else:
            output_file = f"{table_name}.xlsx"

        # Export the selected table/collection to the chosen format
        if file_format == "c":
            export_to_csv(connection, table_name, output_file, query_params, exception_field, exceptions)
        elif file_format == "x":
            csv_temp_file = f"{table_name}_temp.csv"
            export_to_csv(connection, table_name, csv_temp_file, query_params, exception_field, exceptions)
            convert_csv_to_xlsx(csv_temp_file, output_file)
            os.remove(csv_temp_file)  # Clean up temporary CSV file
        else:
            print("Something went wrong. Exiting.")
            return

        print(
            f"Data from table/collection '{table_name}' has been successfully exported to {output_file}"
        )
    except ValueError:
        print("Invalid input. Please enter a number.")


if __name__ == "__main__":
    main()

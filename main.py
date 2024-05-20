import csv
import os
import psycopg2
import sqlite3
from pymongo import MongoClient
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


# Function to connect to a MongoDB database
# def connect_mongodb(uri):
#     client = MongoClient(uri)
#     # db = client["default"]
#     return client


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
    elif isinstance(connection, MongoClient):
        collections = connection.list_collection_names()
        table_names = collections
    else:
        raise Exception("Unsupported database type")
    return table_names


# Function to export data from a selected collection/table to a CSV file
def export_to_csv(connection, collection_or_table_name, csv_file):
    cursor = None  # Initialize cursor variable

    if isinstance(connection, psycopg2.extensions.connection):
        query = f"SELECT * FROM public.{collection_or_table_name};"
        cursor = connection.cursor()  # Use the connection's cursor method
        cursor.execute(query)
        rows = cursor.fetchall()
        headers = [desc[0] for desc in cursor.description]

        with open(csv_file, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(headers)
            writer.writerows(rows)

    elif isinstance(connection, sqlite3.Connection):
        query = f"SELECT * FROM {collection_or_table_name};"
        cursor = connection.cursor()  # Use the connection's cursor method
        cursor.execute(query)
        rows = cursor.fetchall()
        headers = [desc[0] for desc in cursor.description]

        with open(csv_file, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(headers)
            writer.writerows(rows)


# TODO: implement support for mongodb
    # elif isinstance(connection, MongoClient):
    #     cursor = connection[collection_or_table_name].find({})
    #     docs = list(cursor)

    #     # Collect all unique keys from the documents
    #     all_fields = set()
    #     for doc in docs:
    #         all_fields.update(doc.keys())
    #     headers = list(all_fields)  # Convert set to list for CSV writing

    #     with open(csv_file, mode="w", newline="", encoding="utf-8") as file:
    #         writer = csv.DictWriter(file, fieldnames=headers)
    #         writer.writeheader()
    #         for doc in docs:
    #             writer.writerow(doc)

    else:
        raise Exception("Unsupported database type")

    if cursor:  # Check if cursor exists before attempting to close
        cursor.close()  # Close the cursor after use
    print(
        f"Data from collection/table '{collection_or_table_name}' has been successfully exported to {csv_file}"
    )


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


def main():
    # Prompt the user for the database URI
    database_uri = input("Enter your database URI: ")

    # Determine the type of database based on the URI
    if "mongodb" in database_uri:
        # connection = connect_mongodb(database_uri)
        return "support for mongodb comiing soon"
    elif "sqlite:" in database_uri:
        connection = connect_sqlite(database_uri)
        
        # postgres support 
    else:
        connection_params = parse_database_uri(database_uri)
        connection = psycopg2.connect(**connection_params)

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
            export_to_csv(connection, table_name, output_file)
        elif file_format == "x":
            csv_temp_file = f"{table_name}_temp.csv"
            export_to_csv(connection, table_name, csv_temp_file)
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

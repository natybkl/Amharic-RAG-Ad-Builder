import os, sys
import json
import pandas as pd
import csv

def convert_json_to_csv(raw_folder, parse_folder):
    # Ensure the CSV folder exists
    if not os.path.exists(parse_folder):
        os.makedirs(parse_folder)

    # Iterate over all files in the JSON folder
    for json_file_name in os.listdir(raw_folder):
        if json_file_name.endswith(".json"):
            json_file_path = os.path.join(raw_folder, json_file_name)

            # Load JSON data
            with open(json_file_path, 'r') as json_file:
                try:
                    data = json.loads(json_file)
                except json.JSONDecodeError:
                    print(f"Error decoding JSON file: {json_file_path}")
                    continue

            # Check if data is a list of dictionaries
            if isinstance(data['message'], list) and data and all(isinstance(item, dict) for item in data):
                # Generate CSV file name
                csv_file_name = os.path.splitext(json_file_name)[0] + ".csv"
                csv_file_path = os.path.join(parse_folder, csv_file_name)

                # Use 'w' mode instead of 'wb'
                with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
                    csv_writer = csv.writer(csv_file)

                    # Write header
                    header = list(data[0].keys())
                    csv_writer.writerow(header)

                    # Write data rows
                    for row in data:
                        csv_writer.writerow(row.values())

                print(f"Conversion successful: {json_file_path} -> {csv_file_path}")
            else:
                print(f"Skipping invalid JSON structure in file: {json_file_path}")


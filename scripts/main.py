# main.py
from process_zip import process_zip, process_zip_files
from clean_data import clean_and_save

# Paths
zip_file_path = "../data/raw/raw.zip"
output_csv_path = "../data/parsed/parsed.csv"
parsed_files_directory = "../data/parsed/"
cleaned_files_directory = "../data/cleaned/"
cleaned_csv_path = "../data/parsed/cleaned_parsed.csv"
cleaned_text_path = "../data/cleaned/cleaned.txt"

# Process the zip file and create a parsed CSV file
process_zip(zip_file_path, output_csv_path)
print("Parsing completed. Output saved to", output_csv_path)

# Clean the parsed data and save to a cleaned CSV and text file
clean_and_save(parsed_csv_path=output_csv_path, 
               cleaned_csv_path=cleaned_csv_path, 
               cleaned_text_path=cleaned_text_path)
print("Cleaning completed. Cleaned files saved to", cleaned_csv_path, "and", cleaned_text_path)

# Process each parsed file in the parsed directory
process_zip_files(zip_file_path, parsed_files_directory)
print("Parsing completed for each file in", zip_file_path)

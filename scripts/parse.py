import os
import pandas as pd
from utils import Util

def parse_all_in_one():
    zip_file_path = "../data/raw/raw.zip"
    output_csv_path = "../data/parsed/parsed.csv"

    util.process_zip(zip_file_path, output_csv_path)
    print("Parsing completed. Output saved to", output_csv_path)

def parse_cleaned_individual_files():
    zip_file_path = "../data/raw/raw.zip"
    output_directory = "../data/parsed/"
    util.process_zip_files(zip_file_path, output_directory)


if __name__ == "__main__":
    util = Util()
    parse_all_in_one()
    parse_cleaned_individual_files()
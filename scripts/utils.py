# util.py

import json
import re
import zipfile
import csv
import pandas as pd

class Util():
    def __init__(self) -> None:
        self.emoji_pattern = re.compile(r"[\U0001F000-\U0001F9FF\U0001FA00-\U0001FFFF\U00020000-\U0002FFFF\U00030000-\U0003FFFF]+", flags=re.UNICODE)
        
        self.symbols = re.compile("["
                                  "\""
                                  "\“"
                                  "\""
                                  "\'"
                                  "\-"
                                  "\*"
                                  "\•"
                                  "\ℹ"
                                  "\﻿"
                                  "\_"
                                  "]+")
        self.url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        self.mention_pattern = r'@(\w+)'

    def read_file(self, file_path: str) -> dict:
        # Open the file for reading
        with open(file_path, 'r') as file:
            # Load the JSON data from the file
            data = json.load(file)
            return data

    def write_file(self, file_path: str, data: dict) -> None:
        # Open the file for writing
        with open(file_path, 'w') as file:
            # Dump the JSON data to the file
            json.dump(data, file, indent=2)

    def parse_text(self, text: any) -> str:
        if isinstance(text, str):
            return text
        elif isinstance(text, list):
            contents = []
            for item in text:
                if isinstance(item, str):
                    contents.append(item)
                elif isinstance(item, dict):
                    contents.append(item['text'])
            return "".join(contents)
        else:
            return ""

    def parse_messages(self, messages: list) -> dict:
        parsed_messages = {
            'id': [],
            'text': [],
            'date': []
        }
        for message in messages:
            if message['type'] != 'message' or len(message['text']) == 0:
                continue
            parsed_messages['id'].append(message['id'])
            message_content = self.parse_text(message['text'])
            parsed_messages['text'].append(message_content)
            parsed_messages['date'].append(message['date'])
        return parsed_messages

    def extract_hashtags(self, text: str) -> list:
        return [word for word in text.split() if word.startswith('#')]

    def extract_emojis(self, text):
        return ''.join(self.emoji_pattern.findall(text))

    def remove_emojis(self, text):
        return self.emoji_pattern.sub('', text)

    def extract_symbols(self, text):
        return ''.join(self.symbols.findall(text))

    def remove_symbols(self, text):
        return self.symbols.sub(' ', text)

    def extract_urls(self, text):
        return re.findall(self.url_pattern, text)

    def extract_mentions(self, text):
        return re.findall(self.mention_pattern, text)
    
    def extract_fields(self, message):
        """
        Extracts relevant fields from the message.
        Returns a tuple containing (channel_id, text, date, labels).
        """
        text = ' '.join(item['text'] for item in message['text_entities'] if item['type'] in 'plain')
        date = message['date']
        labels = "LABEL"  # Replace 'your_label' with the actual label(s) relevant to your use case
        return text, date, labels

    def process_json_file(self, json_file, csv_writer):
        """
        Processes a JSON file, extracts relevant fields, and writes to CSV.
        """
        data = json.load(json_file)

        channel_id = data['id']
        for message in data['messages']:
            text, date, labels = self.extract_fields(message)
            csv_writer.writerow([channel_id, text, date, labels])

    def process_zip(self, zip_file_path, output_csv_path):
        """
        Processes a zip file, extracts data from JSON files, and writes to a CSV file.
        """
        with zipfile.ZipFile(zip_file_path, 'r') as zip_file:
            with open(output_csv_path, 'w', newline='', encoding='utf-8') as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow(['id', 'text', 'date', 'label'])

                for file_info in zip_file.infolist():
                    with zip_file.open(file_info.filename) as json_file:
                        print(json_file)
                        self.process_json_file(json_file, csv_writer)

    def process_zip_files(self, zip_file_path, output_directory):
        with zipfile.ZipFile(zip_file_path, 'r') as zip_file:
            # Iterate through each file in the zip archive
            for file_info in zip_file.infolist():
                with zip_file.open(file_info.filename) as json_file:
                    # Process the JSON file and create a DataFrame
                    data = json.load(json_file)
                    parsed_data = self.parse_json_data(data)

                    # Create a DataFrame from the parsed data
                    df = pd.DataFrame(parsed_data)

                    # Save the DataFrame to a CSV file
                    output_file_name = os.path.splitext(os.path.basename(file_info.filename))[0]
                    output_csv_path = os.path.join(output_directory, f"{output_file_name}_parsed.csv")
                    df.to_csv(output_csv_path, index=False)

    def parse_json_data(self, data):
        # Implement your JSON parsing logic here
        # Modify this method according to how you want to extract data from the JSON
        parsed_data = {
            'id': [],
            'text': [],
            'date': [],
            'label': []
        }

        for message in data['messages']:
            # Extract relevant fields from the message
            text, date, labels = self.extract_fields(message)
            parsed_data['id'].append(data['id'])
            parsed_data['text'].append(text)
            parsed_data['date'].append(date)
            parsed_data['label'].append(labels)
            
        return parsed_data
                        
    def file_reader(self, path: str, ) -> str:
        fname = os.path.join(path)
        with open(fname, 'r') as f:
            system_message = f.read()
        return system_message

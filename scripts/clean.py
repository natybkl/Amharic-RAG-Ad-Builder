import os
import pandas as pd
from utils import Util

def clean(filepath):
    df = pd.read_csv(filepath)

    # Apply method to clean null or empty values in the 'text' column
    df = df.dropna()

    # Remove newlines from the 'text' column
    df['text'] = df['text'].replace('\n', ' ', regex=True)

    # Remove hashtags from the 'text' column
    df['text'] = df['text'].str.replace(r'\#\w+', '', regex=True)

    # Apply method to remove emojis from the 'text' column
    df['text'] = df['text'].apply(util.remove_emojis)

    # Apply method to remove special symbols from the 'text' column
    df['text'] = df['text'].apply(util.remove_symbols)

    # Apply method to remove hyperlinks or URLs from the 'text' column
    df['text'] = df['text'].str.replace(util.url_pattern, '', regex=True).str.strip()
    df['text'] = df['text'].str.replace(util.mention_pattern, '', regex=True).str.strip()

    # Apply method to remove extra spaces, multiple spaces, or leading/trailing spaces from the 'text' column
    df['text'] = df['text'].str.replace('\s+', ' ', regex=True).str.strip()
    df['text'] = df['text'].replace(r'!+', '!', regex=True)
    df['text'] = df['text'].replace(r'\.+', '', regex=True)

    # Clean specific Amharic letters
    letters = [
        [['ሐ', 'ሑ', 'ሒ', 'ሓ', 'ሔ', 'ሖ'], ['ሀ', 'ሁ', 'ሂ', 'ሃ', 'ሄ', 'ህ', 'ሆ']],
        [['ኀ', 'ኁ', 'ኂ', 'ኃ', 'ኄ', 'ኅ', 'ኆ'], ['ሀ', 'ሁ', 'ሂ', 'ሃ', 'ሄ', 'ህ', 'ሆ']],
        [['ሠ', 'ሡ', 'ሢ', 'ሣ', 'ሤ', 'ሦ', 'ሦ', 'ሧ'], ['ሰ', 'ሱ', 'ሲ', 'ሳ', 'ሴ', 'ስ', 'ሶ', 'ሷ']],
        [['ዐ', 'ዑ', 'ዒ', 'ዓ', 'ዔ', 'ዕ', 'ዖ'], ['አ', 'ኡ', 'ኢ', 'ኣ', 'ኤ', 'እ', 'ኦ']],
        [['ጸ', 'ጹ', 'ጺ', 'ጻ', 'ጼ', 'ጽ', 'ጾ'], ['ፀ', 'ፁ', 'ፂ', 'ፃ', 'ፄ', 'ፅ', 'ፆ']]
    ]

    for letter in letters:
        for i in range(len(letter[0])):
            df['text'] = df['text'].str.replace(letter[0][i], letter[1][i])

    # Clean English characters from the 'text' column
    df['text'] = df['text'].str.replace(r'[A-Za-z]+', '', regex=True)


    # Save the cleaned text to a separate text file
    cleaned_text_path = os.path.join(cleaned_files_directory, f"{os.path.splitext(filename)[0]}.txt")
    df['text'].to_csv(cleaned_text_path, index=False, header=False)

def clean_all_in_one(input_path, output_path):
    # Specify the paths
    parsed_csv_path = "../data/parsed/parsed.csv"
    output_cleaned_csv_path = "../data/parsed/cleaned_parsed.csv"

    




if __name__ == "__main__":
    util = Util()
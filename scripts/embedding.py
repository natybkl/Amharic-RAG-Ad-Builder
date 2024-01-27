import pandas as pd
from tqdm import tqdm
from pinecone import Pinecone
from dotenv import load_dotenv
import os
from embeddings import Embedder  # Assuming you have an embeddings module

# Load environment variables from .env
load_dotenv()

# Create a progress bar
progress_bar = tqdm()

# Counter variable
counter = 0

def load(csv_path, column):
    # Get Pinecone instance
    pinecone = Pinecone()

    # Read CSV file into a DataFrame
    df = pd.read_csv(csv_path)

    # Ensure the selected column exists in the CSV file
    if column not in df.columns:
        print(f"Column {column} not found in CSV file")
        exit(1)

    # Extract the selected column from the DataFrame
    documents = df[column].astype(str).tolist()

    # Get index name, cloud, and region
    index_name = os.getenv('PINECONE_INDEX')
    index_cloud = os.getenv('PINECONE_CLOUD')
    index_region = os.getenv('PINECONE_REGION')

    # Create a Pinecone index with a dimension of 384 to hold the outputs
    # of our embeddings model. Use suppress_conflicts in case the index already exists.
    pinecone.create_index(index_name, dimension=384, cloud=index_cloud, region=index_region, wait_until_ready=True, suppress_conflicts=True)

    # Select the target Pinecone index.
    index = pinecone.index(index_name, 'text_metadata')

    # Start the progress bar
    progress_bar.total = len(documents)
    progress_bar.update(0)

    # Start the batch embedding process
    embedder = Embedder()  # Assuming you have an Embedder class
    embedder.init()

    batch_size = 100
    for i in range(0, len(documents), batch_size):
        batch = documents[i:i+batch_size]

        # Batch embedding process
        embeddings = embedder.embed_batch(batch)

        # Whenever the batch embedding process returns a batch of embeddings, insert them into the index
        index.upsert(embeddings)

        # Update counter and progress bar
        counter += len(embeddings)
        progress_bar.update(len(embeddings))

    progress_bar.close()
    print(f"Inserted {len(documents)} documents into index {index_name}")

if __name__ == "__main__":
    csv_path = "your_csv_file.csv"  # Replace with your CSV file path
    target_column = "your_target_column"  # Replace with your target column name
    load(csv_path, target_column)

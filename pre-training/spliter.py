import jsonlines
from sklearn.model_selection import train_test_split

# Specify the input and output file paths
input_file_path = 'cleaned.jsonl'
train_output_path = 'train.jsonl'
eval_output_path = 'eval.jsonl'

# Load the data from the JSONL file
data = []
with jsonlines.open(input_file_path, 'r') as reader:
    for line in reader:
        data.append(line)

# Split the data into training and evaluation sets
train_data, eval_data = train_test_split(data, test_size=0.2, random_state=42)

# Write the training data to the train output file
with jsonlines.open(train_output_path, 'w') as writer:
    for line in train_data:
        writer.write(line)

# Write the evaluation data to the eval output file
with jsonlines.open(eval_output_path, 'w') as writer:
    for line in eval_data:
        writer.write(line)

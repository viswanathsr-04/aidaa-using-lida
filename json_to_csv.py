import json
import csv
import pandas as pd


output_file = 'datafile.csv'
def ldjson_to_csv(input_file):
    # Read the LDJSON file and collect all possible fieldnames
    fieldnames = set()

    with open(input_file, 'r') as ldjson_file:
        data_list = [json.loads(line.strip()) for line in ldjson_file]
        for data in data_list:
            fieldnames.update(data.keys())  # Collect all unique keys

    # Write to CSV
    with open(output_file, 'w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=list(fieldnames))
        writer.writeheader()
        
        for data in data_list:
            writer.writerow(data)  # Will handle missing keys automatically

    print(f"Conversion completed! ldjson-CSV saved as {output_file}")


def json_to_csv(input_file):
    with open(input_file) as file:
        data = json.load(file)

    df = pd.json_normalize(data)

    # Save to CSV
    df.to_csv(output_file, index=False)


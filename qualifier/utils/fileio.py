# -*- coding: utf-8 -*-
"""Helper functions to load and save CSV data.

This contains a helper function for loading and saving CSV files.

"""
import csv


def load_csv(csvpath, bank_data, header=None):
    """Reads the CSV file from path provided.

    Args:
        csvpath (Path): The csv file path.

    Returns:
        A list of lists that contains the rows of data from the CSV file.

    """
    with open(csvpath, "r") as csvfile:
        data = []
        csvreader = csv.reader(csvfile, delimiter=",")

        # Skip the CSV Header
        next(csvreader)

        # Read the CSV data
        for row in csvreader:
            data.append(row)
    return data

def save_csv(csv_path_name, bank_data, header=None):
    with open(csv_path_name, "w", newline='') as csv_file:
        writer = csv.writer(csv_file, '')
        print(f"Creating the Header row")
        for line in bank_data:
            print(f"This is a potential lender: {line}")
            writer.writerow(line)
    return None





import os
import re
import pandas as pd

# Define the ISO 8601 timestamp regex
iso_regex = r"^\s*$|^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\+\d{2}:\d{2}$"

def is_iso8601(timestamp):
    """Check if the timestamp is empty, a space, or valid ISO 8601 format"""
    return bool(re.match(iso_regex, timestamp))

def validate_csv(file_path):
    """Check if the CSV file has correct format"""
    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        return False, f"Error reading CSV file: {e}"

    required_columns = ['t0', 't1']
    if not all(col in df.columns for col in required_columns):
        return False, f"CSV missing required columns: {required_columns}"

    # Validate t0 and t1 columns for correct format
    for index, row in df.iterrows():
        if not is_iso8601(str(row['t0'])) or not is_iso8601(str(row['t1'])):
            return False, f"Invalid t0/t1 timestamp format in file {file_path} at row {index + 1}"

    return True, "Valid CSV file."

def validate_folder(folder_path):
    """Validate all CSV files in a folder"""
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".csv"):
                file_path = os.path.join(root, file)
                valid, message = validate_csv(file_path)
                if not valid:
                    print(f"Validation failed for {file_path}: {message}")
                    return False
                else:
                    print(f"Validation passed for {file_path}")
    return True

if __name__ == "__main__":
    folders = ["flags", "adjustments"]
    all_valid = True
    for folder in folders:
        if not validate_folder(folder):
            all_valid = False
    
    if not all_valid:
        print("CSV validation failed.")
        exit(1)
    else:
        print("All CSV files are valid.")
        exit(0)

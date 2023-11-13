import csv
from dateutil.parser import parse

input_file_path = 'house_listings_w_15var.csv'
output_file_path = 'house_listing_w_15var_noZeroDupe.csv'

def is_valid_row(row, header_row):
    return row != header_row and row['totalPrice'] != '0' and row['usableArea'] != '0' and row['latitude'] != '' and row['totalPrice'] != '' and row['usableArea'] != ''

def row_key(row):
    return tuple(value for key, value in row.items() if key != 'lastUpdated')

def parse_date(date_str):
    try:
        return parse(date_str)
    except ValueError:
        return None

with open(input_file_path, 'r', newline='') as f, open(output_file_path, 'w', newline='') as out_file:
    reader = csv.DictReader(f)
    writer = csv.DictWriter(out_file, fieldnames=reader.fieldnames)
    writer.writeheader()

    header_row = next(reader)
    latest_rows = {}

    for row in reader:
        if is_valid_row(row, header_row):
            row_date = parse_date(row['lastUpdated'])
            if row_date is None:
                continue

            key = row_key(row)
            if key not in latest_rows or parse_date(latest_rows[key]['lastUpdated']) < row_date:
                latest_rows[key] = row

    for row in latest_rows.values():
        writer.writerow(row)

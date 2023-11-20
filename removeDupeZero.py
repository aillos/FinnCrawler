import csv
from dateutil.parser import parse

input_file_path = 'house_listings_w_15var3.csv'
output_file_path = 'house_listing_processed.csv'

def is_valid_row_combined(row):
    try:
        price_condition = float(row['totalPrice'].strip()) >= 150000
        area_condition = float(row['usableArea'].strip()) >= 15
        latitude_condition = row['latitude'].strip() != ''
        property_type_condition = row['propertyType'].strip() != 'Andre'
        no_zero_condition = row['totalPrice'] != '0' and row['usableArea'] != '0'
        return price_condition and area_condition and latitude_condition and property_type_condition and no_zero_condition
    except ValueError:
        return False

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

    latest_rows = {}

    for row in reader:
        if is_valid_row_combined(row):
            row_date = parse_date(row['lastUpdated'])
            if row_date is None:
                continue

            key = row_key(row)
            if key not in latest_rows or parse_date(latest_rows[key]['lastUpdated']) < row_date:
                latest_rows[key] = row

    for row in latest_rows.values():
        writer.writerow(row)

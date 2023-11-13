import csv

input_file_path = 'house_listings_w_15var2.csv'
output_file_path = 'house_listing_w_15var_noZero.csv'

def is_non_zero_and_non_empty(value):
    return value.strip() not in ('', '0')

with open(input_file_path, 'r', newline='') as f, open(output_file_path, 'w', newline='') as out_file:
    reader = csv.DictReader(f)
    writer = csv.DictWriter(out_file, fieldnames=reader.fieldnames)
    writer.writeheader()

    for row in reader:
        if all(is_non_zero_and_non_empty(row[field].strip()) for field in ['totalPrice', 'usableArea', 'latitude']):
            writer.writerow(row)

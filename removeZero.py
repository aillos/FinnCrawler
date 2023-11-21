import csv

input_file_path = 'house_listings.csv'
output_file_path = 'house_listing_clean.csv'


def is_valid_row(row):
    try:
        return (float(row['totalPrice'].strip()) >= 150000 and
                float(row['usableArea'].strip()) >= 15 and
                row['latitude'].strip() != '' and
                row['longitude'].strip() != '' and
                row['latitude'].strip() != 'None' and
                row['longitude'].strip() != 'None' and
                float(row['usableArea'].strip()) <= 1000 and
                row['propertyType'].strip() != 'Andre')
    except ValueError:
        return False


with open(input_file_path, 'r', newline='') as f, open(output_file_path, 'w', newline='') as out_file:
    reader = csv.DictReader(f)
    writer = csv.DictWriter(out_file, fieldnames=reader.fieldnames)
    writer.writeheader()

    for row in reader:
        if is_valid_row(row):
            writer.writerow(row)

import csv

input_file_path = 'house_listings_w_15var4.csv'
output_file_path = 'house_listing_w_15var_notNew.csv'


def is_valid_row(row):
    try:
        return row['new'].strip() != 'True'
    except ValueError:
        return False


with open(input_file_path, 'r', newline='') as f, open(output_file_path, 'w', newline='') as out_file:
    reader = csv.DictReader(f)
    writer = csv.DictWriter(out_file, fieldnames=reader.fieldnames)
    writer.writeheader()

    for row in reader:
        if is_valid_row(row):
            writer.writerow(row)

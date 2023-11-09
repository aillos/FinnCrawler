import csv
from more_itertools import unique_everseen

input_file_path = './FinnCrawler/house_listings.csv'
output_file_path = 'house_listing_nodup_nozero.csv'

with open(input_file_path, 'r', newline='') as f, open(output_file_path, 'w', newline='') as out_file:
    reader = csv.DictReader(f)
    writer = csv.DictWriter(out_file, fieldnames=reader.fieldnames)
    print(reader.fieldnames)
    writer.writeheader()

    unique_rows = unique_everseen(reader, key=lambda row: tuple(row.values()))

    for row in unique_rows:
        if row['totalPrice'] != '0' and row['usableArea'] != '0' and row['latitude'] != '' and row['totalPrice'] != '':
            writer.writerow(row)
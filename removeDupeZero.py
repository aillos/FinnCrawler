import csv

input_file_path = 'house_listings.csv'
output_file_path = 'house_listing_clean.csv'


def is_valid_row(row):
    def safe_float(value, default=0.0):
        try:
            return float(value.strip())
        except ValueError:
            return default

    try:
        totalPrice = float(row['totalPrice'].strip())
        usableArea = float(row['usableArea'].strip())
    except ValueError:

        return False

    bedrooms = safe_float(row['bedrooms'], default=0.0)
    rooms = safe_float(row['rooms'], default=0.0)

    property_type = row['propertyType'].strip()

    return (totalPrice >= 150000 and
            usableArea >= 15 and
            row['latitude'].strip() not in ['', 'None'] and
            row['longitude'].strip() not in ['', 'None'] and
            bedrooms <= 12 and
            rooms <= 20 and
            usableArea <= 1000 and
            property_type != 'BygÃ¥rd/Flermannsbolig' and
            property_type != 'Hytte' and
            property_type != 'GÃ¥rdsbruk/SmÃ¥bruk' and
            property_type != 'Garasje/Parkering' and
            property_type != 'Produksjon/Industri' and
            property_type != 'Tomter' and
            property_type != 'Kombinasjonslokaler' and
            property_type != 'Andre')


unique_rows = set()

with open(input_file_path, 'r', newline='') as f, open(output_file_path, 'w', newline='') as out_file:
    reader = csv.DictReader(f)
    writer = csv.DictWriter(out_file, fieldnames=reader.fieldnames)
    writer.writeheader()

    for row in reader:
        if is_valid_row(row):
            identifier = tuple(row[field].strip() for field in reader.fieldnames)
            if identifier not in unique_rows:
                unique_rows.add(identifier)
                writer.writerow(row)

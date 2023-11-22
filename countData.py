import csv

input_file_path = 'house_listing_clean.csv'
output_file_path = 'house_listing_count.csv'

count_new = {'True': 0, 'False': 0}
count_built = {}
count_bedrooms = {}
count_rooms = {}
count_energy_color = {}
count_energy_label = {}
count_ownership = {}
count_property_type = {}
count_is_sold = {'True': 0, 'False': 0}

with open(input_file_path, 'r', newline='') as f:
    reader = csv.DictReader(f)

    for row in reader:
        if row['new'].strip() in count_new:
            count_new[row['new'].strip()] += 1

        built = row['built'].strip()
        if built:
            count_built[built] = count_built.get(built, 0) + 1

        bedrooms = row['bedrooms'].strip()
        if bedrooms:
            count_bedrooms[bedrooms] = count_bedrooms.get(bedrooms, 0) + 1

        rooms = row['rooms'].strip()
        if rooms:
            count_rooms[rooms] = count_rooms.get(rooms, 0) + 1

        for field in ['energy_color', 'energy_label', 'ownership', 'propertyType', 'isSold']:
            value = row[field].strip()
            if value:
                if field == 'EnergyColor':
                    count_energy_color[value] = count_energy_color.get(value, 0) + 1
                elif field == 'EnergyLabel':
                    count_energy_label[value] = count_energy_label.get(value, 0) + 1
                elif field == 'Ownership':
                    count_ownership[value] = count_ownership.get(value, 0) + 1
                elif field == 'PropertyType':
                    count_property_type[value] = count_property_type.get(value, 0) + 1
                elif field == 'isSold':
                    count_is_sold[value] = count_is_sold.get(value, 0) + 1

with open(output_file_path, 'w', newline='') as out_file:
    writer = csv.DictWriter(out_file, fieldnames=['Field', 'Value', 'Count'])
    writer.writeheader()

    for field, count_dict in [('new', count_new), ('built', count_built), ('bedrooms', count_bedrooms),
                              ('rooms', count_rooms), ('EnergyColor', count_energy_color),
                              ('EnergyLabel', count_energy_label), ('Ownership', count_ownership),
                              ('PropertyType', count_property_type), ('isSold', count_is_sold)]:
        for value, count in count_dict.items():
            writer.writerow({'Field': field, 'Value': value, 'Count': count})

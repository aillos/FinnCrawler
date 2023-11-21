from more_itertools import unique_everseen

with open('FinnCrawler/house_listings2.csv', 'r') as f, open('house_listing_nodup.csv', 'w') as out_file:
    out_file.writelines(unique_everseen(f))

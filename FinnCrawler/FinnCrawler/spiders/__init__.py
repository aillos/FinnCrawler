import scrapy
import json
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

from ..items import HouseListingItem

class FinnSpider(scrapy.Spider):
    name = "finn"
    start_urls = ["https://www.finn.no/realestate/homes/search.html?location=0.22042", "https://www.finn.no/realestate/homes/search.html?location=0.22034", "https://www.finn.no/realestate/homes/search.html?location=0.20015", "https://www.finn.no/realestate/homes/search.html?location=0.20018", "https://www.finn.no/realestate/homes/search.html?location=0.20061", "https://www.finn.no/realestate/homes/search.html?location=0.20012", "https://www.finn.no/realestate/homes/search.html?location=0.22054", "https://www.finn.no/realestate/homes/search.html?location=0.20016", "https://www.finn.no/realestate/homes/search.html?location=0.22038", "https://www.finn.no/realestate/homes/search.html?location=0.22046", "https://www.finn.no/realestate/homes/search.html?location=1.22030.20046&location=1.22030.20045&location=1.22030.20110&location=1.22030.20024&location=1.22030.20042", "https://www.finn.no/realestate/homes/search.html?location=1.22030.20026&location=1.22030.20047&location=1.22030.20058&location=1.22030.20051&location=1.22030.20128&location=1.22030.20114&location=1.22030.20055&location=1.22030.20116&location=1.22030.20021&location=1.22030.20117&location=1.22030.20119&location=1.22030.20113&location=1.22030.20060&location=1.22030.20025&location=1.22030.22103&location=1.22030.20099&location=1.22030.20111&location=1.22030.20121&location=1.22030.20125&location=1.22030.22105", "https://www.finn.no/realestate/homes/search.html?location=1.22030.20100&location=1.22030.20052&location=1.22030.20027&location=1.22030.20122&location=1.22030.20022&location=1.22030.20059&location=1.22030.20057&location=1.22030.20115&location=1.22030.20043&location=1.22030.20054&location=1.22030.20130&location=1.22030.20034&location=1.22030.20112&location=1.22030.22104", "https://www.finn.no/realestate/homes/search.html?location=1.22030.20129&location=1.22030.20035&location=1.22030.20050&location=1.22030.20023&location=1.22030.20120&location=1.22030.20033&location=1.22030.20056&location=1.22030.20039&location=1.22030.20037&location=1.22030.20118&location=1.22030.20041&location=1.22030.20123"]

    custom_settings = {
        'FEED_FORMAT': 'csv',
        'FEED_URI': '../house_listings.csv',
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    def parse(self, response):
        listing_urls = response.css('.sf-search-ad-link.link.link--dark.hover\\:no-underline::attr(href)').getall()
        for listing_url in listing_urls:
            if listing_url:
                #self.logger.info(f"Following URL: {listing_url}")
                yield response.follow(listing_url, self.parse_listing)

        parsed_url = urlparse(response.url)
        current_page = response.meta.get('current_page', 1)
        query_params = parse_qs(parsed_url.query)

        query_params['page'] = [current_page + 1]

        next_page_url = parsed_url._replace(query=urlencode(query_params, doseq=True)).geturl()

        if current_page < 60:
            #self.logger.info(f"Following next page: {next_page_url}")
            yield response.follow(next_page_url, self.parse, meta={'current_page': current_page + 1})

    def parse_listing(self, response):
        json_data = response.xpath('//script[@id="ad-data"]/text()').get()

        if json_data:
            data = json.loads(json_data)

            latitude = data.get("latitude")
            longitude = data.get("longitude")
            postNumber = data.get("postNumber")
            type = data.get("propertyType")
            ownership = data.get("ownership")
            energy_color = data.get("energyColorCode")
            energy_label = data.get("energyLabel")

            units = data.get('units', [])
            total_prices = [unit.get('totalPrice') for unit in units if unit.get('totalPrice')]

            total_sqft = [unit.get('usableArea') for unit in units if unit.get('usableArea')]

            if total_prices:
                average_price = total_prices[0]
                if len(total_prices) > 1:
                    average_price = sum(total_prices) / len(total_prices)
                    average_price = round(average_price)
            else:
                average_price = data.get("totalPrice")

            if total_sqft:
                average_sqft = total_sqft[0]
                if len(total_sqft) > 1:
                    average_sqft = sum(total_sqft) / len(total_sqft)
                    average_sqft = round(average_sqft)
            else:
                average_sqft = data.get("usableArea")

            if average_price == 0:
                self.logger.info(data)

            new_item = HouseListingItem()
            new_item["latitude"] = latitude
            new_item["longitude"] = longitude
            new_item["postNumber"] = postNumber
            new_item["totalPrice"] = average_price
            new_item["usableArea"] = average_sqft
            new_item["propertyType"] = type
            new_item["ownership"] = ownership
            new_item["energyLabel"] = energy_label
            new_item["energyColor"] = energy_color
            yield new_item

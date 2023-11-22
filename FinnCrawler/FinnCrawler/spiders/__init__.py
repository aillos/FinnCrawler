from datetime import datetime
import re

import scrapy
import json
from urllib.parse import urlparse, parse_qs, urlencode

from ..items import HouseListingItem


class FinnSpider(scrapy.Spider):
    name = "finn"
    start_urls = ["https://www.finn.no/realestate/homes/search.html"]
    custom_settings = {
        'FEED_FORMAT': 'csv',
        'FEED_URI': '../house_listings.csv',
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    @staticmethod
    def standardize_date(date_str):

        iso_match = re.match(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}', date_str)
        if iso_match:

            return datetime.fromisoformat(date_str).isoformat()

        else:

            month_mapping = {
                'jan.': '01', 'feb.': '02', 'mar': '03', 'apr.': '04',
                'mai': '05', 'jun': '06', 'jul': '07', 'aug.': '08',
                'sep.': '09', 'okt.': '10', 'nov.': '11', 'des.': '12'
            }

            for nor_month, num_month in month_mapping.items():
                if nor_month in date_str:
                    date_str = date_str.replace(nor_month, num_month)
                    break

            date_obj = datetime.strptime(date_str, '%d. %m %Y %H:%M')
            return date_obj.isoformat()

    def parse(self, response):
        listing_urls = response.css('.sf-search-ad-link.link.link--dark.hover\\:no-underline::attr(href)').getall()
        for listing_url in listing_urls:
            if listing_url:
                yield response.follow(listing_url, self.parse_listing)

        parsed_url = urlparse(response.url)
        current_page = response.meta.get('current_page', 1)
        query_params = parse_qs(parsed_url.query)

        query_params['page'] = [current_page + 1]

        next_page_url = parsed_url._replace(query=urlencode(query_params, doseq=True)).geturl()

        if current_page < 60:
            yield response.follow(next_page_url, self.parse, meta={'current_page': current_page + 1})

    def parse_listing(self, response):
        json_data = response.xpath('//script[@id="ad-data"]/text()').get()

        if json_data:

            data = json.loads(json_data)

            finnkode = int(data.get("finnkode"))
            latitude = float(data.get("latitude"))
            longitude = float(data.get("longitude"))
            postNumber = data.get("postNumber")
            ownership = data.get("ownership")
            energy_label = data.get("energyLabel")
            energy_color = data.get("energyColorCode")
            # create_date = data.get("createdAt")
            lastUpdated = data.get("lastUpdatedAt")
            isSold = bool(data.get("isSold"))
            totalPrice = data.get("totalPrice")
            usableArea = data.get("usableArea")
            propType = data.get("propertyType")
            rooms = data.get("rooms")
            primaryRoom = data.get("primaryRoomArea")
            bedrooms = data.get("bedrooms")
            facilities = data.get("facilities")
            postArea = data.get("postArea")
            localAreaName = data.get("localAreaName")

            description_list = data.get('descriptionList', [])
            built = None
            for item in description_list:
                if item.get('title') == 'Byggeår':
                    built = item.get('text')
                    break

            units = data.get('units', [])

            # IF MULTIPLE UNITS
            if units:
                for unit in units:

                    new_item = HouseListingItem()
                    new_item["finnkode"] = finnkode
                    new_item["latitude"] = latitude
                    new_item["longitude"] = longitude
                    new_item["postNumber"] = postNumber
                    new_item["totalPrice"] = unit.get('totalPrice')
                    new_item["usableArea"] = unit.get('usableArea')
                    new_item["propertyType"] = unit.get('propertyType')
                    new_item["ownership"] = ownership
                    new_item["energy_label"] = energy_label
                    new_item["energy_color"] = energy_color
                    # new_item["createDate"] = create_date
                    new_item["bedrooms"] = unit.get('bedrooms')
                    new_item["lastUpdated"] = self.standardize_date(lastUpdated)
                    new_item["isSold"] = bool(unit.get("isSold"))
                    new_item["primaryRoom"] = unit.get('primaryRoomArea')
                    new_item["rooms"] = unit.get('rooms')
                    new_item["built"] = built
                    new_item["facilities"] = facilities
                    new_item["postArea"] = postArea
                    new_item["localAreaName"] = localAreaName
                    new_item["new"] = bool(True)
                    new_item["monthlyCost"] = None
                    yield new_item

            # IF ONLY ONE UNIT
            else:

                new_item = HouseListingItem()
                new_item["finnkode"] = finnkode
                new_item["latitude"] = latitude
                new_item["longitude"] = longitude
                new_item["postNumber"] = postNumber
                new_item["totalPrice"] = totalPrice
                new_item["usableArea"] = usableArea
                new_item["propertyType"] = propType
                new_item["ownership"] = ownership
                new_item["energy_label"] = energy_label
                new_item["energy_color"] = energy_color
                # new_item["createDate"] = create_date
                new_item["bedrooms"] = bedrooms
                new_item["lastUpdated"] = self.standardize_date(lastUpdated)
                new_item["isSold"] = isSold
                new_item["primaryRoom"] = primaryRoom
                new_item["rooms"] = rooms
                new_item["built"] = built
                new_item["facilities"] = facilities
                new_item["postArea"] = postArea
                new_item["localAreaName"] = localAreaName
                new_item["new"] = bool(True)
                new_item["monthlyCost"] = None
                yield new_item

        # IF NOT NYBYGG
        else:
            full_address = response.xpath(
                '//a[@data-testid="map-link"]/span[@data-testid="object-address"]/text()').get()
            url = response.xpath('//a[@data-testid="map-link"]/@href').get()
            parsed_url = urlparse(url) if url else None
            query_params = parse_qs(parsed_url.query) if parsed_url else {}

            latitude = float(query_params.get("lat", [None])[0]) if query_params.get("lat", [None])[0] else None
            longitude = float(query_params.get("lng", query_params.get("lon", [None]))[0]) if \
                query_params.get("lng", query_params.get("lon", [None]))[0] else None

            if full_address:
                parts = full_address.split(',')

                if len(parts) > 1:
                    post_location = parts[1].strip().split(' ')
                    postCode = post_location[0]
                    postLoc = ' '.join(post_location[1:])
            else:
                postCode = "none"
                postLoc = "none"

            def get_property_detail(response, testid, regex=None):
                selector = response.xpath(f'//div[@data-testid="{testid}"]/dd/text()')
                if selector:
                    text = selector.get().strip()
                    if regex:
                        match = re.search(regex, text)
                        return match.group(1) if match else None
                    return text
                return None

            built_year = get_property_detail(response, "info-construction-year")
            prop_type = get_property_detail(response, "info-property-type")
            bed = get_property_detail(response, "info-bedrooms")
            primary = get_property_detail(response, "info-primary_area", r'(\d+)')
            energy_full_text = get_property_detail(response, "energy-label-info")
            energy = energy_full_text[0] if energy_full_text else None
            energy_last_word = energy_full_text.split()[-1] if energy_full_text else None
            owner = get_property_detail(response, "info-ownership-type")
            area = get_property_detail(response, "info-usable-area", r'(\d+)')
            room = int(get_property_detail(response, "info-rooms")) if get_property_detail(response, "info-rooms") else 0
            facilities = response.xpath('//section[@data-testid="object-facilities"]/div/div/text()').extract()
            facilities = facilities if facilities else None
            total_price_text = get_property_detail(response, "pricing-total-price")
            total_price = int(
                total_price_text.replace(u'\xa0', '').replace(' kr', '').strip()) if total_price_text else None
            monthlyCost_text = get_property_detail(response, "pricing-common-monthly-cost")
            if monthlyCost_text:
                monthlyCost = int(monthlyCost_text.replace(u'\xa0', '').replace(' kr', '').strip())
            else:
                monthlyCost = 0

            new_item = HouseListingItem()
            new_item["finnkode"] = int(
                response.xpath('/html/body/main/section[2]/div[1]/table/tbody/tr[1]/td/text()').get())
            new_item["latitude"] = latitude
            new_item["longitude"] = longitude
            new_item["postNumber"] = int(postCode)
            new_item["totalPrice"] = total_price
            new_item["usableArea"] = area
            new_item["propertyType"] = prop_type
            new_item["ownership"] = owner
            new_item["energy_label"] = energy
            new_item["energy_color"] = energy_last_word
            new_item["bedrooms"] = bed
            new_item["rooms"] = room
            new_item["lastUpdated"] = self.standardize_date(
                response.xpath('/html/body/main/section[2]/div[1]/table/tbody/tr[2]/td/text()').get())
            new_item["isSold"] = bool(True)
            new_item["primaryRoom"] = primary
            new_item["built"] = built_year
            new_item["facilities"] = facilities
            new_item["postArea"] = postLoc
            new_item["localAreaName"] = response.xpath('//div[@data-testid="local-area-name"]/text()').get()
            new_item["new"] = bool(False)
            new_item["monthlyCost"] = monthlyCost
            yield new_item

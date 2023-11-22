from datetime import datetime
import re

import scrapy
import json
from urllib.parse import urlparse, parse_qs, urlencode

from ..items import HouseListingItem


class FinnSpider(scrapy.Spider):
    name = "finn"
    start_urls = [
        "https://www.finn.no/realestate/homes/search.html?location=1.22042.20166&location=1.22042.20172&location=1.22042.20178&location=1.22042.20176&location=1.22042.20175&location=1.22042.20181&location=1.22042.20182&location=1.22042.20170&location=1.22042.20167&location=1.22042.20191&location=1.22042.20165&location=1.22042.20174&location=1.22042.20179&location=1.22042.20192",
        "https://www.finn.no/realestate/homes/search.html?location=1.22042.20189&location=1.22042.20171&location=1.22042.20190&location=1.22042.20164&location=1.22042.20193&location=1.22042.20169&location=1.22042.20168&location=1.22042.20177&location=1.22042.20183&location=1.22042.20173&location=1.22042.20187",
        "https://www.finn.no/realestate/homes/search.html?location=1.22034.20081&location=1.22034.20086&location=1.22034.20069&location=1.22034.20073&location=1.22034.20078&location=1.22034.20105&location=1.22034.20082&location=1.22034.20096&location=1.22034.20085&location=1.22034.20101&location=1.22034.20070&location=1.22034.20063&location=1.22034.20062&location=1.22034.20087&location=1.22034.20084&location=1.22034.20089",
        "https://www.finn.no/realestate/homes/search.html?location=1.22034.20106&location=1.22034.20065&location=1.22034.20091&location=1.22034.20067&location=1.22034.20083&location=1.22034.20103&location=1.22034.20077&location=1.22034.20094&location=1.22034.20064&location=1.22034.20092&location=1.22034.20088&location=1.22034.20066&location=1.22034.20076&location=1.22034.20102&location=1.22034.20104&location=1.22034.20093&location=1.22034.20068&location=1.22034.20079&location=1.22034.20074&location=1.22034.20080&location=1.22034.20109&location=1.22034.20108&location=1.22034.20095&location=1.22034.20097&location=1.22034.20071&location=1.22034.20075&location=1.22034.20072&location=1.22034.20090&location=1.22034.20098&location=1.22034.20107",
        "https://www.finn.no/realestate/homes/search.html?location=1.20015.20304&location=1.20015.20314&location=1.20015.20307&location=1.20015.20297&location=1.20015.22101&location=1.20015.20309&location=1.20015.20287&location=1.20015.20285&location=1.20015.22102&location=1.20015.20281&location=1.20015.20280&location=1.20015.20300&location=1.20015.20317&location=1.20015.20284&location=1.20015.20292&location=1.20015.20296&location=1.20015.20311&location=1.20015.20312&location=1.20015.20294&location=1.20015.20310&location=1.20015.20286&location=1.20015.20283",
        "https://www.finn.no/realestate/homes/search.html?location=1.20015.20289&location=1.20015.20282&location=1.20015.20288&location=1.20015.20299",
        "https://www.finn.no/realestate/homes/search.html?location=0.20018",
        "https://www.finn.no/realestate/homes/search.html?location=1.20061.20528&location=1.20061.20507&location=1.20061.20519&location=1.20061.20515&location=1.20061.20524&location=1.20061.20512&location=1.20061.20529",
        "https://www.finn.no/realestate/homes/search.html?location=1.20061.20527&location=1.20061.20511&location=1.20061.20523&location=1.20061.20522&location=1.20061.20518&location=1.20061.20520&location=1.20061.20514&location=1.20061.20516&location=1.20061.20526&location=1.20061.20532&location=1.20061.20510",
        "https://www.finn.no/realestate/homes/search.html?location=1.20061.20530&location=1.20061.20509&location=1.20061.20525&location=1.20061.20517&location=1.20061.20533&location=1.20061.20508&location=1.20061.20531&location=1.20061.20521",
        "https://www.finn.no/realestate/homes/search.html?location=1.20012.20200&location=1.20012.20215&location=1.20012.20194&location=1.20012.20204&location=1.20012.20197&location=1.20012.20209&location=1.20012.20201&location=1.20012.20217&location=1.20012.20202&location=1.20012.20214&location=1.20012.20199&location=1.20012.20206",
        "https://www.finn.no/realestate/homes/search.html?location=1.20012.20195&location=1.20012.20211&location=1.20012.20198&location=1.20012.20205&location=1.20012.20196&location=1.20012.20219&location=1.20012.20218&location=1.20012.20216&location=1.20012.20203&location=1.20012.20210&location=1.20012.20208",
        "https://www.finn.no/realestate/homes/search.html?location=1.22054.20413",
        "https://www.finn.no/realestate/homes/search.html?location=1.22054.20398&location=1.22054.20438&location=1.22054.20437&location=1.22054.20452&location=1.22054.20423&location=1.22054.20455&location=1.22054.20432&location=1.22054.20434&location=1.22054.22115&location=1.22054.20421&location=1.22054.20447&location=1.22054.20435&location=1.22054.20446&location=1.22054.20445&location=1.22054.20453&location=1.22054.20422&location=1.22054.20431&location=1.22054.20442&location=1.22054.20449&location=1.22054.20433&location=1.22054.20436&location=1.22054.20440&location=1.22054.20414&location=1.22054.20430&location=1.22054.20448&location=1.22054.20417&location=1.22054.20443&location=1.22054.20412&location=1.22054.20439&location=1.22054.20418&location=1.22054.20450&location=1.22054.20424&location=1.22054.20454&location=1.22054.20451&location=1.22054.20420&location=1.22054.20441&location=1.22054.20429",
        "https://www.finn.no/realestate/homes/search.html?location=1.20016.20363&location=1.20016.20347&location=1.20016.20322&location=1.20016.20359&location=1.20016.22112&location=1.20016.20321&location=1.20016.20335&location=1.20016.20360&location=1.20016.20354&location=1.20016.20325&location=1.20016.20366&location=1.20016.20349&location=1.20016.20356&location=1.20016.20340&location=1.20016.20337&location=1.20016.20345&location=1.20016.20336&location=1.20016.20344&location=1.20016.20358&location=1.20016.20330&location=1.20016.22114&location=1.20016.22113&location=1.20016.20329&location=1.20016.20361&location=1.20016.20331&location=1.20016.20313&location=1.20016.20334&location=1.20016.20357",
        "https://www.finn.no/realestate/homes/search.html?location=1.20016.20357&location=1.20016.20341&location=1.20016.20338&location=1.20016.20355&location=1.20016.20343&location=1.20016.20346&location=1.20016.20342&location=1.20016.20350&location=1.20016.20327&location=1.20016.20323",
        "https://www.finn.no/realestate/homes/search.html?location=2.20016.20318.20504",
        "https://www.finn.no/realestate/homes/search.html?location=2.20016.20318.20501&location=2.20016.20318.20502&location=2.20016.20318.20505&location=2.20016.20318.20731",
        "https://www.finn.no/realestate/homes/search.html?location=1.22038.20150&location=1.22038.20152&location=1.22038.20161&location=1.22038.20143&location=1.22038.20157&location=1.22038.20132&location=1.22038.20131&location=1.22038.20151&location=1.22038.20159&location=1.22038.20135",
        "https://www.finn.no/realestate/homes/search.html?location=1.22038.20160&location=1.22038.22106&location=1.22038.20153&location=1.22038.20148&location=1.22038.20146&location=1.22038.20134&location=1.22038.20158&location=1.22038.20149&location=1.22038.20147&location=1.22038.20156&location=1.22038.20162&location=1.22038.20133&location=1.22038.20163",
        "https://www.finn.no/realestate/homes/search.html?location=1.22046.22109&location=1.22046.20267&location=1.22046.20243&location=1.22046.20240&location=1.22046.20251&location=1.22046.22108&location=1.22046.20273&location=1.22046.20224&location=1.22046.20221&location=1.22046.20252&location=1.22046.20226&location=1.22046.20268&location=1.22046.20278&location=1.22046.20255",
        "https://www.finn.no/realestate/homes/search.html?location=1.22046.20220",
        "https://www.finn.no/realestate/homes/search.html?location=1.22046.20257&location=1.22046.20258&location=1.22046.22107&location=1.22046.20236&location=1.22046.20228&location=1.22046.20266&location=1.22046.20264&location=1.22046.20245&location=1.22046.20246&location=1.22046.20238&location=1.22046.20262&location=1.22046.20256&location=1.22046.22111&location=1.22046.20225&location=1.22046.20279&location=1.22046.22110&location=1.22046.20223&location=1.22046.20227&location=1.22046.20231&location=1.22046.20233&location=1.22046.20244&location=1.22046.20248&location=1.22046.20265&location=1.22046.20235&location=1.22046.20259",
        "https://www.finn.no/realestate/homes/search.html?location=1.22030.20024&location=1.22030.20114&location=1.22030.20128&location=1.22030.20051&location=1.22030.20058&location=1.22030.20047&location=1.22030.20026",
        "https://www.finn.no/realestate/homes/search.html?location=1.22030.20046&location=1.22030.20045",
        "https://www.finn.no/realestate/homes/search.html?location=1.22030.20110&location=1.22030.20042&location=1.22030.20055&location=1.22030.20116&location=1.22030.20021",
        "https://www.finn.no/realestate/homes/search.html?location=1.22030.20117&location=1.22030.20119&location=1.22030.20113&location=1.22030.20060&location=1.22030.20025&location=1.22030.22103&location=1.22030.20099&location=1.22030.20111&location=1.22030.20121&location=1.22030.20125",
        "https://www.finn.no/realestate/homes/search.html?location=1.22030.22105&location=1.22030.20100",
        "https://www.finn.no/realestate/homes/search.html?location=1.22030.20052&location=1.22030.20122&location=1.22030.20027&location=1.22030.20022",
        "https://www.finn.no/realestate/homes/search.html?location=1.22030.20059&location=1.22030.20057&location=1.22030.20115&location=1.22030.20043&location=1.22030.20054&location=1.22030.22104",
        "https://www.finn.no/realestate/homes/search.html?location=1.22030.20130&location=1.22030.20034&location=1.22030.20112&location=1.22030.20129&location=1.22030.20035&location=1.22030.20050&location=1.22030.20023",
        "https://www.finn.no/realestate/homes/search.html?location=1.22030.20120&location=1.22030.20033&location=1.22030.20056&location=1.22030.20039&location=1.22030.20037&location=1.22030.20118&location=1.22030.20041&location=1.22030.20123"]

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

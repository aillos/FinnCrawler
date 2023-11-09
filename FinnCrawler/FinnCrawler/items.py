import scrapy

class HouseListingItem(scrapy.Item):
    latitude = scrapy.Field()
    longitude = scrapy.Field()
    postNumber = scrapy.Field()
    totalPrice = scrapy.Field()
    usableArea = scrapy.Field()
    propertyType = scrapy.Field()
    ownership = scrapy.Field()
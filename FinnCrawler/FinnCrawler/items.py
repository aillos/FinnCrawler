import scrapy


class HouseListingItem(scrapy.Item):
    latitude = scrapy.Field()
    longitude = scrapy.Field()
    postNumber = scrapy.Field()
    totalPrice = scrapy.Field()
    usableArea = scrapy.Field()
    propertyType = scrapy.Field()
    ownership = scrapy.Field()
    energyLabel = scrapy.Field()
    energyColor = scrapy.Field()
    createDate = scrapy.Field()
    bedrooms = scrapy.Field()
    lastUpdated = scrapy.Field()
    isSold = scrapy.Field()
    rooms = scrapy.Field()
    primaryRoom = scrapy.Field()
    finnkode = scrapy.Field()
    built = scrapy.Field()
    facilities = scrapy.Field()
    localAreaName = scrapy.Field()
    postArea = scrapy.Field()
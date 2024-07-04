import scrapy


class Apartment(scrapy.Item):
    property_name = scrapy.Field()
    property_id = scrapy.Field()
    breadcrumbs = scrapy.Field()
    price = scrapy.Field()
    image_url = scrapy.Field()
    description = scrapy.Field()
    seller_name = scrapy.Field()
    location = scrapy.Field()
    property_type = scrapy.Field()
    bathrooms = scrapy.Field()
    bedrooms = scrapy.Field()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

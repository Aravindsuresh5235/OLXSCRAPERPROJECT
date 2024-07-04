import scrapy
from .dataclass import Apartment

class OlxScrapy(scrapy.Spider):
    name = "olx"

    def start_requests(self):
        url = 'https://www.olx.in/kozhikode_g4058877/for-rent-houses-apartments_c1723'
        yield scrapy.Request(url=url, callback=self.parse_listing_page)

    def parse_listing_page(self, response):
        url_prefix = "https://www.olx.in"
        
        # Extract listing URLs and make requests to each listing page
        for listing in response.xpath("//li[@class='_1DNjI']"):
            listing_url = url_prefix + listing.css('a::attr(href)').get()
            yield scrapy.Request(url=listing_url, callback=self.parse_listing)

        # Follow the pagination link to the next page
        next_page_url = response.css('link[rel="next"]::attr(href)').get()
        if next_page_url:
            yield response.follow(next_page_url, callback=self.parse_listing_page)

    def parse_listing(self, response):
        apartment = Apartment()
        apartment['property_name'] = response.xpath("//span[@class='dBLgK']/text()").get()
        apartment['property_id'] = response.xpath("//div[@class='_1-oS0']//strong/text()").getall()[2]
        apartment['breadcrumbs'] = response.xpath("//ol[@class='rui-2Pidb']/li/a[@class='_26_tZ']/text()").getall()
        apartment['price'] = response.xpath("//span[@class='T8y-z']/text()").get()
        apartment['image_url'] = response.xpath("//img[@class='_1Iq92']/@src").get()
        apartment['description'] = ' '.join(response.xpath("//div[@data-aut-id='itemDescriptionContent']/p/text()").getall())
        apartment['location'] = ''.join(response.xpath("//div[@class='rui-99hme gp-Oc']/div[@class='rui-oN78c']/div[@class='_3Uj8e']/span[@class='_1RkZP']/text()").getall())
        apartment['property_type'] = response.xpath("//span[@data-aut-id='value_type']/text()").get()
        apartment['bathrooms'] = response.xpath("//span[@data-aut-id='value_bathrooms']/text()").get()
        apartment['bedrooms'] = response.xpath("//span[@data-aut-id='value_bathrooms']/text()").get()

        yield apartment
import scrapy 

class BookCoversSpider(scrapy.Spider):
    name = 'covers'
    start_urls = ['http://books.toscrape.com/']

    def parse(self, response):
        
        images= list()
        
        for img in response.css('.thumbnail::attr(src)').getall():
            images.append(response.urljoin(img))

        yield {
            'image_urls': images
        }
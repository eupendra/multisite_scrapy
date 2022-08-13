import scrapy
class BooksSpider(scrapy.Spider):
    name = 'books'
    allowed_domains = ['books.toscrape.com','www.gutenberg.org']

    def start_requests(self):
        books_url = 'https://books.toscrape.com/catalogue/page-{}.html'
        for i in range(1, 51):
            yield scrapy.Request(books_url.format(i))

    def parse(self, response):
        for s in response.xpath('//article'):
            item = {
                'price': s.xpath('.//p[@class="price_color"]/text()').get(),
                'title': s.xpath('.//h3/a/@title').get()
            }
            url = 'https://www.gutenberg.org/ebooks/search/?query={}&submit_search=Go%21'
            url = url.format(item['title'])
            yield scrapy.Request(url,
                                 callback=self.parse_gutenberg,
                                 cb_kwargs={
                                     'item':item
                                 })

    def parse_gutenberg(self, response, item):
        result = response.xpath('//span[contains(text(),"Displaying results")]/text()').get()
        has_ebook= False
        if result:
            has_ebook = True
        item['Has eBook'] = has_ebook
        yield item

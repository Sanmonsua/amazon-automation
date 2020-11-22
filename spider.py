import scrapy
import time


class AmazonSpider(scrapy.Spider):
    name = 'amazon'
    base_url = 'https://www.amazon.com/'

    def start_requests(self):
        search_input = input('What are you looking for today? ')
        search = '+'.join(search_input.split(' '))
        url = f'{self.base_url}s?k={search}'
        yield scrapy.Request(url=url, callback=self.parse, meta={ 'search' : search }, headers={ 'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36'})

    def parse(self, response):
        print(response.body)
        search = response.meta['search']
        pages_num = response.xpath('//ul[@class="a-pagination"]/li[last()-1]/text()').get()
        pages_urls = [ f'{self.base_url}s?k={search}&page={p}' for p in range(1, int(pages_num)+1)]
        for page in pages_urls:
            time.sleep(1)
            yield scrapy.Request(url=page, callback=self.parse_search, headers={ 'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36'})
        

    def parse_search(self, response):
        for search_result in response.xpath('//div[@data-component-type="s-search-result"]//h2/a/span/text()').getall():
            yield { 'title' : search_result }


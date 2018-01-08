import scrapy


class CollinsSpider(scrapy.Spider):
    name = "collins"

    custom_settings = {
        "DOWNLOAD_DELAY": 3,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 3,
        "HTTPCACHE_ENABLED": True
    }

    start_urls = ["https://www.collins.senate.gov/newsroom?page={}".format(i) for i in range(0, 152)]

    def parse(self, response):
        for href in response.xpath(
                '//*[contains(@class, "node-title")]/a/@href'
        ).extract():
            # For each festival link, call 'parse_festival' (defined later)
            yield scrapy.Request(
                url="https://collins.senate.gov" + href,
                callback=self.parse_collins,
                meta={'url': href}
            )

        next_url = response.xpath(
            '//*[contains(@class, "pager-next")]/a/@href'
        ).extract()

        yield scrapy.Request(
            url=next_url,
            callback=self.parse
        )

    def parse_collins(self, response):
        try:
            title = response.xpath('//h1/text()').extract()[-1]
        except:
            title = ''

        try:
            date = response.xpath('//div[@class="submitted"]/span/text()').extract()
        except:
            date = ''

        try:
            arr = response.xpath('//div[@class="field-items"]//p/text()').extract()
            arr = [i for i in arr if i != "\xa0"]
            release = " ".join(arr)
        except:
            release = ''

        yield {
            'title': title,
            'date': date,
            'release': release}
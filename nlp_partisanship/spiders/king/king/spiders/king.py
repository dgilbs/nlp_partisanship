import scrapy


class KingSpider(scrapy.Spider):
    name = "king"

    custom_settings = {
        "DOWNLOAD_DELAY": 5,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 3,
        "HTTPCACHE_ENABLED": True
    }

    start_urls = ["https://www.king.senate.gov/newsroom/press-releases?PageNum_rs={}&".format(i) for i in range(1, 107)]

    def parse(self, response):
        for href in response.xpath(
                '//*[contains(@class, "table")]//td/a/@href'
        ).extract():
            # For each festival link, call 'parse_festival' (defined later)
            yield scrapy.Request(
                url=href.strip(),
                callback=self.parse_king,
                meta={'url': href}
            )

        next_url = response.xpath(
            '//*[contains(@class, "next")]/a/@href'
        ).extract()[0]

        yield scrapy.Request(
            url="https://king.senate.gov" + next_url,
            callback=self.parse
        )

    def parse_king(self, response):
        try:
            title = response.xpath('*//h1/text()').extract()[0]
        except:
            title = ''

        try:
            date = response.xpath('//*[@class="dateline"]/text()').extract()
        except:
            date = ''

        try:
            arr = response.xpath('//*[@class="span11"]//p/text()').extract()
            release = " ".join(arr)
        except:
            release = ''

        yield {
            'title': title,
            'date': date,
            'release': release}
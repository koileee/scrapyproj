import scrapy
from ..items import HousingItem

class HousingSpider(scrapy.Spider):
    name = 'housing'
    # custom_settings = {
    #     'REDIRECT_ENABLED': False
    # }
    start_urls = ['https://shanghai.anjuke.com/sale/']

    def parse(self, response):
        # 验证码处理部分
        # next page link
        next_url = response.xpath(
            '//*[@id="content"]/div[4]/div[7]/a[7]/@href').extract()[0]
        print('*********' + str(next_url) + '**********')
        if next_url:
            yield scrapy.Request(url=next_url,
                                 callback=self.parse)

        # 爬取每一页的所有房屋链接
        num = len(response.xpath(
            '//*[@id="houselist-mod-new"]/li').extract())
        num = num/2
        for i in range(1, num):
            url = response.xpath(
                '//*[@id="houselist-mod-new"]/li[{}]/div[2]/div[1]/a/@href'
                    .format(i)).extract()[0]
            yield scrapy.Request(url, callback=self.parse_detail)
    def parse_detail(self, response):
        houseinfo = response.xpath('//*[@class="houseInfo-wrap"]')
        if houseinfo:
            l = ItemLoader(HousingItem(), houseinfo)

            l.add_xpath('mode', '//div/ul/li[10]/div[2]/text()')
            l.add_xpath('area', '//div/ul/li[5]/div[2]/text()')
            l.add_xpath('floor', '//div/ul/li[11]/div[2]/text()')
            l.add_xpath('age', '//div/ul/li[7]/div[2]/text()')
            l.add_xpath('price', '//div/ul/li[3]/div[2]/text()')
            l.add_xpath('location', '//div/ul/li[4]/div[2]/p/text()')
            l.add_xpath('district', '//div/ul/li[4]/div[2]/p/a[1]/text()')

            yield l.load_item()

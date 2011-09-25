import re

from scrapy import log
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.http import Request
from imdb.items import ImdbItem

class ImdbSpider(CrawlSpider):
    name = 'imdb_toplist'
    allowed_domains = ['imdb.com']
    start_urls = ['http://www.imdb.com/chart/top']

    rules = (
        Rule(SgmlLinkExtractor(allow=r'/chart/[\d]+s$'), callback='parse_toplist_page', follow=True),
    )

    def parse_toplist_page(self, response):
        hxs = HtmlXPathSelector(response)

        log.msg(hxs.select('//title/text()').extract().pop(0), level=log.INFO)

        # items = []

        rows = hxs.select('//div[@id="main"]/table[1]/tr')

        for row in rows[1:]:
            cols = row.select('.//td')

            if len(cols) is 0: break;

            # lets go deeper and get the rest of the movie data
            url = cols[2].select('.//a/@href').extract().pop(0)
            if url[0:4] != 'http':
                url = 'http://www.imdb.com'+url
            yield Request(url, callback=self.parse_movie_page)

            # for (counter, col) in enumerate(cols):
            #     if counter == 1:
            #         rating = cols[1].select('.//text()').extract().pop(0)
            #         item['rating'] = float(rating) if rating else 0.0
            #     elif counter == 2:
            #         title_td = cols[2].select('.//text()').extract()
            #         url = cols[2].select('.//a/@href').extract().pop(0)
            #         if url[0:4] != 'http':
            #             url = 'http://www.imdb.com'+url
            #         id = re.search('(\d+)', url).group()
            #         year = re.search('(\d+)', title_td[1]).group()
            #         item['url'] = url
            #         item['id'] = int(id) if id else 0
            #         item['title'] = title_td.pop(0)
            #         item['year'] = int(year) if year else 0
            #     elif counter == 3:
            #         votes = cols[3].select('.//text()').extract().pop(0).replace(',', '').strip()
            #         item['votes'] = int(votes) if votes else 0

            # items.append(item)
            # log.msg(item, level=log.INFO)

        # return items

    def parse_movie_page(self, response):
        hxs = HtmlXPathSelector(response)

        title_h1 = hxs.select('//h1[@class="header"]')
        year = title_h1.select('span/a/text()').extract().pop(0)

        ratings = hxs.select('//div[@class="star-box-details"]')

        i = ImdbItem()

        url = response.url
        if url[0:4] != 'http':
            url = 'http://www.imdb.com'+url

        id = re.search('(\d+)', url).group()
        i['id'] = int(id) if id else 0

        i['url'] = url
        i['title'] = title_h1.select('text()').re('.*[^<]').pop(1)

        original_title = title_h1.select('span[@class="title-extra"]/text()').extract()
        i['original_title'] = original_title.pop(0) if original_title else ''

        i['year'] = int(year)

        description = hxs.select('//p[@itemprop="description"]/text()').extract()
        i['description'] = description.pop(0).strip() if description else ''

        # i['image_small'] = None

        image_large = hxs.select('//td[@id="img_primary"]/a/img/@src').extract()
        # i['image_large'] = image_large.pop(0) if image_large else None

        rating = ratings.select('.//span[@itemprop="ratingValue"]/text()').extract().pop(0).strip()
        i['rating'] = float(rating) if ratings else 0.00

        votes = ratings.select('.//span[@itemprop="ratingCount"]/text()').extract().pop(0).replace(',', '').strip()
        i['votes'] = int(votes) if votes else 0

        # for ImagePipeline
        i['image_urls'] = image_large if image_large else []

        return i

import re

from scrapy import log
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
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
        
        items = []
        
        rows = hxs.select('//div[@id="main"]/table[1]/tr')
        
        for row in rows[1:]:
            cols = row.select('.//td')
            
            if len(cols) is 0: break;
            
            item = ImdbItem()
            
            for (counter, col) in enumerate(cols):
                if counter == 1:
                    rating = cols[1].select('.//text()').extract().pop(0)
                    item['rating'] = float(rating) if rating else 0.0
                elif counter == 2:
                    title_td = cols[2].select('.//text()').extract()
                    url = cols[2].select('.//a/@href').extract().pop(0)
                    if url[0:4] != 'http':
                        url = 'http://www.imdb.com'+url
                    id = re.search('(\d+)', url).group()
                    year = re.search('(\d+)', title_td[1]).group()
                    item['url'] = url
                    item['id'] = int(id) if id else 0
                    item['title'] = title_td.pop(0)
                    item['year'] = int(year) if year else 0
                elif counter == 3:
                    votes = cols[3].select('.//text()').extract().pop(0).replace(',', '').strip()
                    item['votes'] = int(votes) if votes else 0
                    
            items.append(item)
            log.msg(item, level=log.INFO)
        
        return items

    def parse_item(self, response):
        hxs = HtmlXPathSelector(response)
        
        title_h1 = hxs.select('//h1[@class="header"]')
        year = title_h1.select('span/a/text()').extract()
        original_title = title_h1.select('span[@class="title-extra"]/text()').extract()
        
        i = ImdbItem()
        
        i['url'] = response.url
        i['title'] = title_h1.select('text()').re('.*[^<]')
        i['original_title'] = original_title
        i['year'] = year
        i['description'] = hxs.select('//p[@itemprop="description"]/text()').extract()
        i['image_small'] = ''
        i['image_large'] = hxs.select('//td[id="img_primary"]/a/img/@src').extract()
        i['rank'] = 0
        i['rating'] = 0.00
        i['votes'] = 0
        
        return i

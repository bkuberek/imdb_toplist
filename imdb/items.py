# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class ImdbItem(Item):
    '''IMDB Movie Item'''

    id = Field()
    url = Field()
    title = Field()
    original_title = Field()
    year = Field()
    description = Field()
    length = Field()
    director = Field()
    image_small = Field()
    image_large = Field()
    rating = Field()
    votes = Field()

    # need this in order to enable the ImagePipelin
    # this won't be persisted
    image_urls = Field()
    images = Field()

# Scrapy settings for imdb project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

import os

cwd = os.getcwd()

BOT_NAME = 'imdb'
BOT_VERSION = '1.0'

SPIDER_MODULES = ['imdb.spiders']
NEWSPIDER_MODULE = 'imdb.spiders'
DEFAULT_ITEM_CLASS = 'imdb.items.ImdbItem'

IMAGES_STORE = cwd + '/../web/uploads/movie'
IMAGES_EXPIRES = 180 # 180 days
IMAGES_THUMBS = {
    'small': (50, 50),
    'large': (250, 250)
}

ITEM_PIPELINES = [
    'scrapy.contrib.pipeline.images.ImagesPipeline',
    'imdb.pipelines.ImdbPipeline'
#    'myproject.pipeline.JsonWriterPipeline',
]
USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)


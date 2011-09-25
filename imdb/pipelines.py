# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html

import pymysql

from scrapy import log
from scrapy.exceptions import DropItem

class ImdbPipeline(object):
    '''This pipeline object will do some basic validation on an ImdbItem object and persist it to a MySQL database.'''

    def __init__(self):
        '''Initialize database connection'''
        self.connection = pymysql.connect(host='localhost', port=3306, user='imdb', passwd='imdb123', db='imdb_toplist')

    def process_item(self, item, spider):
        '''Process movie item. Expects item to be an ImbdItem object'''

        cursor = self.connection.cursor()

        keys = item.keys()

        item['image_large'] = item['images'][0]['path'][5:] if item['images'][0] else ''


        if 'id' not in keys:
            raise DropItem("Missing id field")

        if cursor.execute('SELECT `id` FROM `movie` WHERE `id` = %d' % item['id']):
            log.msg('Updating movie %d' % item['id'], level=log.INFO)
            sql = 'UPDATE `movie` SET'
            i = 0
            for (key, value) in item.items():
                if key in ('images','image_urls'): continue
                sql += ', ' if i > 0 else ' '
                sql += '`%s` = %s' % (key, self.connection.escape(value))
                i += 1
            sql += ' WHERE id = %d' % item['id']
        else:
            log.msg('Inserting movie %d' % item['id'], level=log.INFO)
            sql = 'INSERT INTO `movie`'
            sql += ' (%s) VALUES (' % (', ').join(keys)
            i = 0
            for key in keys:
                if key in ('images','image_urls'): continue
                sql += ', ' if i > 0 else ' '
                sql += '%s' % self.connection.escape(item[key])
                i += 1
            sql += ')'

        cursor.execute(sql)

        cursor.close()

        return item

    def __del__(self):
        '''Not sure if this is called. May have to open and close connection on process_item()'''
        self.connection.close()

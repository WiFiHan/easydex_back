# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from dexmanager.models import SrcDex
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
import logging as log

class IndexPipeline:
    def process_item(self, item, spider):
        # print("pipeline entered.")
        caller_spider = spider.name
        if caller_spider == 'indicesinfo':
            try:
                index, created = SrcDex.objects.get_or_create(title=item['title'])
                if created:
                    index.title = item['title']
                    index.url = item['url']
                    index.category = item['category']
                index.closing = item['closing']
                index.updated_at = timezone.now()
                index.save()
            except Exception as e:
                print("Error saving index info:", e)
                
        else:
            try:
                index = SrcDex.objects.get(title=item['title'])
            except Exception as e:
                print("Error getting index info:", e)
            try:
                index.values = item['values']
                index.description = item['description']
                index.updated_at = timezone.now()
                index.save()
            except Exception as e:
                print("Error saving index values:", e)

        return item
    
    def open_spider(self, spider):
        log.info("Opening Spider: {}".format(spider.name))
        
        
    def close_spider(self, spider):
        log.info("Closing Spider: {}".format(spider.name))
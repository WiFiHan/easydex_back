# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from dexmanager.models import SrcDex, HankyungTitle
from django.utils import timezone
import logging as log

class IndexPipeline:
    def process_item(self, item, spider):
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
                # index.search_keyword = item['keywords']
                index.save()
            except Exception as e:
                print("Error saving index info:", e)
                
        elif caller_spider == 'indexhistory':
            try:
                index = SrcDex.objects.get(title=item['title'])
            except Exception as e:
                print("title:", item['title'])
                print("Error getting index info:", e)
            try:
                index.values = item['values']
                index.description = item['description']
                index.updated_at = timezone.now()
                index.save()
            except Exception as e:
                print("Error saving index values:", e)
        else:
            try:
                article, created = HankyungTitle.objects.get_or_create(title=item['title'])
                if created:
                    article.title = item['title']
                article.page = item['page']
                article.updated_at = timezone.now()
                article.save()
            except Exception as e:
                print("Error saving article info:", e)

        return item
    
    def open_spider(self, spider):
        log.info("Opening Spider: {}".format(spider.name))
        
        
    def close_spider(self, spider):
        log.info("Closing Spider: {}".format(spider.name))
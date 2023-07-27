# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from dexmanager.models import SrcDex, HankyungTitle
from django.utils import timezone
import logging as log
from .func import remove_brackets_and_append
from .func import generate_keywords, generate_description, reduce_title

class IndexPipeline:
    def process_item(self, item, spider):
        caller_spider = spider.name
        if caller_spider == 'indicesinfo':
            try:
                index, created = SrcDex.objects.get_or_create(title=item['title'])
                if not index.title:
                    index.title = item['title']
                if not index.url:
                    index.url = item['url']
                if not index.category:
                    index.category = item['category']
                index.closing = item['closing']
                index.updated_at = timezone.now()
                if not index.search_keyword:
                    keywords_str = generate_keywords(item['title'])
                    keywords_list = keywords_str.splitlines()
                    keywords_list = [element.split('. ', 1)[1] for element in keywords_list]
                    index.search_keyword = remove_brackets_and_append(keywords_list)
                if not index.reduced_title:
                    reduced_title = reduce_title(item['title'])
                    index.reduced_title = reduced_title
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
                if not index.description:
                    description = generate_description(item['title'])
                    index.description = description
                index.updated_at = timezone.now()
                index.save()
            except Exception as e:
                print("Error saving index values:", e)
        else:
            try:
                article, created = HankyungTitle.objects.get_or_create(title=item['title'])
                if created:
                    article.title = item['title']
                article.content = item['content']
                article.updated_at = timezone.now()
                article.save()
            except Exception as e:
                print("Error saving article info:", e)

        return item
    
    def open_spider(self, spider):
        log.info("Opening Spider: {}".format(spider.name))
        
        
    def close_spider(self, spider):
        log.info("Closing Spider: {}".format(spider.name))
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from dexmanager.models import SrcDex
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone

class IndexPipeline:
    def process_item(self, item, spider):
        caller_spider = spider.name
        if caller_spider == 'indicesinfo':
            try: 
                index = SrcDex.objects.get(title=item['title'])  # get existing one
            except ObjectDoesNotExist:
                index = SrcDex(title=item['title'])              # create new one
            try:
                index.closing = item['closing']
                index.updated_at = timezone.now()
                index.url = item['url']                        # make it enable when you want to update url
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
                index.updated_at = timezone.now()
                index.save()
            except Exception as e:
                print("Error saving index values:", e)
        return item
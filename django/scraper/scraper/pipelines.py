# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from dexmanager.models import SrcDex
from django.core.exceptions import ObjectDoesNotExist

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
                index.save()
            except Exception as e:
                print("Error saving index info:", e)
        else:
            try:
                index = SrcDex.objects.get(title=item['title'])
            except Exception as e:
                print("Error getting index info:", e)
            try:
                print("Saving index values:", item['values'])
                index.values = item['values']
                index.save()
            except Exception as e:
                print("Error saving index values:", e)
        return item
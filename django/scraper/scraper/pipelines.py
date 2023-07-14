# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from dexmanager.models import SrcDex

class IndexPipeline:
    def process_item(self, item, spider):
        index = SrcDex(title=item['title'], closing=item['closing'])
        try:
            index.save()
        except Exception as e:
            print("Error saving index:", e)
        return item
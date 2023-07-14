# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from index.models import Index

class IndexPipeline:
    def process_item(self, item, spider):
        index = Index(name=item['name'], closing=item['closing'])
        # print(index.name)
        # print(index.closing)
        print(type(index))
        try:
            index.save()
        except Exception as e:
            
            print("Error saving index:", e)    
        # return scrapy_item
        # print(type(item))
        # print(type(scrapy_item))
        # item.save()
        return item
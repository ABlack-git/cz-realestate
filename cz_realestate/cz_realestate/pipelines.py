import logging
from .mappers import ItemDocumentMapper

log = logging.getLogger(__name__)


class MongoPipeline:

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        pass

    def process_item(self, item, spider):
        mapper = ItemDocumentMapper(item)
        log.info(f"Saving {type(item)} item with id {mapper.get_item_id()} to database")
        doc = mapper.get_document()
        doc.save()

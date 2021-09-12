from mongoengine import Document
from .items import BezrealitkyFlatItem
from .entities import BezrealitkyListing


class ItemDocumentMapper:
    known_item_types = [BezrealitkyFlatItem]

    def __init__(self, item):
        self.item = item

        if type(self.item) not in self.known_item_types:
            raise ValueError(f'Unknown item type: {type(self.item)}')

    def get_document(self) -> Document:
        if isinstance(self.item, BezrealitkyFlatItem):
            doc = BezrealitkyListing(
                listing_id=self.item.listing_id,
                uri=self.item.uri,
                title=self.item.title,
                sub_title=self.item.sub_title,
                info=self.item.info
            )
            doc.set_coordinates(self.item.coordinates.lng, self.item.coordinates.lat)
        else:
            raise ValueError(f'Unknown item type: {type(self.item)}')

        return doc

    def get_item_id(self):
        if isinstance(self.item, BezrealitkyFlatItem):
            return self.item.listing_id

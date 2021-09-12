from datetime import datetime
import mongoengine as mongoe
from . import mongoutils


@mongoutils.update_modified.apply
class BezrealitkyListing(mongoe.Document):
    listing_id = mongoe.LongField(required=True)
    uri = mongoe.StringField(required=True)
    title = mongoe.StringField(required=True)
    sub_title = mongoe.StringField(required=True)
    coords = mongoe.PointField()
    info = mongoe.DictField()
    active = mongoe.BooleanField(default=True)
    created_on = mongoe.DateTimeField(default=datetime.utcnow)
    modified_on = mongoe.DateTimeField(default=datetime.utcnow)

    meta = {'collection': 'bezrealitky'}

    @property
    def coordinates(self):
        return self.coords['coordinates']

    @coordinates.setter
    def coordinates(self, value):
        if not isinstance(value, dict) or 'lat' not in value or 'lng' not in value:
            raise ValueError("Value should be dict containing 'lat' and 'lng' keys")

        self.coords = [value['lng'], value['lat']]

    def set_coordinates(self, lng, lat):
        self.coords = [lng, lat]

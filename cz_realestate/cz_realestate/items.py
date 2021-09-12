from dataclasses import dataclass


@dataclass
class Coordinates:
    lat: float = None
    lng: float = None


@dataclass()
class BezrealitkyFlatItem:
    listing_id: str = None
    uri: str = None
    title: str = None
    sub_title: str = None
    coordinates: Coordinates = None
    info: dict = None

    @property
    def coords(self):
        return [self.coordinates.lng, self.coordinates.lat]

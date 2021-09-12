from enum import Enum
from typing import Dict


class ApartmentInfo(Enum):
    FEES = ('Fees', 'fees', int)
    DEPOSIT = ('Refundable security deposit', 'deposit', int)
    FLOOR_SPACE = ('Floor Space', 'floor_space', int)
    FLOOR = ('Floor', 'floor', int)
    LISTING_ID = ('Listing ID', 'listing_id', int)
    PRICE = ('Price', 'price', int)
    TOWN = ('Town', 'town', str)
    LAYOUT = ('Layout', 'layout', str)
    AVAILABLE_FROM = ('Available from', 'available_from', str)
    OWNERSHIP_TYPE = ('Ownership Type', 'ownership_type', str)
    BUILDING_TYPE = ('Building Type', 'building_type', str)
    CONDITION = ('Condition', 'condition', str)
    FURNITURE = ('Furnishing and Fittings', 'furniture', str)
    AGE = ('Age', 'age', str)
    DESIGN = ('Design', 'design', str)
    HEATING = ('Heating', 'heating', str)
    RENOVATION = ('Renovation', 'renovation', str)
    FLOOR_IN_BUILDING = ('Total number of floors', 'floor_in_building', str)
    FRONT_GARDEN = ('Front garden', 'front_garden', str)
    DISTRICT = ('Metropolitan district', 'district', str)
    PENB = ('PENB', 'penb', str)
    BALCONY = ('Balcony', 'balcony', bool)
    TERRACE = ('Terrace', 'terrace', bool)
    GARAGE = ('Garage', 'garage', bool)
    LIFT = ('Lift', 'lift', bool)
    NEW_BUILDING = ('New building', 'new_building', bool)
    PARKING = ('Parking', 'parking', bool)
    LOGGIA = ('Loggia', 'loggia', bool)
    CELLAR = ('Cellar', 'cellar', bool)

    def __init__(self, info_name, key, prop_type):
        self.info_name: str = info_name
        self.key: str = key
        self.prop_type: type = prop_type


INFO_MAPPING: Dict[str, ApartmentInfo] = {info_enum.info_name: info_enum for info_enum in ApartmentInfo}

LAYOUT_MAPPING = {
    'Small studio': 'Garsoniera',
    'Studio': '1kk',
    '1 bedroom': '1+1',
    '1 bedroom with open-plan kitchen': '2+kk',
    '2 bedroom': '2+1',
    '2 bedroom with open-plan kitchen': '3+kk',
    '3 bedroom': '3+1',
    '3 bedroom with open-plan kitchen': '4+kk',
    '4 bedroom': '4+1',
    '4 bedroom with open-plan kitchen': '5+kk',
    '5 bedroom': '5+1',
    '5 bedroom with open-plan kitchen': '5+kk',
    '6 bedroom': '6+1',
    '6 bedroom with open-plan kitchen': '7+kk',
    '7 bedroom': '7+1',
    'Other': 'Other'
}

import scrapy
from urllib.parse import urlencode
import unicodedata

from ..items import BezrealitkyFlatItem, Coordinates
from ..enums import INFO_MAPPING, ApartmentInfo, LAYOUT_MAPPING
from ..entities import BezrealitkyListing


class BezrealitkyPragueRentSpider(scrapy.Spider):
    name = "bezrealitky_prague_rents"
    base_url = 'https://www.bezrealitky.com/properties-flats-houses'
    api_url = 'https://www.bezrealitky.cz/api/record/markers'

    def start_requests(self):
        request_body = {
            'offerType': 'pronajem',
            'estateType': 'byt',
            'boundary': str([[{"lat": 50.0998947, "lng": 14.6911961}, {"lat": 50.0721289, "lng": 14.6999919},
                              {"lat": 50.0568947, "lng": 14.6401916}, {"lat": 50.0188407, "lng": 14.669537},
                              {"lat": 49.9944411, "lng": 14.6401518}, {"lat": 50.0163634, "lng": 14.582393},
                              {"lat": 50.0108381, "lng": 14.5274725}, {"lat": 49.9707711, "lng": 14.4622402},
                              {"lat": 49.9706693, "lng": 14.4006472}, {"lat": 49.9419006, "lng": 14.395562},
                              {"lat": 49.9572087, "lng": 14.3254392}, {"lat": 49.9676279, "lng": 14.344916},
                              {"lat": 49.9718588, "lng": 14.3268138}, {"lat": 49.9906467, "lng": 14.3427236},
                              {"lat": 50.0022104, "lng": 14.2948377}, {"lat": 50.0235957, "lng": 14.3158639},
                              {"lat": 50.0583091, "lng": 14.2480852}, {"lat": 50.0771366, "lng": 14.2893735},
                              {"lat": 50.1029963, "lng": 14.2244355}, {"lat": 50.1300802, "lng": 14.302453},
                              {"lat": 50.1160189, "lng": 14.3607835}, {"lat": 50.1480311, "lng": 14.3657001},
                              {"lat": 50.141429, "lng": 14.3949016}, {"lat": 50.1774301, "lng": 14.5268551},
                              {"lat": 50.1501702, "lng": 14.5632297}, {"lat": 50.1541328, "lng": 14.5990028},
                              {"lat": 50.1452435, "lng": 14.5877286}, {"lat": 50.1293063, "lng": 14.6008738},
                              {"lat": 50.1226041, "lng": 14.6591154}, {"lat": 50.1065008, "lng": 14.657436},
                              {"lat": 50.0998947, "lng": 14.6911961}]]).replace(' ', '').replace("'", '"'),
            'hasDrawnBoundary': 'true',
            'locationInput': 'Praha'
        }
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        return [scrapy.Request(url=self.api_url, headers=headers, body=urlencode(request_body),
                               callback=self.process_start_request, method='POST')]

    def process_start_request(self, response):
        requests = []
        current_ids = {int(flat['id']) for flat in response.json()}
        active_listings = BezrealitkyListing.objects(active=True)
        ids_to_ignore = set()

        # update inactive listings and ignore listings that are still active both in db and on a website
        for active_listing in active_listings:
            if active_listing.listing_id not in current_ids:
                active_listing.active = False
                active_listing.save()
            else:
                ids_to_ignore.add(active_listing.listing_id)

        self.logger.info(f"Found {len(current_ids)} listings. After filtering {len(current_ids) - len(ids_to_ignore)} "
                         f"listings remain")

        for flat in response.json():
            if int(flat['id']) not in ids_to_ignore:
                kwargs = {
                    'listing_id': flat['id'],
                    'uri': flat['uri']
                }
                url = self.base_url + '/' + flat['uri']
                requests.append(scrapy.Request(url=url, callback=self.parse, cb_kwargs=kwargs))

        return requests

    def parse(self, response, **kwargs) -> BezrealitkyFlatItem:
        self.logger.info(f"Parsing listing with id {kwargs['listing_id']} and uri {kwargs['uri']}")
        flat_item = BezrealitkyFlatItem()
        flat_item.listing_id = kwargs['listing_id']
        flat_item.uri = kwargs['uri']

        flat_item.title = response.xpath('.//h1[contains(@class, "heading__title")]/span/text()').get()
        flat_item.sub_title = response.xpath('.//h1[contains(@class,"heading__title")]'
                                             '/span[contains(@class, "heading__perex")]/text()').get().strip()

        lng = float(response.xpath('.//div[contains(@class, b-map)]/@data-lng').get())
        lat = float(response.xpath('.//div[contains(@class, b-map)]/@data-lat').get())
        flat_item.coordinates = Coordinates(lat=lat, lng=lng)
        flat_item.info = self._process_info_table(response)

        return flat_item

    def _process_info_table(self, response) -> dict:
        info_dict = {}
        table_entries = response.xpath('.//h2[text()="Specifications"]/following-sibling::table/tbody/tr')
        for table_entry in table_entries:
            apartment_info_key = table_entry.xpath('th/text()').get().strip(':')
            if apartment_info_key == 'Project name':
                value = table_entry.xpath('td/a/text()').get()
            else:
                value = table_entry.xpath('td/text()').get()
            if apartment_info_key in INFO_MAPPING:
                try:
                    info_type = INFO_MAPPING[apartment_info_key]
                    info_dict[info_type.key] = self._process_info_value(value, info_type)
                except (ValueError, KeyError) as e:
                    self.logger.error(f"Error occurred when processing info entry {apartment_info_key} with value "
                                      f"{value}", e)
                    self.logger.warning(f"Skipping processing of {apartment_info_key}")
            else:
                self.logger.warning(f"{apartment_info_key} key is not known")
                key = apartment_info_key.lower().replace(' ', '_')
                # remove any diacritic
                key = ''.join(c for c in unicodedata.normalize('NFD', key) if not unicodedata.combining(c))
                info_dict[key] = value

        return info_dict

    def _process_info_value(self, value, info_type):
        if info_type.prop_type == str:
            if info_type == ApartmentInfo.LAYOUT:
                return LAYOUT_MAPPING[value]
            return value
        if info_type.prop_type == int:
            if info_type == ApartmentInfo.FLOOR_SPACE:
                return int(value.split(' ')[0])
            elif info_type in (ApartmentInfo.PRICE, ApartmentInfo.FEES, ApartmentInfo.DEPOSIT):
                return int(value.split(' ')[1].replace(',', ''))
            else:
                return int(value)
        elif info_type.prop_type == bool:
            return value.lower() in ('yes', 'true', 'y', 'ano')

import logging
import sys
from mongoengine import connect
from pymongo.errors import ServerSelectionTimeoutError
from scrapy.crawler import Crawler

log = logging.getLogger(__name__)


class MongoExtension:
    def __init__(self, db, host, port):
        self.db = db
        self.host = host
        self.port = port

    @classmethod
    def from_crawler(cls, crawler: Crawler):
        log.info(f"Establishing connection with mongodb.")
        db = crawler.settings.get('MONGO_DB')
        host = crawler.settings.get('MONGO_HOST')
        port = crawler.settings.getint('MONGO_PORT')

        client = connect(db=db, host=host, port=port)
        try:
            info = client.server_info()
            log.info(f"Connection established, mongo version: {info['version']}")
        except ServerSelectionTimeoutError:
            log.critical(f"Cannot establish connection with mongo instance. Crawler will be shut down.", exc_info=True)
            sys.exit(-1)

        return cls(db, host, port)

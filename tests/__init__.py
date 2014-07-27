#!/usr/bin/python
# -*- coding: utf-8 -*-


from cow.testing import CowTestCase
from tests.sandbox.server import SandboxServer
from tests.sandbox.config import Config


class TestCase(CowTestCase):
    def get_config(self):
        return dict(
            SQLALCHEMY_CONNECTION_STRING="mysql+mysqldb://root@localhost:3306/test_cow",
            SQLALCHEMY_POOL_SIZE=1,
            SQLALCHEMY_POOL_MAX_OVERFLOW=0,
            SQLALCHEMY_AUTO_FLUSH=True,
            COMMIT_ON_REQUEST_END=False,
            REDISHOST='localhost',
            REDISPORT=7575,
            REDISPUBSUB=True,
            ELASTIC_SEARCH_HOST='localhost',
            ELASTIC_SEARCH_PORT=9200,
            ELASTIC_SEARCH_INDEX='cow-test',
            MONGO_DATABASES={
                'default': {
                    'host': 'localhost',
                    'port': 4445,
                    'database': 'cow-motorengine'
                }
            },
            MONGOHOST='localhost',
            MONGOPORT=4445,
            MONGODATABASE='cow-motor',
            PUSHER_APP_ID=83144,
            PUSHER_KEY='850aacc45509459d4c1b',
            PUSHER_SECRET='0e4c46d1b5c8fc4c1dc6'
        )

    def get_server(self):
        cfg = Config(**self.get_config())

        self.server = SandboxServer(config=cfg)
        return self.server

#!/usr/bin/python
# -*- coding: utf-8 -*-

from derpconf.config import Config

Config.define('TESTCONF', 'test-configuration', "Test configuration in sandbox", 'Section')
Config.define('MONGOHOST', 'localhost', "Database configuration", "section")
Config.define('MONGOPORT', 6667, "Database configuration", "section")
Config.define('MONGODATABASE', 'test-db', "Database configuration", "section")

Config.define('REDISHOST', 'localhost', "Database configuration", "section")
Config.define('REDISPORT', 7780, "Database configuration", "section")
Config.define('REDISDB', 0, "Database Configuration", "section")
Config.define('REDISPASS', None, "Database Configuration", "section")

Config.define('ELASTIC_SEARCH_HOST', 'localhost', "Search configuration", "section")
Config.define('ELASTIC_SEARCH_PORT', 9200, "Search configuration", "section")

Config.define('GEOPY_GOOGLE_DOMAIN', 'maps.googleapis.com', "Google Maps domain", "GeoPy")
Config.define('GEOPY_GOOGLE_PROTOCOL', 'http', "Google Maps protocol", "GeoPy")
Config.define('GEOPY_GOOGLE_CLIENT_ID', None, "Google Maps API Client ID", "GeoPy")
Config.define('GEOPY_GOOGLE_SECRET_KEY', None, "Google Maps API Secret Key", "GeoPy")

Config.define('SQLALCHEMY_CONNECTION_STRING', '', "Database connection string", "SQLAlchemy")
Config.define('SQLALCHEMY_POOL_SIZE', 10, "Database connection pool size", "SQLAlchemy")

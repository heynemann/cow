#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

from tornado_geopy.geocoders import GoogleV3

from cow.plugins import BasePlugin


class GeoPyGooglePlugin(BasePlugin):
    @classmethod
    def after_start(cls, application, io_loop=None, *args, **kw):
        domain = application.config.get('GEOPY_GOOGLE_DOMAIN')
        protocol = application.config.get('GEOPY_GOOGLE_PROTOCOL')
        client_id = application.config.get('GEOPY_GOOGLE_CLIENT_ID')
        secret_key = application.config.get('GEOPY_GOOGLE_SECRET_KEY')

        logging.info("Creating GoogleV3 GeoPy connection at %s://%s..." % (protocol, domain))

        application.google_geocoder = GoogleV3(
            io_loop=application.io_loop,
            domain=domain,
            protocol=protocol,
            client_id=client_id,
            secret_key=secret_key
        )

    @classmethod
    def before_end(cls, application, *args, **kw):
        if hasattr(application, 'elastic_search'):
            logging.info("Disconnecting from GoogleV3 GeoPy...")
            del application.google_geocoder

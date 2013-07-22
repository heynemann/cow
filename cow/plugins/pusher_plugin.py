#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

#import pusherclient
import pusher
from tornado import ioloop
from tornado.concurrent import return_future

from cow.plugins import BasePlugin


class Pusher(object):
    def __init__(self, publisher, io_loop=None):
        self.io_loop = io_loop
        if self.io_loop is None:
            self.io_loop = ioloop.IOLoop.instance()

        self.publisher = publisher

    @return_future
    def publish(self, channel, event_name, event_data, callback):
        self.publisher[channel].trigger(event_name, event_data, callback=callback)


class PusherPlugin(BasePlugin):
    @classmethod
    def after_start(cls, application, io_loop=None, *args, **kw):
        app_id = application.config.get('PUSHER_APP_ID')
        key = application.config.get('PUSHER_KEY')
        secret = application.config.get('PUSHER_SECRET')

        if not app_id or not key or not secret:
            raise RuntimeError("PUSHER_APP_ID, PUSHER_KEY and PUSHER_SECRET configurations are all required.")

        logging.info("Connecting to pusher...")
        pusher.app_id = app_id
        pusher.key = key
        pusher.secret = secret
        pusher.channel_type = pusher.TornadoChannel
        publisher = pusher.Pusher()

        application.pusher = Pusher(publisher=publisher, io_loop=io_loop)

    @classmethod
    def before_end(cls, application, *args, **kw):
        if hasattr(application, 'pusher'):
            logging.info("Disconnecting from pusher...")
            del application.pusher

    @classmethod
    def before_healthcheck(cls, application, callback, *args, **kw):
        callback(True)

    @classmethod
    def validate(cls, result, *args, **kw):
        return result

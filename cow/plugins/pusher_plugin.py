#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

import pusherclient
import pusher
from tornado import ioloop

from cow.plugins import BasePlugin


class Pusher(object):
    def __init__(self, subscriber, publisher, io_loop=None):
        self.io_loop = io_loop
        if self.io_loop is None:
            self.io_loop = ioloop.IOLoop.instance()

        self.subscriber = subscriber
        self.publisher = publisher

    def subscribe(self, channel, event_name, callback):
        channel = self.subscriber.subscribe(channel)
        channel.bind(event_name, self.handle_event(callback))

    def handle_event(self, callback):
        def handle(self, *args, **kwargs):
            self.io_loop.add_callback(callback, *args, **kwargs)
        return handle

    def publish(self, channel, event_name, event_data, callback):
        self.publisher[channel].trigger(event_name, event_data, callback=callback)


class MotorPlugin(BasePlugin):
    @classmethod
    def after_start(cls, application, io_loop=None, *args, **kw):
        app_id = application.config.get('PUSHER_APP_ID')
        key = application.config.get('PUSHER_KEY')
        secret = application.config.get('PUSHER_SECRET')

        if not app_id or not key or not secret:
            raise RuntimeError("PUSHER_APP_ID, PUSHER_KEY and PUSHER_SECRET configurations are all required.")

        logging.info("Connecting to pusher...")
        subscriber = pusherclient.Pusher(key)
        publisher = pusher.Pusher(app_id=app_id, key=key, secret=secret)

        application.pusher = Pusher(subscriber=subscriber, publisher=publisher, io_loop=io_loop)

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

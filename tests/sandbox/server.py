#!/usr/bin/python
# -*- coding: utf-8 -*-

from cow.server import Server
from cow.plugins.motor_plugin import MotorPlugin
from cow.plugins.motorengine_plugin import MotorEnginePlugin
from cow.plugins.redis_plugin import RedisPlugin
from cow.plugins.es_plugin import ESPlugin
from cow.plugins.geopy_google_plugin import GeoPyGooglePlugin

from tests.sandbox.handlers.test import TestHandler


class SandboxServer(Server):
    def get_handlers(self):
        return (
            ('/', TestHandler),
        )

    def get_plugins(self):
        return [
            MotorPlugin,
            MotorEnginePlugin,
            RedisPlugin,
            ESPlugin,
            GeoPyGooglePlugin
        ]

if __name__ == '__main__':
    SandboxServer.run()

#!/usr/bin/python
# -*- coding: utf-8 -*-

from cow.server import Server
from cow.plugins.es_plugin import ESPlugin
from cow.plugins.motor_plugin import MotorPlugin
from cow.plugins.redis_plugin import RedisPlugin
from cow.plugins.pusher_plugin import PusherPlugin
from cow.plugins.gandalf_plugin import GandalfPlugin
from cow.plugins.sqlalchemy_plugin import SQLAlchemyPlugin
from cow.plugins.mongoengine_plugin import MongoEnginePlugin
from cow.plugins.motorengine_plugin import MotorEnginePlugin

from tests.sandbox.handlers.test import TestHandler


class SandboxServer(Server):
    def get_handlers(self):
        return (
            ('/', TestHandler),
        )

    def get_plugins(self):
        return [
            ESPlugin,
            MotorPlugin,
            RedisPlugin,
            # PusherPlugin,  # removed until pusher supports python 3+
            GandalfPlugin,
            SQLAlchemyPlugin,
            MotorEnginePlugin,
            MongoEnginePlugin
        ]

if __name__ == '__main__':
    SandboxServer.run()

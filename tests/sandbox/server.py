#!/usr/bin/python
# -*- coding: utf-8 -*-

from cow.server import Server
from cow.plugins.motor_plugin import MotorPlugin

from tests.sandbox.handlers.test import TestHandler


class SandboxServer(Server):
    def get_handlers(self):
        return (
            ('/', TestHandler),
        )

    def get_plugins(self):
        return [
            MotorPlugin
        ]

if __name__ == '__main__':
    SandboxServer.run()

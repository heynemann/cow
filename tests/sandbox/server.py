#!/usr/bin/python
# -*- coding: utf-8 -*-

from cow.server import Server

from tests.sandbox.handlers.test import TestHandler


class SandboxServer(Server):
    def get_handlers(self):
        return (
            ('/', TestHandler),
        )

if __name__ == '__main__':
    SandboxServer.run()

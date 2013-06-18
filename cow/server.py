#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os.path import exists, join
import inspect
import imp

from tornado.web import Application
from derpconf.config import Config


class Server(object):
    def __init__(self, debug=False):
        self.root_path = inspect.getfile(self.__class__)
        self.debug = debug
        self.application = self.get_app()
        self.config_module = self.load_config_module()
        self.application.config = self.get_config()

    @property
    def template_path(self):
        return join(self.root_path, 'templates')

    @property
    def static_path(self):
        return join(self.root_path, 'static')

    def get_config(self):
        return self.config_module()

    def load_config_module(self):
        config_path = join(self.root_path.rstrip('/'), 'config')
        module_path = join(config_path, '__init__.py')
        if exists(config_path) and exists(module_path):
            config = imp.load_source('cowserver.config', module_path)
            return config.Config

        return Config

    def get_app(self):
        return Application(self.get_handlers(), self.get_settings())

    def get_handlers(self):
        raise NotImplementedError('You must implement the get_handlers method in your Server implementation')

    def get_settings(self):
        return {
            'debug': self.debug,
            'template_path': self.template_path,
            'static_path': self.static_path,
        }

    def start(self):
        pass

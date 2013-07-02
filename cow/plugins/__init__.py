#!/usr/bin/env python
# -*- coding: utf-8 -*-


class BasePlugin(object):
    @classmethod
    def before_start(cls, server):
        pass

    @classmethod
    def after_start(cls, server):
        pass

    @classmethod
    def before_end(cls, server):
        pass

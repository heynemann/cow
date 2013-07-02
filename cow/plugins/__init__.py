#!/usr/bin/env python
# -*- coding: utf-8 -*-


class BasePlugin(object):
    @classmethod
    def before_start(cls, server, *args, **kw):
        pass

    @classmethod
    def after_start(cls, server, *args, **kw):
        pass

    @classmethod
    def before_end(cls, server, *args, **kw):
        pass

    @classmethod
    def before_healthcheck(cls, server, handler, callback, *args, **kw):
        pass

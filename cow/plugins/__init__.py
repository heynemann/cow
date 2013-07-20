#!/usr/bin/env python
# -*- coding: utf-8 -*-


class BasePlugin(object):
    @classmethod
    def after_start(cls, server, *args, **kw):
        pass

    @classmethod
    def before_end(cls, server, *args, **kw):
        pass

    @classmethod
    def before_healthcheck(cls, application, callback, *args, **kw):
        callback(True)

    @classmethod
    def validate(cls, result, *args, **kw):
        return result

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import sys

import mongoengine
import mongoengine.connection
from pymongo.errors import AutoReconnect

from cow.plugins import BasePlugin


class MongoEnginePlugin(BasePlugin):
    @classmethod
    def after_start(cls, application, io_loop=None, *args, **kw):
        databases = application.config.get('MONGO_DATABASES')

        if not databases or not isinstance(databases, (dict,)):
            raise RuntimeError("MONGO_DATABASES configuration is required and should be a dictionary.")

        items = databases.items()
        for index, (key, value) in enumerate(items):
            host = value['host']
            port = int(value['port'])
            db = value['database']
            username = value.get('username', None)
            password = value.get('password', None)

            conn_str = "mongodb://%s:%d/%s" % (host, port, db)

            if username is not None:
                if password is not None:
                    conn_str = "mongodb://%s:%s@%s:%d/%s" % (username, password, host, port, db)
                else:
                    conn_str = "mongodb://%s@%s:%d/%s" % (username, host, port, db)

            arguments = dict(
                host=conn_str,
            )

            arguments['alias'] = key

            replica_set = arguments.get('replica_set', None)
            if replica_set is not None:
                arguments['replicaSet'] = replica_set

            logging.info("Connecting to mongodb at %s" % conn_str)

            mongoengine.connect(db, **arguments)

            if index == 0:
                arguments.pop('alias')
                mongoengine.connect(db, **arguments)


    @classmethod
    def before_end(cls, application, *args, **kw):
        pass
        #databases = application.config.get('MONGO_DATABASES')
        #for key in databases.keys():
            #logging.info("Disconnecting from mongodb[%s]..." % key)
            #mongoengine.disconnect(alias=key)

    @classmethod
    def before_healthcheck(cls, application, callback, *args, **kw):
        databases = application.config.get('MONGO_DATABASES')
        for key in databases.keys():
            conn = mongoengine.connection.get_connection(alias=key).connection
            try:
                callback(conn.command('ping'))
            except AutoReconnect:
                logging.exception(sys.exc_info()[1])
                callback({})

    @classmethod
    def validate(cls, result, *args, **kw):
        return result.get('ok', 0) == 1.0

    @classmethod
    def define_configurations(cls, config):
        config.define('MONGO_DATABASES', None, "Dictionary holding all the mongodb connections to be made.", "MotorEngine")

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

from sqlalchemy import create_engine, exc
from sqlalchemy.orm import scoped_session, sessionmaker

from cow.plugins import BasePlugin


class SQLAlchemyMixin(object):
    @property
    def db(self):
        return self.application.sqlalchemy_db


class SQLAlchemyPlugin(BasePlugin):
    @classmethod
    def after_start(cls, application, io_loop=None, *args, **kw):
        autoflush = application.config.get('SQLALCHEMY_AUTO_FLUSH', False)
        connstr = application.config.SQLALCHEMY_CONNECTION_STRING
        engine = create_engine(
            connstr,
            convert_unicode=True,
            pool_size=application.config.SQLALCHEMY_POOL_SIZE,
            max_overflow=application.config.SQLALCHEMY_POOL_MAX_OVERFLOW,
            echo=application.server.debug
        )

        logging.info("Connecting to \"%s\" using SQLAlchemy" % connstr)

        application.sqlalchemy_db = scoped_session(sessionmaker(bind=engine, autoflush=autoflush))

    @classmethod
    def before_healthcheck(cls, application, callback, *args, **kw):
        try:
            result = application.sqlalchemy_db.execute("SELECT 1").fetchone()
            callback(result[0])
        except exc.OperationalError, ex:
            if ex.args[0] in (2006,   # MySQL server has gone away
                              2013,   # Lost connection to MySQL server during query
                              2055):  # Lost connection to MySQL server at '%s', system error: %d
                # caught by pool, which will retry with a new connection
                raise exc.DisconnectionError()
            else:
                raise

    @classmethod
    def validate(cls, result, *args, **kw):
        if not result:
            logging.exception("Could not connect using SQLAlchemy.")
            return False

        return result == 1

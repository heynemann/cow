cow framework
=============

[![Build Status](https://travis-ci.org/heynemann/cow.png?branch=master)](https://travis-ci.org/heynemann/cow)
[![PyPi version](https://pypip.in/v/cow-framework/badge.png)](https://crate.io/packages/cow-framework/)
[![PyPi downloads](https://pypip.in/d/cow-framework/badge.png)](https://crate.io/packages/cow-framework/)
[![Coverage Status](https://coveralls.io/repos/heynemann/cow/badge.png?branch=master)](https://coveralls.io/r/heynemann/cow?branch=master)
[![codeq](https://codeq.io/github/heynemann/cow/badges/master.png)](https://codeq.io/github/heynemann/cow/branches/master)

introduction
------------

cow is a web framework in the sense that it allows users to create tornado applications with configuration, templates and static files very easily without being a different beast.

cow automates most of the boring parts of tornado, allowing users to write only the part that actually matters: the handlers.

installing
----------

Installing cow is as easy as:

    pip install cow-framework

writing my first cow application
--------------------------------

After installing cow, go to the folder where you want to create your application and type:

    cow myproject

This command will create the basic infrastructure for your project:

* server.py - the heart of your app and the place where you should put your handlers;
* templates - folder where you can store all your applications templates;
* static - folder where your static files should go;
* config - folder where your configuration files should be;
* config/__init__.py - module where you can declare your configuration default values.

Running your new application is as easy as:

    python server.py

To confirm that your application is running, type the following command:

    curl http://localhost:4444/healthcheck/

You should get as the result the string `WORKING`.

how do I add my own handlers
----------------------------

If you open `server.py`, you'll see that it has a method called `get_handlers` that should return a list of handlers that will be passed to tornado. This is where you can put your own handlers.

Suppose we have a `HelloWorldHandler` that writes `Hello World` to our users, like the following:

    from tornado.web import RequestHandler

    class HelloWorldHandler(RequestHandler):
        def get(self):
            self.write("Hello World!")

Then in our server.py `Server` class, we need to add it to a route, like this:

    from cow.server import Server as CowServer
    from myproject.handlers.hello_world import HelloWorldHandler

    class Server(CowServer):
        def get_handlers(self):
            return (
                ('/', HelloWorldHandler),
            )

Now if you run `server.py` and access `http://localhost:4444/` you should see the string `Hello World`.

how do I test my code
---------------------

It's really simple. You can use tornado's `AsyncHTTPTestCase`, like this:

    from tornado.testing import AsyncHTTPTestCase
    from myproject.server import Server  # the same server as in the above code

    class TestHelloWorld(AsyncHTTPTestCase):
        def get_app(self):
            return Server().application

        def test_hello_world(self):
            response = self.fetch('/')
            assert response.code == 200
            assert response.body == 'Hello World'

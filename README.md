cow framework
=============

[![Build Status](https://travis-ci.org/heynemann/cow.png?branch=master)](https://travis-ci.org/heynemann/cow)
[![PyPi version](https://pypip.in/v/cow-framework/badge.png)](https://crate.io/packages/cow-framework/)
[![PyPi downloads](https://pypip.in/d/cow-framework/badge.png)](https://crate.io/packages/cow-framework/)
[![Coverage Status](https://coveralls.io/repos/heynemann/cow/badge.png?branch=master)](https://coveralls.io/r/heynemann/cow?branch=master)

introduction
------------

cow is a web framework in the sense that it allows users to create tornado applications with configuration, templates and static files very easily without being a different beast.

cow automates most of the boring parts of tornado, allowing users to write only the part that actually matters: the handlers.

installing
----------

Installing cow is as easy as:

    pip install cow-framework

how to start a new app
----------------------

Just create a server.py file that looks like this:

    from cow.server import Server
    from cow.plugins.motorengine_plugin import MotorEnginePlugin


    def main():
        AppServer.run()


    class AppServer(Server):
        def get_handlers(self):
            return (
                # Add your handlers here
                # ('/', TestHandler),
            )

        def get_plugins(self):
            # add whatever plug-ins you want to use here
            return [
                MotorEnginePlugin,
            ]

    if __name__ == '__main__':
        AppServer.run()

To run your app, just use `python server.py`, or add the `main` method to your `setup.py` file as a command.


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

It's really simple. You can use cow's `CowTestCase`, like this:

    from cow.testing import CowTestCase
    from myproject.server import Server  # the same server as in the above code

    class TestHelloWorld(CowTestCase):
        def get_config(self):
            return {}  # add whatever configuration your app requires

        def get_server(self):
            cfg = Config(**self.get_config())
            return Server(cfg)

        def test_hello_world(self):
            response = self.fetch('/')
            assert response.code == 200
            assert response.body == 'Hello World'

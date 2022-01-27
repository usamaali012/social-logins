import tornado
from tornado.web import Application
from tornado.httpserver import HTTPServer
from tornado import ioloop
from apis import HomePageHandler, SuccessPageHandler, TokenHandler, FbHandler


class MyServer(Application):
    def __init__(self):
        handler = self.GetHandler()
        Application.__init__(self, handler)
        # self.application = Application.__init__(self, handler)

    def GetHandler(self):
        handler = [
            (r"/", HomePageHandler),
            (r"/success", SuccessPageHandler),
            (r'/tokensignin', TokenHandler),
            (r'/me', FbHandler),
        ]

        return handler

    def start_server(self):
        self.listen(8091)
        print("Port running at 8091")
        tornado.ioloop.IOLoop.current().start()
        #
        # ssl_options = {
        #     "certfile": "/var/pyTest/keys/ca.csr",
        #     "keyfile": "/var/pyTest/keys/ca.key",
        # }

        # http_server = HTTPServer(self.application, ssl_options=ssl_options)
        # http_server.listen(8091)
        # print("Port running at 8091")
        # tornado.ioloop.IOLoop.current().start()


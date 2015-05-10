# -*- coding: utf-8 -*-
import sys

from tornado import wsgi, web, httpserver, ioloop
from werkzeug.debug import DebuggedApplication


class MultiStaticFileHandler(web.StaticFileHandler):
    def initialize(self):
        self.root = ''

    def set_extra_headers(self, path):
        self.set_header('Cache-control', 'no-cache')

    @classmethod
    def get_absolute_path(cls, root, path):
        from django.contrib.staticfiles import finders
        return finders.find(path)

    def validate_absolute_path(self, root, absolute_path):
        return absolute_path


def get_server(debug=None):
    from django.conf import settings
    from keybar.wsgi import application as django_application
    from keybar.utils.crypto import get_server_context

    if debug is None:
        debug = settings.DEBUG

    app = DebuggedApplication(django_application, evalex=debug)

    container = wsgi.WSGIContainer(app)

    application = web.Application([
        (r'/static/(.*)', MultiStaticFileHandler, {}),
        (r'.*', web.FallbackHandler, dict(fallback=container)),
    ], debug=debug)

    server = httpserver.HTTPServer(
        application,
        ssl_options=get_server_context(verify=settings.KEYBAR_VERIFY_CLIENT_CERTIFICATE))
    return server


def run_server():
    server = get_server()

    print('Start server on https://keybar.local:8443')

    server.listen(8443, 'keybar.local')

    try:
        ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        sys.exit(0)


if __name__ == '__main__':
    run_server()

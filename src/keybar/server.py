# -*- coding: utf-8 -*-
import sys

from tornado import wsgi, web, httpserver, ioloop
from django.conf import settings
from django.contrib.staticfiles import finders
from werkzeug.debug import DebuggedApplication


class MultiStaticFileHandler(web.StaticFileHandler):
    def initialize(self):
        self.root = ''

    def set_extra_headers(self, path):
        self.set_header('Cache-control', 'no-cache')

    @classmethod
    def get_absolute_path(cls, root, path):
        return finders.find(path)

    def validate_absolute_path(self, root, absolute_path):
        return absolute_path


def get_server(debug=settings.DEBUG):
    from keybar.wsgi import application as django_application
    from keybar.utils.logging import enable_error_logging_in_debug_mode
    from keybar.utils.crypto import get_server_context

    app = DebuggedApplication(django_application, evalex=debug)

    enable_error_logging_in_debug_mode()

    container = wsgi.WSGIContainer(app)

    application = web.Application([
        (r'/static/(.*)', MultiStaticFileHandler, {}),
        (r'.*', web.FallbackHandler, dict(fallback=container)),
    ], debug=debug)

    # TODO: enable verify
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

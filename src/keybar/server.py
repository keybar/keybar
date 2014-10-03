#-*- coding: utf-8 -*-
import sys

from tornado import wsgi, web, httpserver, ioloop

from django.conf import settings

from keybar.wsgi import application as django_application
from keybar.utils.crypto import get_server_context


class MultiStaticFileHandler(web.StaticFileHandler):
    def initialize(self, paths):
        self.paths = paths

    def set_extra_headers(self, path):
        self.set_header("Cache-control", "no-cache")

    def get(self, path):
        for try_path in self.paths:
            try:
                super(MultiStaticFileHandler, self).initialize(try_path)
                # HACK… no idea how to properly put a try/except around a future
                # expression
                return super(MultiStaticFileHandler, self).get(path).result()
            except web.HTTPError as exc:
                if exc.status_code == 404:
                    continue
                raise

        raise web.HTTPError(404)


def get_server():
    container = wsgi.WSGIContainer(django_application)

    static_media_paths = settings.STATICFILES_DIRS + (settings.MEDIA_ROOT,)

    application = web.Application([
        (r'/static/(.*)', MultiStaticFileHandler, {'paths': static_media_paths}),
        (r".*", web.FallbackHandler, dict(fallback=container)),
    ])

    # TODO: enable verify
    server = httpserver.HTTPServer(
        application,
        ssl_options=get_server_context(verify=False))
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

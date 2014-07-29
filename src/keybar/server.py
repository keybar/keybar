import sys

from tornado import wsgi, web, httpserver, ioloop

from django.conf import settings

from keybar.wsgi import application as django_application
from keybar.utils.security import get_server_context


def run_server():
    container = wsgi.WSGIContainer(django_application)

    application = web.Application([
        (r'/static/(.*)', web.StaticFileHandler, {'path': settings.STATIC_ROOT}),
        (r'/media/(.*)', web.StaticFileHandler, {'path': settings.MEDIA_ROOT}),
        (r".*", web.FallbackHandler, dict(fallback=container)),
    ], debug=True)

    # TODO: enable verify
    server = httpserver.HTTPServer(
        application,
        ssl_options=get_server_context(verify=False))

    print('Start server on https://keybar.local:8443')

    server.listen(8443, 'keybar.local')

    try:
        ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        sys.exit(0)


if __name__ == '__main__':
    run_server()

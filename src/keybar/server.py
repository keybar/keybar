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
    ])

    # TODO: enable verify
    server = httpserver.HTTPServer(
        application,
        ssl_options=get_server_context(verify=False))

    print('Start server on https://local.keybar.io:8443')

    server.listen(8443, 'local.keybar.io')

    try:
        ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        sys.exit(0)


# Another, simpler method
"""
import BaseHTTPServer, SimpleHTTPServer
import ssl

httpd = BaseHTTPServer.HTTPServer(
    ('localhost', 4443),
    SimpleHTTPServer.SimpleHTTPRequestHandler)
httpd.socket = ssl.wrap_socket(
    httpd.socket,
    certfile='path/to/localhost.pem',
    server_side=True)
httpd.serve_forever()
"""

if __name__ == '__main__':
    run_server()

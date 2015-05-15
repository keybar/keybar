import socket
import errno

from pytest_django.live_server_helper import parse_addr
from django.test.testcases import LiveServerThread as LiveServerThreadBase
from django.db import connections
from tornado import ioloop

from keybar.server import get_server


class LiveServerThread(LiveServerThreadBase):
    ports = range(8990, 9999)

    def run(self):
        if self.connections_override:
            # Override this thread's database connections with the ones
            # provided by the main thread.
            for alias, conn in self.connections_override.items():
                connections[alias] = conn
        try:
            self.server = get_server(debug=False)

            for index, port in enumerate(self.possible_ports):
                try:
                    self.server.listen(port, 'keybar.local')
                except socket.error as exc:
                    if (index + 1 < len(self.possible_ports) and exc.errno == errno.EADDRINUSE):
                        # This port is already in use, so we go on and try with
                        # the next one in the list.
                        continue
                    else:
                        # Either none of the given ports are free or the error
                        # is something else than "Address already in use". So
                        # we let that error bubble up to the main thread.
                        raise exc
                else:
                    # A free port was found.
                    self.port = port
                    break

            self.is_ready.set()
            self.loop = ioloop.IOLoop.instance()
            self.loop.start()
        except Exception as exc:
            self.terminate()
            self.error = exc
            self.is_ready.set()

    def terminate(self):
        if hasattr(self, 'loop'):
            # Stop the WSGI server
            self.server.stop()
            self.loop.stop()


class LiveServer:
    def __init__(self, addr):
        host, possible_ports = parse_addr(addr)
        self.thread = LiveServerThread(host, possible_ports, None)
        self.thread.daemon = True
        self.thread.start()
        self.thread.is_ready.wait()

        if self.thread.error:
            raise self.thread.error

    def stop(self):
        """Stop the server"""
        self.thread.terminate()
        self.thread.join()

    @property
    def url(self):
        return 'https://{0}'.format(self.domain)

    @property
    def domain(self):
        return '{0}:{1}'.format(self.thread.host, self.thread.port)

    def __str__(self):
        return self.url

    def __add__(self, other):
        return str(self) + other

    def __repr__(self):
        return '<LiveServer listening at {0}>'.format(self.url)

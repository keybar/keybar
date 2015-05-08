# -*- coding: utf-8 -*-
import pkg_resources


class ServerHeaderMiddleware:
    distribution_version = pkg_resources.get_distribution('keybar').version

    def process_response(self, request, response):
        response['Server'] = 'Keybar/{0}'.format(self.distribution_version)
        return response

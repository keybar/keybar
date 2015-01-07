# Some code stolen from httpie (https://github.com/jakubroztocil/httpie/) :)

import os
import sys
import json
import time
import pkg_resources
from textwrap import dedent

from argparse import (RawDescriptionHelpFormatter, FileType,
                      OPTIONAL, ZERO_OR_MORE, SUPPRESS, ArgumentParser)

# Set default settings so that django.setup() works
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'keybar.settings')

import django
django.setup()

import requests
import click
from httpie.models import Environment
from httpie.output import PygmentsProcessor
from django.utils.encoding import force_text

from keybar.client import Client
from keybar.models.user import User


def format_body(body):
    try:
        obj = json.loads(body)
    except ValueError:
        # Invalid JSON, ignore.
        pass
    else:
        # Indent, sort keys by name, and avoid
        # unicode escapes to improve readability.
        body = json.dumps(obj, sort_keys=True, ensure_ascii=False, indent=4)
    return body


class HTTPieHelpFormatter(RawDescriptionHelpFormatter):
    def __init__(self, max_help_position=6, *args, **kwargs):
        # A smaller indent for args help.
        kwargs['max_help_position'] = max_help_position
        super(HTTPieHelpFormatter, self).__init__(*args, **kwargs)

    def _split_lines(self, text, width):
        text = dedent(text).strip() + '\n\n'
        return text.splitlines()


class Environment(object):
    verbose = False
    debug = False
    traceback = False
    client = None


pass_env = click.make_pass_decorator(Environment)


@click.group()
@click.version_option(pkg_resources.get_distribution('keybar').version)
@click.option('--verbose', '-v', is_flag=True, help='Enables verbose mode.')
@click.option('--traceback', is_flag=True, help='Shows traceback on error.')
@click.option('--debug', is_flag=True, help='Enable debug mode.')
@click.pass_context
def cli(ctx, verbose, traceback, debug):
    ctx.obj = Environment()
    ctx.obj.traceback = traceback
    ctx.obj.debug = debug
    ctx.obj.start = time.time()

    user = User.objects.get(email='admin@admin.admin')
    secret = open('src/keybar/tests/resources/rsa_keys/id_rsa', 'rb').read()
    device_id = user.devices.all().first().id.hex
    ctx.obj.client = Client(device_id, secret)


def _request(env, method, endpoint):
    try:
        response = getattr(env.client, method)('https://keybar.local:8443{endpoint}'.format(
            endpoint=endpoint
        ))

        headers = '\n'.join(
            '{key}: {value}'.format(key=key, value=value) for key, value in response.headers.items()
        )
        formatted_body = format_body(force_text(response.content))

        processor = PygmentsProcessor()

        click.echo('\n{headers}\n\n{body}\n\nTime Taken: {time}\n'.format(
            headers=processor.process_headers(headers),
            body=processor.process_body(formatted_body, 'application/json', 'json', 'utf-8'),
            time=time.time() - env.start
        ))
    except (KeyboardInterrupt, SystemExit):
        if env.traceback:
            raise
        click.echo('\n', file=sys.stderr)
    except Exception as exc:
        if env.traceback:
            raise
        click.echo('{0}: {1}'.format(type(exc).__name__, str(exc)), file=sys.stderr)


@cli.command()
@click.argument('endpoint')
@pass_env
def get(env, endpoint):
    _request(env, 'get', endpoint)


@cli.command()
@click.argument('endpoint')
@pass_env
def post(env, endpoint):
    _request(env, 'post', endpoint)


if __name__ == '__main__':
    cli()

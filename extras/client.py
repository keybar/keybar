# Some code stolen from httpie (https://github.com/jakubroztocil/httpie/) :)

import os
import sys
import json
import time
from textwrap import dedent

from argparse import (RawDescriptionHelpFormatter, FileType,
                      OPTIONAL, ZERO_OR_MORE, SUPPRESS, ArgumentParser)

# Set default settings so that django.setup() works
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'keybar.settings')

import django
django.setup()

import requests
from httpie.models import Environment
from httpie.input import Parser
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
        text = textwrap.dedent(text).strip() + '\n\n'
        return text.splitlines()


parser = ArgumentParser(
    formatter_class=HTTPieHelpFormatter,
    description='Keybar',
    epilog=dedent('''
    For every --OPTION there is also a --no-OPTION that reverts OPTION
    to its default value.
    Suggestions and bug reports are greatly appreciated:
        https://github.com/keybar/keybar/issues
    ''')
)

positional = parser.add_argument_group(
    title='Positional Arguments',
    description=dedent('''
    These arguments come after any flags and in the order they are listed here.
    Only URL is required.
    ''')
)

positional.add_argument(
    'endpoint',
    metavar='ENDPOINT',
    help='''
    '''
)


troubleshooting = parser.add_argument_group(title='Troubleshooting')

troubleshooting.add_argument(
    '--traceback',
    action='store_true',
    default=True,
    help='''
    '''
)

troubleshooting.add_argument(
    '--debug',
    action='store_true',
    default=True,
    help='''
    '''
)

def main(args=sys.argv[1:], env=Environment()):
    """Run the main program and write the output to ``env.stdout``.
    Return exit status code.
    """
    def error(msg, *args, **kwargs):
        msg = msg % args
        level = kwargs.get('level', 'error')
        env.stderr.write('\nhttp: %s: %s\n' % (level, msg))

    debug = True
    traceback = True
    exit_status = 0

    try:
        args = parser.parse_args(args=args)

        # TODO: allow customization
        secret = open('extras/example_keys/id_rsa', 'rb').read()
        user = User.objects.get(email='admin@admin.admin')
        device_id = user.devices.all().first().id.hex

        start = time.time()

        client = Client(device_id, secret)

        endpoint = args.endpoint

        response = client.get('https://keybar.local:8443{endpoint}'.format(
            endpoint=endpoint
        ))

        headers = '\n'.join(
            '{key}: {value}'.format(key=key, value=value) for key, value in response.headers.items()
        )
        formatted_body = format_body(force_text(response.content))

        processor = PygmentsProcessor()

        env.stdout.write('\n{headers}\n\n{body}\n\nTime Taken: {time}\n'.format(
            headers=processor.process_headers(headers),
            body=processor.process_body(formatted_body, 'application/json', 'json', 'utf-8'),
            time=time.time() - start
        ))
    except (KeyboardInterrupt, SystemExit):
        if traceback:
            raise
        env.stderr.write('\n')
        exit_status = 1

    except requests.Timeout:
        exit_status = 1
        error('Request timed out (%ss).', args.timeout)

    except Exception as e:
        if traceback:
            raise
        error('%s: %s', type(e).__name__, str(e))
        exit_status = 1

    return exit_status


main()

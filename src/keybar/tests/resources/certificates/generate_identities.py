#!/usr/bin/env python
import argparse
import os

from py509.x509 import (
    make_certificate_authority, make_certificate_signing_request,
    make_certificate, make_pkey, make_serial)

from OpenSSL import crypto

from keybar.utils.logging import get_logger

# Based on https://github.com/sholsapp/python-ssl-playground/blob/master/bin/generate-identities

logger = get_logger(__name__)


NOW = 0
TEN_YEARS = 10 * 365 * 24 * 60 * 60


def write_key(path, name, obj):
    with open(os.path.join(path, name + '.key'), 'wb') as fh:
        fh.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, obj))


def write_cert(path, name, obj):
    with open(os.path.join(path, name + '.cert'), 'wb') as fh:
        fh.write(crypto.dump_certificate(crypto.FILETYPE_PEM, obj))


def write_trust(path, name, *args):
    with open(os.path.join(path, name + '-ca-bundle.crt'), 'wb') as fh:
        fh.write(b'\n'.join(
            [crypto.dump_certificate(crypto.FILETYPE_PEM, cert) for cert in args]
        ))


def make_tls_chain(path, dry_run, chain_name):
    root = '%s-ROOT' % chain_name
    root_key, root_cert = make_certificate_authority(CN=root)
    logger.info('Made [%s] subject [%s]', root, root_cert.get_subject())

    if not dry_run:
        write_key(path, root, root_key)
        write_cert(path, root, root_cert)

    intermediates = []

    intermediate = '%s-intermediate' % chain_name

    intermediate_key = make_pkey(key_bits=1024)
    int_csr = make_certificate_signing_request(
        intermediate_key, CN=intermediate, OU=intermediate)
    intermediate_cert = make_certificate(
        int_csr, root_key, root_cert, make_serial(), NOW, TEN_YEARS,
        exts=[crypto.X509Extension(b'basicConstraints', True, b'CA:TRUE')])

    if not dry_run:
        write_key(path, intermediate, intermediate_key)
        write_cert(path, intermediate, intermediate_cert)

    intermediates.append(intermediate_cert)
    logger.info(
        'Made [%s] subject [%s] from [%s]',
        intermediate, intermediate_cert.get_subject(), root_cert.get_subject())

    server = '%s-SERVER' % intermediate
    server_key = make_pkey(key_bits=1024)
    server_csr = make_certificate_signing_request(
        server_key, CN='keybar.local', OU=server)
    server_cert = make_certificate(
        server_csr, intermediate_key, intermediate_cert, make_serial(), NOW,
        TEN_YEARS,
        exts=[crypto.X509Extension(
            b'subjectAltName', True, b'IP:192.168.0.1,URI:i-am-a-server')])

    if not dry_run:
        write_key(path, server, server_key)
        write_cert(path, server, server_cert)

    logger.info(
        'Made [%s] subject [%s] from [%s]',
        server, server_cert.get_subject(), intermediate_cert.get_subject())

    client = '%s-CLIENT' % intermediate
    client_key = make_pkey(key_bits=1024)
    client_csr = make_certificate_signing_request(client_key, CN='keybar.local', OU=client)
    client_cert = make_certificate(
        client_csr, intermediate_key, intermediate_cert, make_serial(), NOW, TEN_YEARS,
        exts=[crypto.X509Extension(
            b'subjectAltName', True, b'IP:192.168.0.2,URI:i-am-a-client')])

    if not dry_run:
        write_key(path, client, client_key)
        write_cert(path, client, client_cert)

    logger.info(
        'Made [%s] subject [%s] from [%s]',
        client, client_cert.get_subject(), intermediate_cert.get_subject())

    if not dry_run:
        write_trust(path, chain_name, root_cert, *intermediates)


def main():
    parser = argparse.ArgumentParser(
        description='Generate sample certificates for a fake public key infrastructure.')
    parser.add_argument(
        '-o', '--output', default=os.getcwd(),
        help='The output directory to place generated files.')
    parser.add_argument(
        '-d', '--dry-run', action='store_true',
        help='Should generated files be written to disk?')
    args = parser.parse_args()

    make_tls_chain(args.output, args.dry_run, 'KEYBAR')


if __name__ == '__main__':
    main()

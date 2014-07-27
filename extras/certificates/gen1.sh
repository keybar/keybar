#!/bin/bash
CAROOT=.
mkdir -p ${CAROOT}/ca.db.certs   # Signed certificates storage
touch ${CAROOT}/ca.db.index      # Index of signed certificates
echo 01 > ${CAROOT}/ca.db.serial # Next (sequential) serial number

# Configuration
cat>${CAROOT}/ca.conf<<'EOF'
[ ca ]
default_ca = ca_default

[ ca_default ]
dir = REPLACE_LATER
certs = $dir
new_certs_dir = $dir/ca.db.certs
database = $dir/ca.db.index
serial = $dir/ca.db.serial
RANDFILE = $dir/ca.db.rand
certificate = $dir/ca.crt
private_key = $dir/ca.key
default_days = 3650
default_crl_days = 30
default_md = md5
preserve = no
policy = generic_policy
[ generic_policy ]
countryName = optional
stateOrProvinceName = optional
localityName = optional
organizationName = optional
organizationalUnitName = optional
commonName = supplied
emailAddress = optional
EOF

sed -i "s|REPLACE_LATER|${CAROOT}|" ${CAROOT}/ca.conf

cd ${CAROOT}

# Generate CA private key
openssl genrsa -out ca.key 1024

# Create Certificate Signing Request
openssl req -new -key ca.key  \
                 -out ca.csr

# Create self-signed certificate
openssl x509 -req -days 10000 \
          -in ca.csr      \
          -out ca.crt     \
          -signkey ca.key

# Create private/public key pair
openssl genrsa -out server.key 4096

# Create Certificate Signing Request
openssl req -new -key server.key \
                 -out server.csr

# Sign key
openssl ca -config ${CAROOT}/ca.conf   \
           -in server.csr              \
           -cert ${CAROOT}/ca.crt      \
           -keyfile ${CAROOT}/ca.key   \
           -out server.crt

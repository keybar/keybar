Keybar
======

This project aims to implement a safe, open and easy to use password store.
Basically it'll be a simple web-application that exposes it's functionality
via a simple REST-Api.

It'll be extensible and easily deployable. With that in mind it'll be easy to
not just host it almost everywhere a certain Python/Django environment is supported
but more importantly to easily host it yourself on your own personal computer.

Ideas
=====

General ideas so that they don't get lost.

Client:

 * Generate GnuPG Key
 * Share public key with server
 * Server sends gpg encrypted message with current token
 * From now on communication based on Fernet encryption

 -> Retrieve password
 -> Set password
 -> ...

Server:

 * Register user with GnuPG key
 * Generate user specific token that expires in a short amount of time
 * Send the token gpg-encrypted to the user
 * Accept only Fernet based encryption communication for all other endpoints

Storage:

 * `cryptography` provides a simple PBKDF2HMAC KDF interface
 * With high enough iterations, a huge random salt (at least 256 bit) and a `length` of at least 256
   the encryption will take hopefully enough time (10s on my laptop) to make it quite hard to actually break through.

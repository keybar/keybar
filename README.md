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

Why yet another password storage?
=================================

In the future, storage systems like Keepass, 1Password, LastPass or others can be supported.

With that in mind, I generally wanted to implement one specific feature on top of LastPass (I use currently), and that
was "change all passwords on a regular basis". With more than 200 sites registered with unique
passwords it takes way too long to change all relevant passwords on a regular basis.

Since LastPass in particular does not provide any good API and in general is sort of a blackbox (we know they are using PBKDF2 but don't see any code or specifics) the only way was to step up and do it myself. To host the storage system in an environment I trust.

With others I generally I don't like the idea of unlocking all my passwords
with just one "key" - usually some kind of a password. There has to be other ways…

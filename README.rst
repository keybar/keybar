======
Keybar
======

.. warning::

   Keybar is under heavy development. Don't use it.


**Keybar** is a framework, service and client for secure password storage and exchange.

.. figure:: https://keybar.readthedocs.org/en/latest/_images/logo.jpeg
   :align: right
   :target: http://thenounproject.com/term/safe/1411/


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

 * Retrieve password
 * Set password
 * ...

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


Installation
------------

.. code-block:: bash

    $ Create your virtualenv (recommended, use virtualenvwrapper)
    $ mkvirtualenv keybar

    $ # Clone repository
    $ git clone git@github.com:keybar/keybar.git

    $ # Activate Environment and install
    $ workon keybar
    $ make develop

    $ # run tests
    $ make test


Edit settings
-------------

Create a new file ``src/keybar/settings.py`` with the following content:

.. code-block:: python

    from keybar.conf.development import *

Edit and adapt this file to your specific environment.


Setup the database
------------------

Create an empty new PostgreSQL database (any other supported by Django works too).

.. code-block:: bash

    $ createdb keybar_dev

.. note::

    You might need to apply a postgresql user (``createdb -U youruser``) e.g ``postgres``
    for proper permissions.


.. code-block:: bash

    $ python manage.py migrate


Superuser & example data
------------------------

.. code-block:: bash

    $ # Create a new super user
    $ python manage.py createsuperuser

Now you can run the webserver and start using the site.

.. code-block:: bash

   $ python manage.py runserver

This starts a local webserver on `localhost:8000 <http://localhost:8000/>`_. To view the administration
interface visit `/admin/ <http://localhost:8000/admin/>`_

Run Celery and other services
-----------------------------

Other services being used:

* Celery, is being used to run [regular] tasks, e.g for mail output.
* Compass, is being used to compile our scss files and the foundation framework.

.. note::

   To test oauth services we require using a SSL server for local development.
   It's not required for regular development but the default setup is using SSL.

   Please install ``stunnel``.

   $ brew install stunnel


To start all of them (including the runserver):

.. code-block:: bash

   $ foreman start

.. note::

   Please make sure you have the ``foreman`` gem installed.

.. note::

    You can find the SSL version on `port 8443 <https://localhost:8443/>`_


Resources
---------

* `Documentation <http://keybar.readthedocs.org>`_
* `Bug Tracker <https://github.com/keybar/keybar/issues>`_
* `Code <https://github.com/keybar/keybar>`_

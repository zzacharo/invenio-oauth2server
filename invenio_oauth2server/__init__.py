# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2018 CERN.
#
# Invenio is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# Invenio is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Invenio; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA 02111-1307, USA.
#
# In applying this license, CERN does not
# waive the privileges and immunities granted to it by virtue of its status
# as an Intergovernmental Organization or submit itself to any jurisdiction.

"""Invenio module that implements OAuth 2 server.

Usage
=====

Protecting your REST API with authentication
--------------------------------------------

If you want to have your REST API endpoints protected using OAuth you
should register their blueprint inside the API app
(InvenioOAuth2ServerREST) which by default includes a ``before_request`` hook.
This hook will, if there is an OAuth token, verify it and set the current user
accordingly. It is important to highlight that this configuration allows
either authenticated clients or anonymous clients.

In case you need to allow access to a resource only for authenticated clients,
you should use the `require_api_auth
<api.html#invenio_oauth2server.decorators.require_api_auth>`__
decorator which requires OAuth2 login:

.. code-block:: python

    @app.route('/api/resource', methods=['GET'])
    @require_api_auth()
    def index():
        return 'Protected resource'

However, protecting your resources only with authentication is not
recommended. Instead, you should add an extra layer using always
`scopes <api.html#invenio_oauth2server.models.Scope>`__. This is because,
basically, any client that owns a token has control over every user resource.
Therefore, using scopes gives a fine-grain control. Here an example using
the default ``email_scope``:

.. code-block:: python

    from invenio_oauth2server.scopes import email_scope

    @app.route('/api/email', methods=['GET'])
    @require_api_auth()
    @require_oauth_scopes(email_scope.id_)
    def index():
        return 'admin@inveniosoftware.org'

Delegating rights via scopes
----------------------------

As mentioned before, the recommended way to protect your endpoints is to use
fine-grain control with scopes. Invenio-OAuth2Server offers the possibility to
create new ones:

.. code-block:: python

    from invenio_oauth2server.models import Scope

    homepage_read = Scope('homepage:read',
                          help_text='Access to the homepage',
                          group='test')

Next, you should add them to ``setup.py`` entrypoints so they get initialized
at start up:

.. code-block:: python

    setup(
        ...
        entry_points={
            'invenio_oauth2server.scopes': [
                'homepage_read = path.to.scopes.file:homepage_read',
            ]
        }
        ...
    )

And then, they can be used in your application:

.. code-block:: python

    from path.to.scopes.file import homepage_read

    @app.route('/', methods=['GET'])
    @require_api_auth()
    @require_oauth_scopes(homepage_read.id_)
    def index():
        return 'Front page content.'

So, finally, with this example, we would allow any authenticated client with
rights to use the ``homepage_scope`` to read the homepage but, prevent from
reading the email if they do not have rights for using the ``email_scope``.

To test this features you can build your own application or use the provided
:doc:`example app </examplesapp>` as boilerplate.

Access control
--------------

It is important to remember that the usage of authentication and scopes is not
enough in most of the cases so access control need to be configured as well.
For more information about access control in Invenio you can visit
`Invenio-Access
<http://invenio-access.readthedocs.io/en/latest/>`__ documentation.


"""

from __future__ import absolute_import, print_function

from .ext import InvenioOAuth2Server, InvenioOAuth2ServerREST
from .proxies import current_oauth2server
from .version import __version__
from .decorators import require_api_auth, require_oauth_scopes

__all__ = (
    '__version__',
    'InvenioOAuth2Server',
    'InvenioOAuth2ServerREST',
    'require_api_auth',
    'require_oauth_scopes',
    'current_oauth2server',
)

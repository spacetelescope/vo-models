.. vo-models documentation master file, created by
   sphinx-quickstart on Tue Dec 26 11:13:34 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

vo-models
---------

``vo-models`` an open-source project to provide Python models for `IVOA <https://www.ivoa.net/>`_ service protocols.

The project is designed to be used by IVOA members, service implementors, and developers to help facilitate the development of IVOA-compliant services and clients.

Features
^^^^^^^^

- **Pydantic-xml Models:** The project includes Python models for IVOA protocols, using `pydantic-xml <https://github.com/dapper91/pydantic-xml>`_. Based on `Pydantic <https://docs.pydantic.dev/latest/>`_, these models describe transactions for an IVOA protocol, such as UWS, and feature automatic validation, parsing and serialization of XML data for use with Python clients and web frameworks.

User Guide
^^^^^^^^^^
.. toctree::
   :maxdepth: 1

   pages/installation

Supported Protocols
^^^^^^^^^^^^^^^^^^^
.. toctree::
   :maxdepth: 2

   pages/protocols/index

Indices and tables
^^^^^^^^^^^^^^^^^^
* :ref:`genindex`
* :ref:`modindex`
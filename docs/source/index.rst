
vo-models
=========

``vo-models`` an open-source project to provide Python models for `IVOA <https://www.ivoa.net/>`_ service protocols.

The project is designed to be used by IVOA members, service implementors, and developers to help facilitate the development of IVOA-compliant services and clients.

Features
^^^^^^^^

- **Pydantic-xml Models:** The project includes Python models for IVOA protocols, using `pydantic-xml <https://github.com/dapper91/pydantic-xml>`_. Based on `Pydantic <https://docs.pydantic.dev/latest/>`_, these models describe transactions for an IVOA protocol, such as UWS, and feature automatic validation, parsing and serialization of XML data for use with Python clients and web frameworks.

Using the models in your project for validation and serialization to XML is as simple as:

.. code-block:: python

    from vo_models.uws import ShortJobDescription

    job = ShortJobDescription(
        phase="PENDING",
        run_id = "run_1",
        job_id = "job_1",
        creation_time = "2021-01-01T00:00:00Z",
    )
    job.to_xml()

.. code-block:: xml

   <uws:jobref id="job_1" xlink:type="simple">
        <uws:phase>PENDING</uws:phase>
         <uws:runId>run_1</uws:runId>
    </uws:jobref>

For more information on getting started with ``vo-models``, see :ref:`quickstart`.

User Guide
^^^^^^^^^^
.. toctree::
   :maxdepth: 1

   pages/quickstart
   pages/installation

Supported Protocols
^^^^^^^^^^^^^^^^^^^
.. toctree::
   :maxdepth: 2

   pages/protocols/index

API Documentation
^^^^^^^^^^^^^^^^^
.. toctree::
   :maxdepth: 1

   pages/api/index

Links
^^^^^

- `Source Code <https://github.com/spacetelescope/vo-models>`_
- `Pydantic-xml <https://pydantic-xml.readthedocs.io/en/latest/>`_
- `Pydantic <https://docs.pydantic.dev/latest/>`_

Indices and tables
^^^^^^^^^^^^^^^^^^
* :ref:`genindex`
* :ref:`modindex`
.. _quickstart:

Quickstart
==========

Basic Usage
-----------

Working with ``vo-models`` classes is easy. They can be created and modified like any Pydantic model.

The following example creates a UWS :ref:`pages/protocols/uws:shortjobdescription` model using keyword arguments and updates the phase:

.. code-block:: python

    from vo_models.uws import ShortJobDescription

    job = ShortJobDescription(
        phase="PENDING",
        run_id = "run_1",
        job_id = "job_1",
        creation_time = "2021-01-01T00:00:00Z",
    )

    job.phase = "COMPLETED"

Deserializing
-------------

Models can also be created from JSON data or ``dicts``:

.. code-block:: python

    from vo_models.uws import ShortJobDescription
    import json

    data = """
    {
        "phase": "PENDING",
        "runId": "run_1",
        "jobId": "job_1",
        "creationTime": "2021-01-01T00:00:00Z"
    }
    """
    data = json.loads(data)
    job = ShortJobDescription(**data)

or from XML:

.. code-block:: python

    from vo_models.uws import ShortJobDescription

    xml = """
    <uws:jobref id="123" xlink:type="simple">
        <uws:phase>PENDING</uws:phase>
    </uws:jobref>'
    """

    job = ShortJobDescription.from_xml(xml)

Serializing
-----------

Models can be serialized to JSON using ``.model_dump_json()`` like any Pydantic model, or to XML using the ``to_xml()`` method of pydantic-xml:

.. grid:: 2
    :gutter: 2

    .. grid-item-card:: Model

        .. literalinclude:: ../../../examples/snippets/uws/uws.py
            :language: python
            :start-after: short-job-description-model-start
            :end-before: short-job-description-model-end

    .. grid-item-card:: Document

        .. tab-set::

            .. tab-item:: XML

                .. code-block:: xml

                    <uws:jobref xmlns:uws="http://www.ivoa.net/xml/UWS/v1.0"
                        xmlns:xlink="http://www.w3.org/1999/xlink"
                        xmlns:xsd="http://www.w3.org/2001/XMLSchema"
                        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                        id="job_1" xlink:type="simple" xlink:href="">
                        <uws:phase>PENDING</uws:phase>
                        <uws:runId>1234567890</uws:runId
                        ><uws:ownerId>anon_user</uws:ownerId>
                        <uws:creationTime>2023-12-27T16:35:39.628Z</uws:creationTime>
                    </uws:jobref>

            .. tab-item:: JSON

                .. code-block:: python

                    short_job_description.model_dump_json()

                .. code-block:: json

                    {"phase":"PENDING",
                    "run_id":"1234567890",
                    "owner_id":"anon_user",
                    "creation_time":"2023-12-27T16:35:39.628Z",
                    "job_id":"job_1",
                    "type":"simple",
                    "href":null}

Optional Elements
-----------------

Some models may have a number of optional elements. By default, ``pydantic-xml`` will include them in the output XML. To exclude them, you can use the ``skip_empty`` argument:

Without the ``skip_empty`` argument:

.. code-block:: python

    from vo_models.uws import JobSummary, Parameters

    job_summary = JobSummary[Parameters](
        job_id = "job_1",
        phase = "PENDING"
    )

    job_summary.to_xml()

.. code-block:: xml

    <uws:job xmlns:uws="http://www.ivoa.net/xml/UWS/v1.0"
        xmlns:xlink="http://www.w3.org/1999/xlink"
        xmlns:xsd="http://www.w3.org/2001/XMLSchema"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        version="1.1">
        <uws:jobId>job_1</uws:jobId>
        <uws:runId></uws:runId>
        <uws:ownerId xsi:nil="true"></uws:ownerId>
        <uws:phase>PENDING</uws:phase>
        <uws:quote xsi:nil="true"></uws:quote>
        <uws:creationTime></uws:creationTime>
        <uws:startTime xsi:nil="true"></uws:startTime>
        <uws:endTime xsi:nil="true"></uws:endTime>
        <uws:executionDuration>0</uws:executionDuration>
        <uws:destruction xsi:nil="true"></uws:destruction>
    </uws:job>

With the ``skip_empty`` argument:

.. code-block:: python

    job_summary.to_xml(skip_empty=True)

.. code-block:: xml

    <uws:job xmlns:uws="http://www.ivoa.net/xml/UWS/v1.0"
        xmlns:xlink="http://www.w3.org/1999/xlink"
        xmlns:xsd="http://www.w3.org/2001/XMLSchema"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        version="1.1">
        <uws:jobId>job_1</uws:jobId>
        <uws:phase>PENDING</uws:phase>
        <uws:executionDuration>0</uws:executionDuration>
    </uws:job>

Submodels And Namespaces
-------------------------

Sub-models can also be serialized to XML, and will correctly inherit their parent's namespace:

.. code-block:: python

    from vo_models.uws import JobSummary, Parameters, Results

    job_summary = JobSummary[Parameters](
    job_id = "job_1",
    owner_id = "anon_user",
    phase = "COMPLETED",
    creation_time = "2023-12-01T12:00:00.000Z",
    start_time = "2023-12-01T12:00:00.000Z",
    results = Results(
        results=[
            ResultReference(id="result1", href="http://example.com/result1"),
            ResultReference(id="result2", href="http://example.com/result2"),
            ],
        ),
    )

    job_summary.results.to_xml()

.. code-block:: xml

    <uws:results xmlns:uws="http://www.ivoa.net/xml/UWS/v1.0"
        xmlns:xlink="http://www.w3.org/1999/xlink"
        xmlns:xsd="http://www.w3.org/2001/XMLSchema"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
        <uws:result id="result1" xlink:type="simple" xlink:href="http://example.com/result1"/>
        <uws:result id="result2" xlink:type="simple" xlink:href="http://example.com/result2"/>
    </uws:results>'

For more information on how to use ``pydantic-xml``, see the `pydantic-xml documentation <https://pydantic-xml.readthedocs.io/en/latest/>`_.

For example usage of ``vo-models`` for each protocol, see :ref:`pages/protocols/index:supported protocols`.
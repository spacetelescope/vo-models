.. _uws:

UWS (Universal Worker Service)
------------------------------

UWS is a protocol for describing and executing jobs on remote services. ``vo-models`` currently provides support for the `UWS 1.1 version <https://www.ivoa.net/documents/UWS/20161024/REC-UWS-1.1-20161024.html>`_ of the protocol.

.. note::
    In the provided examples, the UWS namespace has not been included for brevity. As output by `to_xml()`, the namespace is included in the root element of the XML document.

Models for UWS are provided in the ``vo_models.uws`` package. Supported models and examples of their usage are:

Models
^^^^^^

ErrorSummary
*****************

Represents an error summary returned by a UWS service as part of a :ref:`pages/protocols/uws:JobSummary` object.

.. grid:: 2
    :gutter: 2

    .. grid-item-card:: Model

        .. literalinclude:: ../../../../examples/snippets/uws/uws.py
            :language: python
            :start-after: error-summary-model-start
            :end-before: error-summary-model-end

    .. grid-item-card:: XML Output

        .. literalinclude:: ../../../../examples/snippets/uws/uws.py
            :language: xml
            :lines: 2-
            :start-after: error-summary-xml-start
            :end-before: error-summary-xml-end

Parameter
*********

Represents a single parameter of a UWS job.

.. grid:: 2
    :gutter: 2

    .. grid-item-card:: Model

        .. literalinclude:: ../../../../examples/snippets/uws/uws.py
            :language: python
            :start-after: parameter-model-start
            :end-before: parameter-model-end

    .. grid-item-card:: XML Output

        .. literalinclude:: ../../../../examples/snippets/uws/uws.py
            :language: xml
            :lines: 2-
            :start-after: parameter-xml-start
            :end-before: parameter-xml-end

For multi-valued attributes, use the type `vo_models.uws.models.MultiValuedParameter` instead of ``list[Parameter]``.
This is equivalent to ``list[Parameter]`` but adds some special validation support required for multi-valued UWS job parameters.

Parameters
**********

Represents a collection of :ref:`pages/protocols/uws:parameter` objects.

.. attention:: This is a generic class that must be subclassed to represent the parameters of the specific service using the UWS protocol.

    See :ref:`pages/protocols/uws:jobsummary` for an example of how this is used in the context of a UWS job summary response.

For example, for a TAP service, the parameters could be represented as follows:

.. grid:: 2
    :gutter: 2

    .. grid-item-card:: Model

        .. literalinclude:: ../../../../examples/snippets/uws/uws.py
            :language: python
            :start-after: parameters-model-start
            :end-before: parameters-model-end

    .. grid-item-card:: XML Output

        .. literalinclude:: ../../../../examples/snippets/uws/uws.py
            :language: xml
            :lines: 2-
            :start-after: parameters-xml-start
            :end-before: parameters-xml-end

ResultReference
*****************

Represents a single result reference as returned by a UWS service as part of a :ref:`pages/protocols/uws:Results` object.

.. grid:: 2
    :gutter: 2

    .. grid-item-card:: Model

        .. literalinclude:: ../../../../examples/snippets/uws/uws.py
            :language: python
            :start-after: result-reference-model-start
            :end-before: result-reference-model-end

    .. grid-item-card:: XML Output

        .. literalinclude:: ../../../../examples/snippets/uws/uws.py
            :language: xml
            :lines: 2-
            :start-after: result-reference-xml-start
            :end-before: result-reference-xml-end

Results
********

Represents a collection of :ref:`pages/protocols/uws:resultreference` objects.

.. grid:: 2
    :gutter: 2

    .. grid-item-card:: Model

        .. literalinclude:: ../../../../examples/snippets/uws/uws.py
            :language: python
            :start-after: results-model-start
            :end-before: results-model-end

    .. grid-item-card:: XML Output

        .. literalinclude:: ../../../../examples/snippets/uws/uws.py
            :language: xml
            :lines: 2-
            :start-after: results-xml-start
            :end-before: results-xml-end

ShortJobDescription
*******************

Represents a UWS ``jobref`` element, returned when fetching the job list from a UWS service.

.. note::
    Note that the XML tag ``<uws:jobref>`` differs from the model name ``ShortJobDescription``.

    The Python model uses the name of the complexType defined in the UWS schema, but when serialized uses the tag name defined as part of the ``<xs:element>`` definition.

    See :ref:`pages/protocols/uws:Jobs` for an example of how this is used in the context of a UWS job list response.

.. grid:: 2
    :gutter: 2

    .. grid-item-card:: Model

        .. literalinclude:: ../../../../examples/snippets/uws/uws.py
            :language: python
            :start-after: short-job-description-model-start
            :end-before: short-job-description-model-end

    .. grid-item-card:: XML Output

        .. literalinclude:: ../../../../examples/snippets/uws/uws.py
            :language: xml
            :lines: 2-
            :start-after: short-job-description-xml-start
            :end-before: short-job-description-xml-end

Jobs
****

Represents a collection of :ref:`pages/protocols/uws:shortjobdescription` objects, returned at the UWS job list endpoint.

.. grid:: 2
    :gutter: 2

    .. grid-item-card:: Model

        .. literalinclude:: ../../../../examples/snippets/uws/uws.py
            :language: python
            :start-after: jobs-model-start
            :end-before: jobs-model-end

    .. grid-item-card:: XML Output

        .. literalinclude:: ../../../../examples/snippets/uws/uws.py
            :language: xml
            :lines: 2-
            :start-after: jobs-xml-start
            :end-before: jobs-xml-end

JobSummary
**********

A model for the complete representation of a UWS job summary, returned by fetching the job id from a UWS service.

.. attention::

    This is a generic class that expects to be provided a subclass of :ref:`pages/protocols/uws:parameters` to represent the parameters of the specific service using the UWS protocol.

    The example below uses the TAPParameters class, shown in the :ref:`pages/protocols/uws:parameters` example above, to represent the parameters of a TAP service.

.. note::
    In this example, we have included the XML namespace in the output, to show how the namespace is included in the root element of the XML document.
.. grid:: 2
    :gutter: 2

    .. grid-item-card:: Model

        .. literalinclude:: ../../../../examples/snippets/uws/uws.py
            :language: python
            :start-after: job-summary-model-start
            :end-before: job-summary-model-end

    .. grid-item-card:: XML Output

        .. literalinclude:: ../../../../examples/snippets/uws/uws.py
            :language: xml
            :lines: 2-
            :start-after: job-summary-xml-start
            :end-before: job-summary-xml-end

Simple Types
^^^^^^^^^^^^

The following simple types are provided in the ``vo_models.uws`` package for use in UWS models:

- :py:class:`vo_models.uws.types.ErrorType`
- :py:class:`vo_models.uws.types.ExecutionPhase`
- :py:class:`vo_models.uws.types.UWSVersion`

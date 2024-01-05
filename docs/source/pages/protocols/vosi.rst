.. _vosi:

VOSI (VO Support Interface)
--------------------------------------------

``vo-models`` supports the following VOSI v1.0 protocols:

Availability
*****************

The Availability model is used to represent the response given by a UWS service to a
``GET /availability`` request.

.. grid:: 2
    :gutter: 2

    .. grid-item-card:: Model

        .. literalinclude:: ../../../../examples/snippets/vosi/availability.py
            :language: python
            :start-after: model-start
            :end-before: model-end

    .. grid-item-card:: XML Output

        .. literalinclude:: ../../../../examples/snippets/vosi/availability.py
            :language: xml
            :lines: 2-
            :start-after: xml-start
            :end-before: xml-end
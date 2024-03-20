.. _vosi:

VOSI (VO Support Interface)
--------------------------------------------

``vo-models`` supports the following VOSI v1.0 protocols:

Availability
^^^^^^^^^^^^

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

Tables
^^^^^^

VOSITable
*********

For requests for a single table from the ``GET /tables/{table_name}`` endpoint, you can use the ``Table`` model.

.. note:: This model is functionally identical to the :ref:`pages/protocols/vodataservice:table` element, specifically namespaced under VOSI.

.. grid:: 2
    :gutter: 2

    .. grid-item-card:: Model

        .. literalinclude:: ../../../../examples/snippets/vosi/tables.py
            :language: python
            :start-after: table-model-start
            :end-before: table-model-end

    .. grid-item-card:: XML Output

        .. literalinclude:: ../../../../examples/snippets/vosi/tables.py
            :language: xml
            :lines: 2-
            :start-after: table-xml-start
            :end-before: table-xml-end


VOSITableSet
************

For requests to the ``GET /tables`` endpoint, you can use the ``TableSet`` model to represent table schemas, their child tables, and columns.

.. note:: This model is functionally identical to the :ref:`pages/protocols/vodataservice:tableset` element, specifically namespaced under VOSI.

.. grid:: 2
    :gutter: 2

    .. grid-item-card:: Model

        .. literalinclude:: ../../../../examples/snippets/vosi/tables.py
            :language: python
            :start-after: tableset-model-start
            :end-before: tableset-model-end

    .. grid-item-card:: XML Output

        .. literalinclude:: ../../../../examples/snippets/vosi/tables.py
            :language: xml
            :lines: 2-
            :start-after: tableset-xml-start
            :end-before: tableset-xml-end
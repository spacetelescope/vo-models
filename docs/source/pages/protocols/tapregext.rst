.. _tapregext:

TAPRegExt
----------

TAPRegExt is an IVOA XML encoding standard for describing TAP service metadata. It is used by the TAP standard to describe the capabilities of a TAP service.

`vo-models` currently supports the full TAPRegExt v1.0 standard. The key model is the ``TableAccess`` model, which represents the capabilities of a TAP server:

Models
^^^^^^

TableAccess
***********

This model represents the capabilities of a TAP server, used as part of the VOSI Capabilities standard.

.. grid:: 2
    :gutter: 2

    .. grid-item-card:: Model

        .. literalinclude:: ../../../../examples/snippets/tapregext/tapregext.py
            :language: python
            :start-after: TableAccess-model-start
            :end-before: TableAccess-model-end

    .. grid-item-card:: XML Output

            .. literalinclude:: ../../../../examples/snippets/tapregext/tapregext.py
                :language: xml
                :lines: 2-
                :start-after: TableAccess-xml-start
                :end-before: TableAccess-xml-end

See the :ref:`tapregext_api` documentation for more information on the models and types available.
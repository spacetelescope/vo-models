.. _voresource:

VOResource
----------

VOResource is an IVOA XML encoding standard for describing resource metadata. It is used by various IVOA standards, such as VODataService, VOSI, and TAPRegExt to describe resources and the services that provide access to them.

`vo-models` currently supports the full VOResource v1.1 standard. Some of the key elements include:

Models
^^^^^^

Resource
********

Any entity or component of a VO application that is describable and identifiable by an IVOA Identifier.

.. grid:: 2
    :gutter: 2

    .. grid-item-card:: Model

        .. literalinclude:: ../../../../examples/snippets/voresource/voresource.py
            :language: python
            :start-after: Resource-model-start
            :end-before: Resource-model-end

    .. grid-item-card:: XML Output

        .. literalinclude:: ../../../../examples/snippets/voresource/voresource.py
            :language: xml
            :lines: 2-
            :start-after: Resource-xml-start
            :end-before: Resource-xml-end

Service
*******

A resource that can be invoked by a client to perform some action on its behalf.

.. grid:: 2
    :gutter: 2

    .. grid-item-card:: Model

        .. literalinclude:: ../../../../examples/snippets/voresource/voresource.py
            :language: python
            :start-after: Service-model-start
            :end-before: Service-model-end

    .. grid-item-card:: XML Output

        .. literalinclude:: ../../../../examples/snippets/voresource/voresource.py
            :language: xml
            :lines: 2-
            :start-after: Service-xml-start
            :end-before: Service-xml-end

Capability
**********

A description of what the service does (in terms of context-specific behavior), and how to use it (in terms of an interface).

.. grid:: 2
    :gutter: 2

    .. grid-item-card:: Model

        .. literalinclude:: ../../../../examples/snippets/voresource/voresource.py
            :language: python
            :start-after: Capability-model-start
            :end-before: Capability-model-end

    .. grid-item-card:: XML Output

        .. literalinclude:: ../../../../examples/snippets/voresource/voresource.py
            :language: xml
            :lines: 2-
            :start-after: Capability-xml-start
            :end-before: Capability-xml-end

Interface
*********

A description of a service interface.

.. grid:: 2
    :gutter: 2

    .. grid-item-card:: Model

        .. literalinclude:: ../../../../examples/snippets/voresource/voresource.py
            :language: python
            :start-after: Interface-model-start
            :end-before: Interface-model-end

    .. grid-item-card:: XML Output

        .. literalinclude:: ../../../../examples/snippets/voresource/voresource.py
            :language: xml
            :lines: 2-
            :start-after: Interface-xml-start
            :end-before: Interface-xml-end

See the :ref:`voresource_api` documentation for more information on the available models and types.

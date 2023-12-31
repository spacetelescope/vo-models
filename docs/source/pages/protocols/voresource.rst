.. _voresource:

VOResource
----------

VOResource is an XML schema for describing IVOA resource metadata. ``vo-models`` currently supports the `VOResource 1.1 <https://www.ivoa.net/documents/VOResource/20180625/REC-VOResource-1.1.html>`_ version.

.. note::
    In the provided examples, the namespaces of the XML output has not been included for brevity. As output by `to_xml()`, the namespace is included in the root element of the XML document.

Models
^^^^^^

Validation
*****************

Represents the validation level of a IVOA resource

.. grid:: 2
    :gutter: 2

    .. grid-item-card:: Model

        .. literalinclude:: ../../../../examples/snippets/voresource/voresource.py
            :language: python
            :start-after: validation-model-start
            :end-before: validation-model-end

    .. grid-item-card:: XML Output

        .. literalinclude:: ../../../../examples/snippets/voresource/voresource.py
            :language: xml
            :lines: 2-
            :start-after: validation-xml-start
            :end-before: validation-xml-end

ResourceName
*****************

The name of a potentially registered resource.

.. grid:: 2
    :gutter: 2

    .. grid-item-card:: Model

        .. literalinclude:: ../../../../examples/snippets/voresource/voresource.py
            :language: python
            :start-after: resource-name-model-start
            :end-before: resource-name-model-end

    .. grid-item-card:: XML Output

        .. literalinclude:: ../../../../examples/snippets/voresource/voresource.py
            :language: xml
            :lines: 2-
            :start-after: resource-name-xml-start
            :end-before: resource-name-xml-end

Date
*****************

A date associated with a resource, with the added ability to specify the context.

.. grid:: 2
    :gutter: 2

    .. grid-item-card:: Model

        .. literalinclude:: ../../../../examples/snippets/voresource/voresource.py
            :language: python
            :start-after: date-model-start
            :end-before: date-model-end

    .. grid-item-card:: XML Output

        .. literalinclude:: ../../../../examples/snippets/voresource/voresource.py
            :language: xml
            :lines: 2-
            :start-after: date-xml-start
            :end-before: date-xml-end

Source
*****************

Represents the source of a particular resource or content.

.. grid:: 2
    :gutter: 2

    .. grid-item-card:: Model

        .. literalinclude:: ../../../../examples/snippets/voresource/voresource.py
            :language: python
            :start-after: source-model-start
            :end-before: source-model-end

    .. grid-item-card:: XML Output

        .. literalinclude:: ../../../../examples/snippets/voresource/voresource.py
            :language: xml
            :lines: 2-
            :start-after: source-xml-start
            :end-before: source-xml-end

Rights
*****************

Represents the rights associated with a resource or content.

.. grid:: 2
    :gutter: 2

    .. grid-item-card:: Model

        .. literalinclude:: ../../../../examples/snippets/voresource/voresource.py
            :language: python
            :start-after: rights-model-start
            :end-before: rights-model-end

    .. grid-item-card:: XML Output

        .. literalinclude:: ../../../../examples/snippets/voresource/voresource.py
            :language: xml
            :lines: 2-
            :start-after: rights-xml-start
            :end-before: rights-xml-end

AccessURL and MirrorURL
***********************

Represents the access and mirror URLs for a resource or content, respectively.

.. grid:: 2
    :gutter: 2

    .. grid-item-card:: Model

        .. literalinclude:: ../../../../examples/snippets/voresource/voresource.py
            :language: python
            :start-after: access-url-model-start
            :end-before: access-url-model-end

        .. literalinclude:: ../../../../examples/snippets/voresource/voresource.py
            :language: python
            :start-after: mirror-url-model-start
            :end-before: mirror-url-model-end

    .. grid-item-card:: XML Output

        .. literalinclude:: ../../../../examples/snippets/voresource/voresource.py
            :language: xml
            :lines: 2-
            :start-after: access-url-xml-start
            :end-before: access-url-xml-end

        .. literalinclude:: ../../../../examples/snippets/voresource/voresource.py
            :language: xml
            :lines: 2-
            :start-after: mirror-url-xml-start
            :end-before: mirror-url-xml-end

Contact
*******

Represents the contact information associated with a resource or content.

.. grid:: 2
    :gutter: 2

    .. grid-item-card:: Model

        .. literalinclude:: ../../../../examples/snippets/voresource/voresource.py
            :language: python
            :start-after: contact-model-start
            :end-before: contact-model-end

    .. grid-item-card:: XML Output

        .. literalinclude:: ../../../../examples/snippets/voresource/voresource.py
            :language: xml
            :lines: 2-
            :start-after: contact-xml-start
            :end-before: contact-xml-end

Creator
*******

Represents the creator (person or organisation) responsible for creating something.

.. grid:: 2
    :gutter: 2

    .. grid-item-card:: Model

        .. literalinclude:: ../../../../examples/snippets/voresource/voresource.py
            :language: python
            :start-after: creator-model-start
            :end-before: creator-model-end

    .. grid-item-card:: XML Output

        .. literalinclude:: ../../../../examples/snippets/voresource/voresource.py
            :language: xml
            :lines: 2-
            :start-after: creator-xml-start
            :end-before: creator-xml-end

Relationship
************

Describes the relationship between one or more resources.

Values for ``relationship_type`` should be taken from the `VOResource vocabulary <http://www.ivoa.net/rdf/voresource/relationship_type>`.

.. grid:: 2
    :gutter: 2

    .. grid-item-card:: Model

        .. literalinclude:: ../../../../examples/snippets/voresource/voresource.py
            :language: python
            :start-after: relationship-model-start
            :end-before: relationship-model-end

    .. grid-item-card:: XML Output

        .. literalinclude:: ../../../../examples/snippets/voresource/voresource.py
            :language: xml
            :lines: 2-
            :start-after: relationship-xml-start
            :end-before: relationship-xml-end

Security Method
***************

Describes the security method used to access a resource.

.. grid:: 2
    :gutter: 2

    .. grid-item-card:: Model

        .. literalinclude:: ../../../../examples/snippets/voresource/voresource.py
            :language: python
            :start-after: security-method-model-start
            :end-before: security-method-model-end

    .. grid-item-card:: XML Output

        .. literalinclude:: ../../../../examples/snippets/voresource/voresource.py
            :language: xml
            :lines: 2-
            :start-after: security-method-xml-start
            :end-before: security-method-xml-end

Curation
********

Describes the general curation of a resource.

.. grid:: 2
    :gutter: 2

    .. grid-item-card:: Model

        .. literalinclude:: ../../../../examples/snippets/voresource/voresource.py
            :language: python
            :start-after: curation-model-start
            :end-before: curation-model-end

    .. grid-item-card:: XML Output

        .. literalinclude:: ../../../../examples/snippets/voresource/voresource.py
            :language: xml
            :lines: 2-
            :start-after: curation-xml-start
            :end-before: curation-xml-end

Content
********

Represents the general content of a resource.

.. grid:: 2
    :gutter: 2

    .. grid-item-card:: Model

        .. literalinclude:: ../../../../examples/snippets/voresource/voresource.py
            :language: python
            :start-after: content-model-start
            :end-before: content-model-end

    .. grid-item-card:: XML Output

        .. literalinclude:: ../../../../examples/snippets/voresource/voresource.py
            :language: xml
            :lines: 2-
            :start-after: content-xml-start
            :end-before: content-xml-end

Interface
*********

Represents the interface of a resource, including the access URL, the interface type and the security method.

.. note::
    The ``Interface`` type is a description of an abstract interface, and must be subclassed, e.g. ``WebService`` or ``WebBrowser``.
    This is done generally by setting the ``xsi:type`` attribute of the interface to the subclass name.


.. grid:: 2
    :gutter: 2

    .. grid-item-card:: Model

        .. literalinclude:: ../../../../examples/snippets/voresource/voresource.py
            :language: python
            :start-after: interface-model-start
            :end-before: interface-model-end

    .. grid-item-card:: XML Output

        .. literalinclude:: ../../../../examples/snippets/voresource/voresource.py
            :language: xml
            :lines: 2-
            :start-after: interface-xml-start
            :end-before: interface-xml-end

WebBrowser and WebService
*************************

Examples of subclasses of ``Interface``. They represent a form-based interface and a web service described by a WSDL, respectively.

Their XML output is functionally identical to the ``Interface`` example above, except for the ``xsi:type`` attribute set to ``vr:WebBrowser`` or ``vr:WebService``.

Resource
********

Any entity or component of a VO application describable by an IVOA identifier.

.. grid:: 2
    :gutter: 2

    .. grid-item-card:: Model

        .. literalinclude:: ../../../../examples/snippets/voresource/voresource.py
            :language: python
            :start-after: resource-model-start
            :end-before: resource-model-end

    .. grid-item-card:: XML Output

        .. literalinclude:: ../../../../examples/snippets/voresource/voresource.py
            :language: xml
            :lines: 2-
            :start-after: resource-xml-start
            :end-before: resource-xml-end

Organisation
************

A named group of persons participating in IVOA applications.

.. grid:: 2
    :gutter: 2

    .. grid-item-card:: Model

        .. literalinclude:: ../../../../examples/snippets/voresource/voresource.py
            :language: python
            :start-after: organisation-model-start
            :end-before: organisation-model-end

    .. grid-item-card:: XML Output

        .. literalinclude:: ../../../../examples/snippets/voresource/voresource.py
            :language: xml
            :lines: 2-
            :start-after: organisation-xml-start
            :end-before: organisation-xml-end

Capability
**********

A description of what a service does, and how to use it.

.. grid:: 2
    :gutter: 2

    .. grid-item-card:: Model

        .. literalinclude:: ../../../../examples/snippets/voresource/voresource.py
            :language: python
            :start-after: capability-model-start
            :end-before: capability-model-end

    .. grid-item-card:: XML Output

        .. literalinclude:: ../../../../examples/snippets/voresource/voresource.py
            :language: xml
            :lines: 2-
            :start-after: capability-xml-start
            :end-before: capability-xml-end

Service
********

A resource that can be invoked by a client.

.. grid:: 2
    :gutter: 2

    .. grid-item-card:: Model

        .. literalinclude:: ../../../../examples/snippets/voresource/voresource.py
            :language: python
            :start-after: service-model-start
            :end-before: service-model-end

    .. grid-item-card:: XML Output

        .. literalinclude:: ../../../../examples/snippets/voresource/voresource.py
            :language: xml
            :lines: 2-
            :start-after: service-xml-start
            :end-before: service-xml-end

.. _uws:

UWS (Universal Worker Service)
------------------------------

UWS is a protocol for describing and executing jobs on remote services. vo-models currently provides support for the `UWS 1.1 version <https://www.ivoa.net/documents/UWS/20161024/REC-UWS-1.1-20161024.html>`_ of the protocol.

Models for UWS are provided in the ``vo_models.uws`` package. Supported models are:

Models
^^^^^^

errorSummary
*****************

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
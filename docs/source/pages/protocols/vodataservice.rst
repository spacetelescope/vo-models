.. _vodataservice:

VODataService
------------

VODataService is an IVOA XML encoding standard for data collections and services that access them. It is an extension of the VOResource standard.

`vo-models` currently supports the following VODataService v1.2 elements:

Models
^^^^^^

FKColumn
********

Represents a single foreign key column.

.. grid:: 2
    :gutter: 2

    .. grid-item-card:: Model

        .. literalinclude:: ../../../../examples/snippets/vodataservice/vodataservice.py
            :language: python
            :start-after: FKColumn-model-start
            :end-before: FKColumn-model-end

    .. grid-item-card:: XML Output

        .. literalinclude:: ../../../../examples/snippets/vodataservice/vodataservice.py
            :language: xml
            :lines: 2-
            :start-after: FKColumn-xml-start
            :end-before: FKColumn-xml-end

ForeignKey
**********

Represents one or more foreign key columns.

.. grid:: 2
    :gutter: 2

    .. grid-item-card:: Model

        .. literalinclude:: ../../../../examples/snippets/vodataservice/vodataservice.py
            :language: python
            :start-after: ForeignKey-model-start
            :end-before: ForeignKey-model-end

    .. grid-item-card:: XML Output

        .. literalinclude:: ../../../../examples/snippets/vodataservice/vodataservice.py
            :language: xml
            :lines: 2-
            :start-after: ForeignKey-xml-start
            :end-before: ForeignKey-xml-end

DataType
********

A simple element containing a column's datatype.

.. grid:: 2
    :gutter: 2

    .. grid-item-card:: Model

        .. literalinclude:: ../../../../examples/snippets/vodataservice/vodataservice.py
            :language: python
            :start-after: DataType-model-start
            :end-before: DataType-model-end

    .. grid-item-card:: XML Output

        .. literalinclude:: ../../../../examples/snippets/vodataservice/vodataservice.py
            :language: xml
            :lines: 2-
            :start-after: DataType-xml-start
            :end-before: DataType-xml-end

TableParam
**********

A description of a table parameter (a column within the table) with a fixed datatype.

.. grid:: 2
    :gutter: 2

    .. grid-item-card:: Model

        .. literalinclude:: ../../../../examples/snippets/vodataservice/vodataservice.py
            :language: python
            :start-after: TableParam-model-start
            :end-before: TableParam-model-end

    .. grid-item-card:: XML Output

        .. literalinclude:: ../../../../examples/snippets/vodataservice/vodataservice.py
            :language: xml
            :lines: 2-
            :start-after: TableParam-xml-start
            :end-before: TableParam-xml-end

Table
*****

A single table element.

.. grid:: 2
    :gutter: 2

    .. grid-item-card:: Model

        .. literalinclude:: ../../../../examples/snippets/vodataservice/vodataservice.py
            :language: python
            :start-after: Table-model-start
            :end-before: Table-model-end

    .. grid-item-card:: XML Output

        .. literalinclude:: ../../../../examples/snippets/vodataservice/vodataservice.py
            :language: xml
            :lines: 2-
            :start-after: Table-xml-start
            :end-before: Table-xml-end

TableSchema
***********

Represents a description of a logically related group of tables.

.. grid:: 2
    :gutter: 2

    .. grid-item-card:: Model

        .. literalinclude:: ../../../../examples/snippets/vodataservice/vodataservice.py
            :language: python
            :start-after: TableSchema-model-start
            :end-before: TableSchema-model-end

    .. grid-item-card:: XML Output

        .. literalinclude:: ../../../../examples/snippets/vodataservice/vodataservice.py
            :language: xml
            :lines: 2-
            :start-after: TableSchema-xml-start
            :end-before: TableSchema-xml-end


TableSet
********

Represents a collection of tables that are part of a single resource.

.. grid:: 2
    :gutter: 2

    .. grid-item-card:: Model

        .. literalinclude:: ../../../../examples/snippets/vodataservice/vodataservice.py
            :language: python
            :start-after: TableSet-model-start
            :end-before: TableSet-model-end

    .. grid-item-card:: XML Output

        .. literalinclude:: ../../../../examples/snippets/vodataservice/vodataservice.py
            :language: xml
            :lines: 2-
            :start-after: TableSet-xml-start
            :end-before: TableSet-xml-end
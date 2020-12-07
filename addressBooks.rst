============
addressBooks
============

The address books API, also including the :doc:`contacts` and :doc:`mailingLists` namespaces, first appeared in Thunderbird 64.

The `Address Books`__ sample extension uses this API.

__ https://github.com/thundernest/sample-extensions/tree/master/addressBooks

Permissions
===========

- addressBooks "Read and modify your address books and contacts"

.. note::

  The permission ``addressBooks`` is required to use ``addressBooks``.

Functions
=========

.. _addressBooks.openUI:

openUI()
--------

Opens the address book user interface.

.. _addressBooks.closeUI:

closeUI()
---------

Closes the address book user interface.

.. _addressBooks.list:

list([complete])
----------------

Gets a list of the user's address books, optionally including all contacts and mailing lists.

- [``complete``] (boolean) If set to true, results will include contacts and mailing lists for each address book.

Returns a `Promise`_ fulfilled with:

- array of :ref:`addressBooks.AddressBookNode`

.. _addressBooks.get:

get(id, [complete])
-------------------

Gets a single address book, optionally including all contacts and mailing lists.

- ``id`` (string)
- [``complete``] (boolean) If set to true, results will include contacts and mailing lists for this address book.

Returns a `Promise`_ fulfilled with:

- :ref:`addressBooks.AddressBookNode`

.. _addressBooks.create:

create(properties)
------------------

Creates a new, empty address book.

- ``properties`` (object)

  - ``name`` (string)

Returns a `Promise`_ fulfilled with:

- string The ID of the new address book.

.. _addressBooks.update:

update(id, properties)
----------------------

Renames an address book.

- ``id`` (string)
- ``properties`` (object)

  - ``name`` (string)

.. _addressBooks.delete:

delete(id)
----------

Removes an address book, and all associated contacts and mailing lists.

- ``id`` (string)

.. _Promise: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise

Events
======

.. _addressBooks.onCreated:

onCreated(node)
---------------

Fired when an address book is created.

- ``node`` (:ref:`addressBooks.AddressBookNode`)

.. _addressBooks.onUpdated:

onUpdated(node)
---------------

Fired when an address book is renamed.

- ``node`` (:ref:`addressBooks.AddressBookNode`)

.. _addressBooks.onDeleted:

onDeleted(id)
-------------

Fired when an addressBook is deleted.

- ``id`` (string)

Types
=====

.. _addressBooks.AddressBookNode:

AddressBookNode
---------------

A node representing an address book.

object:

- ``id`` (string) The unique identifier for the node. IDs are unique within the current profile, and they remain valid even after the program is restarted.
- ``name`` (string)
- ``type`` (:ref:`addressBooks.NodeType`) Always set to ``addressBook``.
- [``contacts``] (array of :ref:`contacts.ContactNode`) A list of contacts held by this node's address book or mailing list.
- [``mailingLists``] (array of :ref:`mailingLists.MailingListNode`) A list of mailingLists in this node's address book.
- [``parentId``] (string) The ``id`` of the parent object.
- [``readOnly``] (boolean) Indicates if the object is read-only. Currently this returns false in all cases, as read-only address books are ignored by the API.

.. _addressBooks.NodeType:

NodeType
--------

Indicates the type of a Node, which can be one of ``addressBook``, ``contact``, or ``mailingList``.

`string <enum_NodeType_17_>`_

.. _enum_NodeType_17:

Values for NodeType:

- ``addressBook``
- ``contact``
- ``mailingList``

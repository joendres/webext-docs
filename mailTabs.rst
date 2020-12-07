========
mailTabs
========

The messages API first appeared in Thunderbird 66 (see `bug 1499617`__).

__ https://bugzilla.mozilla.org/show_bug.cgi?id=1499617

The `Filter`__  and `Layout`__ sample extensions use this API.

__ https://github.com/thundernest/sample-extensions/tree/master/filter
__ https://github.com/thundernest/sample-extensions/tree/master/layout

Functions
=========

.. _mailTabs.query:

query(queryInfo)
----------------

Gets all mail tabs that have the specified properties, or all mail tabs if no properties are specified.

- ``queryInfo`` (object)

  - [``active``] (boolean) Whether the tabs are active in their windows.
  - [``currentWindow``] (boolean) Whether the tabs are in the current window.
  - [``lastFocusedWindow``] (boolean) Whether the tabs are in the last focused window.
  - [``windowId``] (integer) The ID of the parent window, or :ref:`windows.WINDOW_ID_CURRENT` for the current window.

Returns a `Promise`_ fulfilled with:

- array of :ref:`mailTabs.MailTab`

.. _mailTabs.update:

update([tabId], updateProperties)
---------------------------------

Modifies the properties of a mail tab. Properties that are not specified in ``updateProperties`` are not modified.

- [``tabId``] (integer) Defaults to the active tab of the current window.
- ``updateProperties`` (object)

  - [``displayedFolder``] (:ref:`folders.MailFolder`) Sets the folder displayed in the tab. The extension must have an accounts permission to do this.
  - [``folderPaneVisible``] (boolean) Shows or hides the folder pane.
  - [``layout``] (`string <enum_layout_9_>`_) Sets the arrangement of the folder pane, message list pane, and message display pane. Note that setting this applies it to all mail tabs.
  - [``messagePaneVisible``] (boolean) Shows or hides the message display pane.
  - [``sortOrder``] (`string <enum_sortOrder_11_>`_) Sorts the list of messages. ``sortType`` must also be given.
  - [``sortType``] (`string <enum_sortType_12_>`_) Sorts the list of messages. ``sortOrder`` must also be given.

.. _enum_layout_9:

Values for layout:

- ``standard``
- ``wide``
- ``vertical``

.. _enum_sortOrder_11:

Values for sortOrder:

- ``none``
- ``ascending``
- ``descending``

.. _enum_sortType_12:

Values for sortType:

- ``none``
- ``date``
- ``subject``
- ``author``
- ``id``
- ``thread``
- ``priority``
- ``status``
- ``size``
- ``flagged``
- ``unread``
- ``recipient``
- ``location``
- ``tags``
- ``junkStatus``
- ``attachments``
- ``account``
- ``custom``
- ``received``
- ``correspondent``

.. _mailTabs.getSelectedMessages:

getSelectedMessages([tabId])
----------------------------

Lists the selected messages in the current folder. A messages permission is required to do this.

- [``tabId``] (integer) Defaults to the active tab of the current window.

Returns a `Promise`_ fulfilled with:

- :ref:`messages.MessageList`

.. note::

  The permission ``messagesRead`` is required to use ``getSelectedMessages``.

.. _mailTabs.setQuickFilter:

setQuickFilter([tabId], properties)
-----------------------------------

Sets the Quick Filter user interface based on the options specified.

- [``tabId``] (integer) Defaults to the active tab of the current window.
- ``properties`` (object)

  - [``attachment``] (boolean) Shows only messages with attachments.
  - [``contact``] (boolean) Shows only messages from people in the address book.
  - [``flagged``] (boolean) Shows only flagged messages.
  - [``show``] (boolean) Shows or hides the Quick Filter bar.
  - [``tags``] (boolean or :ref:`messages.TagsDetail`) Shows only messages with tags on them.
  - [``text``] (:ref:`mailTabs.QuickFilterTextDetail`) Shows only messages matching the supplied text.
  - [``unread``] (boolean) Shows only unread messages.

.. _Promise: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise

Events
======

.. _mailTabs.onDisplayedFolderChanged:

onDisplayedFolderChanged(tab, displayedFolder)
----------------------------------------------

Fired when the displayed folder changes in any mail tab.

- ``tab`` (:ref:`tabs.Tab`) *Changed in Thunderbird 76, previously just the tab's ID*
- ``displayedFolder`` (:ref:`folders.MailFolder`)

.. note::

  The permission ``accountsRead`` is required to use ``onDisplayedFolderChanged``.

.. _mailTabs.onSelectedMessagesChanged:

onSelectedMessagesChanged(tab, selectedMessages)
------------------------------------------------

Fired when the selected messages change in any mail tab.

- ``tab`` (:ref:`tabs.Tab`) *Changed in Thunderbird 76, previously just the tab's ID*
- ``selectedMessages`` (:ref:`messages.MessageList`)

.. note::

  The permission ``messagesRead`` is required to use ``onSelectedMessagesChanged``.

Types
=====

.. _mailTabs.MailTab:

MailTab
-------

object:

- ``active`` (boolean)
- ``displayedFolder`` (:ref:`folders.MailFolder`) The ``accountsRead`` permission is required.
- ``folderPaneVisible`` (boolean)
- ``id`` (integer)
- ``layout`` (`string <enum_layout_28_>`_)
- ``messagePaneVisible`` (boolean)
- ``sortOrder`` (`string <enum_sortOrder_30_>`_)
- ``sortType`` (`string <enum_sortType_31_>`_)
- ``windowId`` (integer)

.. _enum_layout_28:

Values for layout:

- ``standard``
- ``wide``
- ``vertical``

.. _enum_sortOrder_30:

Values for sortOrder:

- ``none``
- ``ascending``
- ``descending``

.. _enum_sortType_31:

Values for sortType:

- ``none``
- ``date``
- ``subject``
- ``author``
- ``id``
- ``thread``
- ``priority``
- ``status``
- ``size``
- ``flagged``
- ``unread``
- ``recipient``
- ``location``
- ``tags``
- ``junkStatus``
- ``attachments``
- ``account``
- ``custom``
- ``received``
- ``correspondent``

.. _mailTabs.QuickFilterTextDetail:

QuickFilterTextDetail
---------------------

object:

- ``text`` (string) String to match against the ``recipients``, ``author``, ``subject``, or ``body``.
- [``author``] (boolean) Shows messages where ``text`` matches the author.
- [``body``] (boolean) Shows messages where ``text`` matches the message body.
- [``recipients``] (boolean) Shows messages where ``text`` matches the recipients.
- [``subject``] (boolean) Shows messages where ``text`` matches the subject.

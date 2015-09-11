Changelog
=========

3.0.1 (2015-09-11)
------------------

* Turning an ``assert`` into a raised error
* Adding unit tests

3.0.0 (2015-06-16)
------------------

* Renaming the product ``gs.site.member.base``

2.5.0 (2015-06-15)
------------------

* Following `gs.group.member.leave`_ to its new home

.. _GitHub: https://github.com/groupserver/gs.site.member

2.4.0 (2014-10-10)
------------------

* Pointing at GitHub_ as the primary code repository
* Naming the reStructuredText files as such

.. _GitHub: https://github.com/groupserver/gs.site.member.base

2.3.3 (2014-09-04)
------------------

* Fixing a ``UnicodeDecodeError``

2.3.2 (2014-03-26)
------------------

* Using the correct marker interface from ``gs.group.base``
* Switching to Unicode literals

2.3.1 (2013-09-23)
------------------

* PEP-8 and metadata fixes

2.3.0 (2012-09-27)
------------------

* Performance improvement to the ``SiteMembers`` class

2.2.1 (2012-06-22)
------------------

* SQLAlchemy update

2.2.0 (2012-04-13)
------------------

* Cascade the new-group-member into a new-site-member event
* Case the group-leave event into a site-leave event

2.1.0 (2012-03-08)
------------------

* Adding the ``SiteMember`` vocabulary

2.0.1 (2012-02-29)
------------------

* Adding a ``try… except`` block for the group-leave events.

2.0.0 (2012-02-24)
------------------

* Initial version, renaming the product from ``gs.sitemember``

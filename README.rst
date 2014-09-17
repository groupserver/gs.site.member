Introduction
============

In GroupServer, each group belongs to a site. Likewise, each 
group-member belongs to a related site-member user-group. This product
provides systems for `site member user-group management`_, a `site
member vocabulary`_, and the `site memberships content provider`_.

Site Member User-Group Management
=================================

When people join a group an event is raised [#JoinEvent]_. This product
provides a *subscriber* for that event, which adds the new group-member
to the site-member user-group if (and only if) he or she is not already
a member of the site-member user-group. When there is a new site member
this product *in turn* raises an event with the interface
``gs.site.member.event.IGSJoinSiteEvent``.

Conversely, when someone leaves a group [#LeaveEvent]_ this product
catches the event and checks if the person is still a member of a group
on this site. If the person is no longer a member of any group then
he or she is removed from the site-member user-group and this product
raises a ``gs.site.member.event.IGSLeaveSiteEvent``.

Site Member Vocabulary
======================

The named vocabulary ``groupserver.SiteMembers`` provides a list of the
members of a site. Each member is represented by a token of 
``(user-ID, user-ID, user-name)``.

Site Memberships Content Provider
=================================

The site memberships content provider ``groupserver.SiteMemberships``
creates a list of sites that a user is a member of. This is used by
the Profile page to allow people to change between sites easily.

..  [#JoinEvent] The event raised when someone **joins** a group has the
    interface ``gs.group.member.join.event.IGSJoinGroupEvent``.
..  [#LeaveEvent] The event raised when someone **leaves** a group has 
    the interface ``gs.group.member.leave.event.IGSLeaveGroupEvent``.


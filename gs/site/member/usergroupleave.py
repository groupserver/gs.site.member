# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright © 2013, 2014 OnlineGroups.net and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
from __future__ import absolute_import, unicode_literals
from logging import getLogger
SUBSYSTEM = 'gs.site.member'
log = getLogger(SUBSYSTEM)
from zope.event import notify
from gs.core import to_ascii
from gs.group.member.base.utils import user_member_of_site
from gs.groups.interfaces import IGSGroupsInfo
from Products.GSGroupMember.groupmembership import member_id
from .audit import SiteMemberAuditor, LEAVE_SITE, LEAVE_SITE_MEMBER
from .event import GSLeaveSiteEvent


def member_removed(context, event):
    groupInfo = event.groupInfo
    userInfo = event.memberInfo
    siteInfo = groupInfo.siteInfo
    auditor = SiteMemberAuditor(context, userInfo, siteInfo)

    if user_member_of_group_on_site(context, userInfo):
        auditor.info(LEAVE_SITE_MEMBER)
    else:
        site_root = context.site_root()
        acl_users = getattr(site_root, 'acl_users')
        if not acl_users:
            raise ValueError('ACL Users not found in site_root')
        memberGroupId = member_id(siteInfo.id)
        try:
            acl_users.delGroupsFromUser([memberGroupId], userInfo.id)
        except ValueError as ve:
            m = 'Tried to remove %s (%s) from the site %s (%s) but '\
                'got a ValueError:\n%s' %\
                (userInfo.name, userInfo.id, siteInfo.name, memberGroupId, ve)
            msg = to_ascii(m)
            log.warning(msg)
        else:
            auditor.info(LEAVE_SITE)
            notify(GSLeaveSiteEvent(context, siteInfo, userInfo))
        assert not(user_member_of_site(userInfo, siteInfo.siteObj))


def user_member_of_group_on_site(context, userInfo):
    groupsInfo = IGSGroupsInfo(context)
    u = userInfo.user
    groups = groupsInfo.get_member_groups_for_user(u, u)
    retval = bool(groups)
    return retval

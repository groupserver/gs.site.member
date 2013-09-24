# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright © 2013 OnlineGroups.net and Contributors.
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
from __future__ import absolute_import
from zope.event import notify
from Products.GSGroupMember.groupmembership import member_id
from gs.group.member.base.utils import user_member_of_site
from .audit import SiteMemberAuditor, JOIN_SITE, JOIN_SITE_MEMBER
from .event import GSJoinSiteEvent


def member_added(context, event):
    groupInfo = event.groupInfo
    userInfo = event.memberInfo
    siteInfo = groupInfo.siteInfo
    auditor = SiteMemberAuditor(context, userInfo, siteInfo)

    if user_member_of_site(userInfo, siteInfo.siteObj):
        auditor.info(JOIN_SITE_MEMBER)
    else:
        site_root = context.site_root()
        acl_users = getattr(site_root, 'acl_users')
        assert acl_users, 'ACL Users not found in site_root'

        groupNames = acl_users.getGroupNames()
        siteInfo = groupInfo.siteInfo
        memberGroupId = member_id(siteInfo.id)
        assert memberGroupId in groupNames, \
            '%s not in %s' % (memberGroupId, groupNames)
        acl_users.addGroupsToUser([memberGroupId], userInfo.id)
        auditor.info(JOIN_SITE)
        notify(GSJoinSiteEvent(context, siteInfo, userInfo))
    assert user_member_of_site(userInfo, siteInfo.siteObj)

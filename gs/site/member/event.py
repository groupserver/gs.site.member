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
from __future__ import unicode_literals
from zope.component.interfaces import ObjectEvent, IObjectEvent
from zope.interface import Attribute, implements


class IGSJoinSiteEvent(IObjectEvent):
    """ An event issued after someone has joined a site."""
    siteInfo = Attribute('The site that is being joined')
    memberInfo = Attribute('The new site member')


class IGSLeaveSiteEvent(IObjectEvent):
    """ An event issued after someone has left a site."""
    siteInfo = Attribute('The site that is being left')
    memberInfo = Attribute('The old site member')


class GSJoinSiteEvent(ObjectEvent):
    implements(IGSJoinSiteEvent)

    def __init__(self, context, siteInfo, memberInfo):
        ObjectEvent.__init__(self, context)
        self.siteInfo = siteInfo
        self.memberInfo = memberInfo


class GSLeaveSiteEvent(ObjectEvent):
    implements(IGSLeaveSiteEvent)

    def __init__(self, context, siteInfo, memberInfo):
        ObjectEvent.__init__(self, context)
        self.siteInfo = siteInfo
        self.memberInfo = memberInfo

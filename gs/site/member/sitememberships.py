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
from zope.interface import implements, Interface
from zope.contentprovider.interfaces import UpdateNotCalled
from zope.component import adapts, createObject
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from zope.pagetemplate.pagetemplatefile import PageTemplateFile
from Products.CustomUserFolder.interfaces import IGSUserInfo
from .interfaces import IGSSiteMembershipsContentProvider
from .sitemembershipvocabulary import SiteMembership


class SiteMembershipsContentProvider(object):
    implements(IGSSiteMembershipsContentProvider)
    adapts(Interface, IDefaultBrowserLayer, Interface)

    def __init__(self, user, request, view):
        self.__parent__ = self.view = view
        self.__updated = False

        self.context = user
        self.request = request
        self.__properties = None

    def update(self):
        self.__updated = True

        self.currentSite = createObject('groupserver.SiteInfo',
          self.context)
        self.userInfo = IGSUserInfo(self.context)
        self.siteMemberships = SiteMembership(self.context)

    def render(self):
        if not self.__updated:
            raise UpdateNotCalled
        pageTemplate = PageTemplateFile(self.pageTemplateFileName)
        retval = pageTemplate(view=self,
                              currentSite=self.currentSite,
                              siteMemberships=self.siteMemberships)
        return retval

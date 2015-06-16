# -*- coding: utf-8 -*-
############################################################################
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
############################################################################
from __future__ import unicode_literals
from zope.cachedescriptors.property import Lazy
from zope.component import createObject
from zope.interface import implements
from zope.interface.common.mapping import IEnumerableMapping
from zope.schema.vocabulary import SimpleTerm
from zope.schema.interfaces import (IVocabulary, IVocabularyTokenized)
from gs.core import to_unicode_or_bust
SITE_FOLDER_TYPES = ('Folder', 'Folder (Ordered)')


class SiteMembership(object):
    implements(IVocabulary, IVocabularyTokenized)
    __used_for__ = IEnumerableMapping

    def __init__(self, user):
        self.context = user
        self.content = self.context.Content

    def __iter__(self):
        """See zope.schema.interfaces.IIterableVocabulary"""
        for siteId in self.siteIds:
            retval = self.get_site_term(siteId)
            yield retval

    def __len__(self):
        """See zope.schema.interfaces.IIterableVocabulary"""
        return len(self.siteIds)

    def __contains__(self, value):
        """See zope.schema.interfaces.IBaseVocabulary"""
        retval = value in self.siteIds
        assert type(retval) == bool
        return retval

    def getQuery(self):
        """See zope.schema.interfaces.IBaseVocabulary"""
        return None

    def getTerm(self, value):
        """See zope.schema.interfaces.IBaseVocabulary"""
        return self.getTermByToken(value)

    def get_site_term(self, siteId):
        site = getattr(self.content, siteId)
        siteInfo = createObject('groupserver.SiteInfo', site)
        retval = SimpleTerm(siteInfo, siteInfo.id,
                            to_unicode_or_bust(siteInfo.name))
        return retval

    def getTermByToken(self, token):
        """See zope.schema.interfaces.IVocabularyTokenized"""
        if token in self:
            return self.get_site_term(token)
        raise LookupError(token)

    @Lazy
    def siteIds(self):
        allSites = self.content.objectIds(SITE_FOLDER_TYPES)
        memberships = ['_'.join(m.split('_')[:-1])
                       for m in self.context.getGroups()]
        retval = [m for m in memberships if m in allSites]
        retval.sort()
        return retval

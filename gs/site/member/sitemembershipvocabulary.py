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
from operator import attrgetter
from zope.cachedescriptors.property import Lazy
from zope.component import createObject
from zope.interface import implements, providedBy
from zope.interface.common.mapping import IEnumerableMapping
from zope.schema.vocabulary import SimpleTerm
from zope.schema.interfaces import IVocabulary, IVocabularyTokenized, \
    ITitledTokenizedTerm

SITE_FOLDER_TYPES = ('Folder', 'Folder (Ordered)')


class SiteMembership(object):
    implements(IVocabulary, IVocabularyTokenized)
    __used_for__ = IEnumerableMapping

    def __init__(self, user):
        self.context = user

    def __iter__(self):
        """See zope.schema.interfaces.IIterableVocabulary"""
        retval = [SimpleTerm(s, s.id, s.name)
                  for s in self.sites]
        retval.sort(key=attrgetter('title'))
        return iter(retval)

    def __len__(self):
        """See zope.schema.interfaces.IIterableVocabulary"""
        return len(self.sites)

    def __contains__(self, value):
        """See zope.schema.interfaces.IBaseVocabulary"""
        retval = value in [s.id for s in self.sites]
        assert type(retval) == bool
        return retval

    def getQuery(self):
        """See zope.schema.interfaces.IBaseVocabulary"""
        return None

    def getTerm(self, value):
        """See zope.schema.interfaces.IBaseVocabulary"""
        return self.getTermByToken(value)

    def getTermByToken(self, token):
        """See zope.schema.interfaces.IVocabularyTokenized"""
        for s in self.sites:
            if s.id == token:
                retval = SimpleTerm(s, s.id, s.name)
                assert retval
                assert ITitledTokenizedTerm in providedBy(retval)
                assert retval.token == retval.value
                return retval
        raise LookupError(token)

    @Lazy
    def sites(self):
        assert self.context
        content = self.context.Content
        memberships = ['_'.join(m.split('_')[:-1])
                       for m in self.context.getGroups()]
        siteMembershipIds = [m for m in memberships
                            if m in content.objectIds(SITE_FOLDER_TYPES)]
        retval = []
        for s in siteMembershipIds:
            site = getattr(content, s)
            siteInfo = createObject('groupserver.SiteInfo', site)
            retval.append(siteInfo)
        assert type(retval) == list
        return retval

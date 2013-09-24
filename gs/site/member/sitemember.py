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
from zope.cachedescriptors.property import Lazy
from zope.interface import implements, providedBy
from zope.component import createObject
from zope.schema.vocabulary import SimpleTerm
from zope.schema.interfaces import IVocabulary, \
  IVocabularyTokenized, ITitledTokenizedTerm
from zope.interface.common.mapping import IEnumerableMapping
from gs.group.member.base.utils import member_id


class SiteMembers(object):
    implements(IVocabulary, IVocabularyTokenized)
    __used_for__ = IEnumerableMapping

    def __init__(self, context):
        self.context = context
        assert self.context, 'There is no context.'

    @Lazy
    def siteInfo(self):
        retval = createObject('groupserver.SiteInfo', self.context)
        return retval

    @Lazy
    def groupsInfo(self):
        retval = createObject('groupserver.GroupsInfo', self.context)
        return retval

    def __iter__(self):
        """See zope.schema.interfaces.IIterableVocabulary"""
        for uid in self.memberIds:
            m = createObject('groupserver.UserFromId', self.context, uid)
            retval = SimpleTerm(m.id, m.id, m.name)
            assert ITitledTokenizedTerm in providedBy(retval)
            assert retval.token == retval.value
            assert retval.token == uid
            yield retval

    def __len__(self):
        """See zope.schema.interfaces.IIterableVocabulary"""
        return len(self.memberIds)

    def __contains__(self, value):
        """See zope.schema.interfaces.IBaseVocabulary"""
        retval = value in self.memberIds
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
        if token in self:
            m = createObject('groupserver.UserFromId', self.context, token)
            retval = SimpleTerm(m.id, m.id, m.name)
        else:
            raise LookupError(token)
        assert ITitledTokenizedTerm in providedBy(retval)
        assert retval.token == retval.value
        assert retval.token == token
        return retval

    @Lazy
    def acl_users(self):
        sr = self.context.site_root()
        assert sr, 'No site root'
        retval = sr.acl_users
        assert retval, 'No ACL Users'
        return retval

    @Lazy
    def memberIds(self):
        smg = self.acl_users.getGroupById(member_id(self.siteInfo.id))
        assert smg, u'Could not get site-member group for %s (%s)' % \
            (self.siteInfo.name, self.siteInfo.id)
        retval = list(smg.getUsers())
        assert type(retval) == list
        return retval

    @Lazy
    def members(self):
        assert self.context
        retval = [createObject('groupserver.UserFromId', self.context, uid)
                   for uid in self.memberIds if uid]
        retval = [u for u in retval
                    if not(u.anonymous)]
        assert type(retval) == list
        return retval

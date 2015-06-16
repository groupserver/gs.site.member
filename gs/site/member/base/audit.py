# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright © 2012, 2013, 2014 OnlineGroups.net and Contributors.
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
SUBSYSTEM = 'gs.site.member'
from logging import getLogger
log = getLogger(SUBSYSTEM)
from pytz import UTC
from datetime import datetime
from zope.component.interfaces import IFactory
from zope.interface import implements, implementedBy
from Products.GSAuditTrail import IAuditEvent, BasicAuditEvent, \
    AuditQuery, event_id_from_data
from Products.XWFCore.XWFUtils import munge_date
from gs.core import to_ascii
UNKNOWN = '0'
JOIN_SITE = '1'
JOIN_SITE_MEMBER = '2'
LEAVE_SITE = '3'
LEAVE_SITE_MEMBER = '4'


class AuditEventFactory(object):
    implements(IFactory)

    title = 'Site Member Audit-Event Factory'
    description = 'Creates a GroupServer audit event for changing the ' \
        'site membership.'

    def __call__(self, context, event_id, code, date,
        userInfo, instanceUserInfo, siteInfo, groupInfo=None,
        instanceDatum='', supplementaryDatum='', subsystem=''):
        if code == JOIN_SITE:
            event = JoinEvent(context, event_id, date, userInfo,
                        siteInfo)
        elif code == JOIN_SITE_MEMBER:
            event = JoinMemberEvent(context, event_id, date, userInfo,
                        siteInfo)
        elif code == LEAVE_SITE:
            event = LeaveEvent(context, event_id, date, userInfo,
                        siteInfo)
        elif code == LEAVE_SITE_MEMBER:
            event = LeaveMemberEvent(context, event_id, date, userInfo,
                        siteInfo)
        else:
            event = BasicAuditEvent(context, event_id, UNKNOWN, date,
                      userInfo, instanceUserInfo, siteInfo, groupInfo,
                      instanceDatum, supplementaryDatum, SUBSYSTEM)
        assert event
        return event

    def getInterfaces(self):
        return implementedBy(BasicAuditEvent)


class JoinEvent(BasicAuditEvent):  # JOIN_SITE = '1'
    ''' An audit-trail event representing a member joining a site.'''
    implements(IAuditEvent)

    def __init__(self, context, id, d, userInfo, siteInfo):
        BasicAuditEvent.__init__(self, context, id, JOIN_SITE, d,
            userInfo, userInfo, siteInfo, None, None, None, SUBSYSTEM)

    def __unicode__(self):
        retval = '%s (%s) joined the site "%s" (%s).' % \
            (self.userInfo.name, self.userInfo.id,
             self.siteInfo.name, self.siteInfo.id)
        return retval

    def __str__(self):
        retval = to_ascii(unicode(self))
        return retval

    @property
    def xhtml(self):
        cssClass = 'audit-event gs-site-member-%s' % self.code
        retval = '<span class="%s">Joined the site <cite>%s</cite>.' %\
                    (cssClass, self.siteInfo.name)
        retval = '%s (%s)' % \
            (retval, munge_date(self.context, self.date))
        return retval


# JOIN_SITE_MEMBER  = '2'
class JoinMemberEvent(BasicAuditEvent):
    ''' An audit-trail event representing a member not joining a site.'''
    implements(IAuditEvent)

    def __init__(self, context, id, d, userInfo, siteInfo):
        BasicAuditEvent.__init__(self, context, id, JOIN_SITE_MEMBER, d,
            userInfo, userInfo, siteInfo, None, None, None, SUBSYSTEM)

    def __unicode__(self):
        retval = '%s (%s) did not join the site "%s" (%s), as the '\
            'member is already a member of the site!' % \
            (self.userInfo.name, self.userInfo.id,
             self.siteInfo.name, self.siteInfo.id)
        return retval

    def __str__(self):
        retval = to_ascii(unicode(self))
        return retval

    @property
    def xhtml(self):
        cssClass = 'audit-event gs-site-member-%s' % self.code
        retval = '<span class="%s">Already a member of the site '\
                    '<cite>%s</cite>.' %\
                    (cssClass, self.siteInfo.name)
        retval = '%s (%s)' % \
            (retval, munge_date(self.context, self.date))
        return retval


class LeaveEvent(BasicAuditEvent):  # LEAVE_SITE = '3'
    ''' An audit-trail event representing a member leaving a site.'''
    implements(IAuditEvent)

    def __init__(self, context, id, d, userInfo, siteInfo):
        BasicAuditEvent.__init__(self, context, id, LEAVE_SITE, d,
            userInfo, userInfo, siteInfo, None, None, None, SUBSYSTEM)

    def __unicode__(self):
        retval = '%s (%s) left the site "%s" (%s).' % \
            (self.userInfo.name, self.userInfo.id,
             self.siteInfo.name, self.siteInfo.id)
        return retval

    def __str__(self):
        retval = to_ascii(unicode(self))
        return retval

    @property
    def xhtml(self):
        cssClass = 'audit-event gs-site-member-%s' % self.code
        retval = '<span class="%s">Left the site <cite>%s</cite>.' %\
                    (cssClass, self.siteInfo.name)
        retval = '%s (%s)' % \
            (retval, munge_date(self.context, self.date))
        return retval


class LeaveMemberEvent(BasicAuditEvent):  # LEAVE_SITE_MEMBER = '4'
    ''' An audit-trail event representing a member not leaving a site.'''
    implements(IAuditEvent)

    def __init__(self, context, id, d, userInfo, siteInfo):
        BasicAuditEvent.__init__(self, context, id, LEAVE_SITE_MEMBER, d,
            userInfo, userInfo, siteInfo, None, None, None, SUBSYSTEM)

    def __unicode__(self):
        retval = '%s (%s) did not leave the site "%s" (%s), as the '\
            'member still belongs to a group on this site.' % \
            (self.userInfo.name, self.userInfo.id,
             self.siteInfo.name, self.siteInfo.id)
        return retval

    def __str__(self):
        retval = to_ascii(unicode(self))
        return retval

    @property
    def xhtml(self):
        cssClass = 'audit-event gs-site-member-%s' % self.code
        retval = '<span class="%s">Still a member of the site '\
            '<cite>%s</cite>.' % (cssClass, self.siteInfo.name)
        retval = '%s (%s)' % \
            (retval, munge_date(self.context, self.date))
        return retval


class SiteMemberAuditor(object):
    def __init__(self, context, userInfo, siteInfo):
        self.context = context
        self.userInfo = userInfo
        self.siteInfo = siteInfo

        self.queries = AuditQuery()
        self.factory = AuditEventFactory()

    def info(self, code):
        d = datetime.now(UTC)
        eventId = event_id_from_data(self.userInfo, self.userInfo,
            self.siteInfo, code, '', str(d))

        e = self.factory(self.context, eventId, code, d,
                self.userInfo, None, self.siteInfo, None,
                '', None, SUBSYSTEM)

        self.queries.store(e)
        log.info(e)

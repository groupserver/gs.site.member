# coding=utf-8
from pytz import UTC
from datetime import datetime
from zope.component.interfaces import IFactory
from zope.interface import implements, implementedBy
from Products.GSAuditTrail import IAuditEvent, BasicAuditEvent, \
    AuditQuery, event_id_from_data
from Products.XWFCore.XWFUtils import munge_date

SUBSYSTEM = 'gs.site.member'
import logging
log = logging.getLogger(SUBSYSTEM) #@UndefinedVariable

UNKNOWN           = '0'
JOIN_SITE         = '1'
JOIN_SITE_MEMBER  = '2'
LEAVE_SITE        = '3'
LEAVE_SITE_MEMBER = '4'

class AuditEventFactory(object):
    implements(IFactory)

    title=u'Site Member Audit-Event Factory'
    description=u'Creates a GroupServer audit event for changing the '\
        u'site membership.'

    def __call__(self, context, event_id,  code, date,
        userInfo, instanceUserInfo,  siteInfo,  groupInfo=None,
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

# JOIN_SITE         = '1'
class JoinEvent(BasicAuditEvent):
    ''' An audit-trail event representing a member joining a site.'''
    implements(IAuditEvent)

    def __init__(self, context, id, d, userInfo, siteInfo):
        BasicAuditEvent.__init__(self, context, id,  JOIN_SITE, d, 
            userInfo, userInfo, siteInfo, None, None, None, SUBSYSTEM)
          
    def __str__(self):
        retval = u'%s (%s) joined the site "%s" (%s).' % \
            (self.userInfo.name, self.userInfo.id, 
             self.siteInfo.name, self.siteInfo.id)
        retval = retval.encode('ascii', 'ignore')
        return retval
    
    @property
    def xhtml(self):
        cssClass = u'audit-event gs-site-member-%s' % self.code
        retval = u'<span class="%s">Joined the site <cite>%s</cite>.' %\
                    (cssClass, self.siteInfo.name)
        retval = u'%s (%s)' % \
            (retval, munge_date(self.context, self.date))
        return retval

# JOIN_SITE_MEMBER  = '2'
class JoinMemberEvent(BasicAuditEvent):
    ''' An audit-trail event representing a member not joining a site.'''
    implements(IAuditEvent)

    def __init__(self, context, id, d, userInfo, siteInfo):
        BasicAuditEvent.__init__(self, context, id,  JOIN_SITE_MEMBER, d, 
            userInfo, userInfo, siteInfo, None, None, None, SUBSYSTEM)
          
    def __str__(self):
        retval = u'%s (%s) did not join the site "%s" (%s), as the '\
            u'member is already a member of the site!' % \
            (self.userInfo.name, self.userInfo.id, 
             self.siteInfo.name, self.siteInfo.id)
        retval = retval.encode('ascii', 'ignore')
        return retval
    
    @property
    def xhtml(self):
        cssClass = u'audit-event gs-site-member-%s' % self.code
        retval = u'<span class="%s">Already a member of the site '\
                    u'<cite>%s</cite>.' %\
                    (cssClass, self.siteInfo.name)
        retval = u'%s (%s)' % \
            (retval, munge_date(self.context, self.date))
        return retval

# LEAVE_SITE        = '3'
class LeaveEvent(BasicAuditEvent):
    ''' An audit-trail event representing a member leaving a site.'''
    implements(IAuditEvent)

    def __init__(self, context, id, d, userInfo, siteInfo):
        BasicAuditEvent.__init__(self, context, id,  LEAVE_SITE, d, 
            userInfo, userInfo, siteInfo, None, None, None, SUBSYSTEM)
          
    def __str__(self):
        retval = u'%s (%s) left the site "%s" (%s).' % \
            (self.userInfo.name, self.userInfo.id, 
             self.siteInfo.name, self.siteInfo.id)
        retval = retval.encode('ascii', 'ignore')
        return retval
    
    @property
    def xhtml(self):
        cssClass = u'audit-event gs-site-member-%s' % self.code
        retval = u'<span class="%s">Left the site <cite>%s</cite>.' %\
                    (cssClass, self.siteInfo.name)
        retval = u'%s (%s)' % \
            (retval, munge_date(self.context, self.date))
        return retval

# LEAVE_SITE_MEMBER = '4'
class LeaveMemberEvent(BasicAuditEvent):
    ''' An audit-trail event representing a member not leaving a site.'''
    implements(IAuditEvent)

    def __init__(self, context, id, d, userInfo, siteInfo):
        BasicAuditEvent.__init__(self, context, id,  LEAVE_SITE_MEMBER, d, 
            userInfo, userInfo, siteInfo, None, None, None, SUBSYSTEM)
          
    def __str__(self):
        retval = u'%s (%s) did not leave the site "%s" (%s), as the '\
            u'member still belongs to a group on this site.' % \
            (self.userInfo.name, self.userInfo.id, 
             self.siteInfo.name, self.siteInfo.id)
        retval = retval.encode('ascii', 'ignore')
        return retval
    
    @property
    def xhtml(self):
        cssClass = u'audit-event gs-site-member-%s' % self.code
        retval = u'<span class="%s">Still a member of the site '\
            u'<cite>%s</cite>.' % (cssClass, self.siteInfo.name)
        retval = u'%s (%s)' % \
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
          
        e = self.factory(self.context, eventId,  code, d, 
                self.userInfo,  None, self.siteInfo, None,
                '', None, SUBSYSTEM)
          
        self.queries.store(e)
        log.info(e)
 

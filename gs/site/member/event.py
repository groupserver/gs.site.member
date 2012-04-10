# coding=utf-8
from zope.component.interfaces import ObjectEvent, IObjectEvent
from zope.interface import Attribute, implements

class IGSJoinSiteEvent(IObjectEvent):
    """ An event issued after someone has joined a site."""
    siteInfo   = Attribute(u'The site that is being joined')
    memberInfo = Attribute(u'The new site member')

class IGSLeaveSiteEvent(IObjectEvent):
    """ An event issued after someone has left a site."""
    siteInfo   = Attribute(u'The site that is being left')
    memberInfo = Attribute(u'The old site member')

class GSJoinSiteEvent(ObjectEvent):
    implements(IGSJoinSiteEvent)
    
    def __init__(self, context, siteInfo, memberInfo):
        ObjectEvent.__init__(self, context)
        self.siteInfo   = groupInfo
        self.memberInfo = memberInfo

class GSLeaveSiteEvent(ObjectEvent):
    implements(IGSLeaveSiteEvent)
    
    def __init__(self, context, siteInfo, memberInfo):
        ObjectEvent.__init__(self, context)
        self.siteInfo   = groupInfo
        self.memberInfo = memberInfo


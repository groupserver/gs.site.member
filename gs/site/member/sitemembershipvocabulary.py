# coding=utf-8
from operator import attrgetter
from zope.interface import implements, providedBy
from zope.component import createObject
from zope.schema.vocabulary import SimpleTerm
from zope.schema.interfaces import IVocabulary,\
  IVocabularyTokenized, ITitledTokenizedTerm
from zope.interface.common.mapping import IEnumerableMapping 
import AccessControl

SITE_FOLDER_TYPES = ('Folder', 'Folder (Ordered)')

class SiteMembership(object):
    implements(IVocabulary, IVocabularyTokenized)
    __used_for__ = IEnumerableMapping

    def __init__(self, user):
        self.context = user
        self.__sites = None
       
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
                retval = SimpleTerm(s, s.id, g.name)
                assert retval
                assert ITitledTokenizedTerm in providedBy(retval)
                assert retval.token == retval.value
                return retval
        raise LookupError, token

    @property
    def sites(self):
        assert self.context
        if self.__sites == None:
            content = self.context.Content
            memberships = ['_'.join(m.split('_')[:-1])
                           for m in self.context.getGroups()]
            siteMembershipIds = [m for m in memberships 
                        if m in content.objectIds(SITE_FOLDER_TYPES)]
            siteInstances = [getattr(content,s) 
                             for s in siteMembershipIds]
            self.__sites = [createObject('groupserver.SiteInfo', s)
                            for s in siteInstances]
        assert type(self.__sites) == list
        return self.__sites


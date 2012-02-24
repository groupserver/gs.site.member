# coding=utf-8
from zope.interface import Attribute
from zope.schema import *
from zope.contentprovider.interfaces import IContentProvider

class IGSSiteMembershipsContentProvider(IContentProvider):
    """The ABEL Profile Properties Content Provider"""
    pageTemplateFileName = Text(title=u"Page Template File Name",
      description=u'The name of the ZPT file that is used to '\
        u'render the information',
      required=False,
      default=u"browser/templates/sitememberships.pt")


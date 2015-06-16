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
from zope.schema import Text
from zope.contentprovider.interfaces import IContentProvider


class IGSSiteMembershipsContentProvider(IContentProvider):
    """The site memberships content provider"""
    pageTemplateFileName = Text(title="Page Template File Name",
      description='The name of the ZPT file that is used to render the '
        'information',
      required=False,
      default="browser/templates/sitememberships.pt")

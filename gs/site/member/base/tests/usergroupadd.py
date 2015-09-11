# -*- coding: utf-8 -*-
############################################################################
#
# Copyright © 2015 OnlineGroups.net and Contributors.
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
from __future__ import absolute_import, unicode_literals
from unittest import TestCase
from mock import patch, MagicMock
from gs.site.member.base.usergroupadd import (
    SiteAddError, member_added, JOIN_SITE_MEMBER, )


class TestAdd(TestCase):
    '''Test joining a group'''

    def setUp(self):
        self.mockEvent = MagicMock()
        ui = self.mockEvent.memberInfo
        ui.id = b'example_user'
        gi = self.mockEvent.groupInfo
        si = gi.siteInfo
        si.id = b'example_site'

    @patch('gs.site.member.base.usergroupadd.user_member_of_site')
    @patch('gs.site.member.base.usergroupadd.SiteMemberAuditor')
    def test_already_a_member(self, Mock_SMA, mock_umos):
        'Test adding someone who is already a site member'
        mock_umos.return_value = True

        member_added(MagicMock(), self.mockEvent)

        Mock_SMA().info.assert_called_once_with(JOIN_SITE_MEMBER)

    @patch('gs.site.member.base.usergroupadd.user_member_of_site')
    @patch('gs.site.member.base.usergroupadd.SiteMemberAuditor')
    def test_site_member_issues(self, Mock_SMA, mock_umos):
        'Test that an error is raised if someone is not a member at the end'
        mock_umos.side_effect = (True, False)

        with self.assertRaises(SiteAddError):
            member_added(MagicMock(), self.mockEvent)

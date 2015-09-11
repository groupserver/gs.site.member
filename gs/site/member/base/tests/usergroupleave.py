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
from gs.site.member.base.usergroupleave import (
    member_removed, LEAVE_SITE_MEMBER, LEAVE_SITE, SiteLeaveError)


class TestLeave(TestCase):
    '''Test the event handler for a person leaving a group'''

    def setUp(self):
        self.mockEvent = MagicMock()
        ui = self.mockEvent.memberInfo
        ui.id = b'example_user'
        gi = self.mockEvent.groupInfo
        si = gi.siteInfo
        si.id = b'example_site'

    @patch('gs.site.member.base.usergroupleave.user_member_of_group_on_site')
    @patch('gs.site.member.base.usergroupleave.SiteMemberAuditor')
    def test_member_not_removed(self, Mock_SMA, mock_umogos):
        '''Ensure a member of groups on the site stays on the stite'''
        mock_umogos.return_value = True
        mockContext = MagicMock()

        member_removed(mockContext, self.mockEvent)
        Mock_SMA().info.assert_called_once_with(LEAVE_SITE_MEMBER)

    @patch('gs.site.member.base.usergroupleave.notify')
    @patch('gs.site.member.base.usergroupleave.user_member_of_group_on_site')
    @patch('gs.site.member.base.usergroupleave.SiteMemberAuditor')
    def test_del_groups(self, Mock_SMA, mock_umogos, mock_notify):
        'Test that the groups are deleted from the user'
        mock_umogos.return_value = False
        mockContext = MagicMock()
        mock_site_root = mockContext.site_root()
        mock_acl_users = getattr(mock_site_root, 'acl_users')

        member_removed(mockContext, self.mockEvent)

        mock_acl_users.delGroupsFromUser.assert_called_once_with(
            [b'example_site_member'], b'example_user')
        Mock_SMA().info.assert_called_once_with(LEAVE_SITE)
        self.assertEqual(1, mock_notify.call_count)

    @patch('gs.site.member.base.usergroupleave.notify')
    @patch('gs.site.member.base.usergroupleave.user_member_of_group_on_site')
    @patch('gs.site.member.base.usergroupleave.SiteMemberAuditor')
    @patch('gs.site.member.base.usergroupleave.log')
    def test_del_groups_issue(self, mock_log, Mock_SMA, mock_umogos, mock_notify):
        'Test that a value-error is turned into a warning'
        mock_umogos.return_value = False
        mockContext = MagicMock()
        mock_site_root = mockContext.site_root()
        mock_acl_users = getattr(mock_site_root, 'acl_users')
        mock_acl_users.delGroupsFromUser.side_effect = ValueError('Because testing')

        member_removed(mockContext, self.mockEvent)

        mock_acl_users.delGroupsFromUser.assert_called_once_with(
            [b'example_site_member'], b'example_user')
        self.assertEqual(0, Mock_SMA().info.call_count)
        self.assertEqual(0, mock_notify.call_count)
        self.assertEqual(1, mock_log.warning.call_count)

    @patch('gs.site.member.base.usergroupleave.user_member_of_site')
    @patch('gs.site.member.base.usergroupleave.user_member_of_group_on_site')
    @patch('gs.site.member.base.usergroupleave.SiteMemberAuditor')
    def test_still_a_member(self, Mock_SMA, mock_umogos, mock_umos):
        'Test the handling of borken people'
        mock_umogos.return_value = False
        mock_umos.return_value = True
        mockContext = MagicMock()
        mock_site_root = mockContext.site_root()
        mock_acl_users = getattr(mock_site_root, 'acl_users')

        with self.assertRaises(SiteLeaveError):
            member_removed(mockContext, self.mockEvent)
        mock_acl_users.delGroupsFromUser.assert_called_once_with(
            [b'example_site_member'], b'example_user')

# coding=utf-8
from Products.GSGroupMember.groupmembership import member_id
from gs.group.member.base.utils import user_member_of_site
from audit import SiteMemberAuditor, JOIN_SITE, JOIN_SITE_MEMBER

def member_added(context, event):
    groupInfo = event.groupInfo
    userInfo = event.memberInfo
    siteInfo = groupInfo.siteInfo
    auditor = SiteMemberAuditor(context, userInfo, siteInfo)

    if user_member_of_site(userInfo, siteInfo.siteObj):
        auditor.info(JOIN_SITE_MEMBER)
    else:
        site_root = context.site_root()
        acl_users = getattr(site_root, 'acl_users')
        assert acl_users, 'ACL Users not found in site_root'

        groupNames = acl_users.getGroupNames()
        siteInfo = groupInfo.siteInfo
        memberGroupId = member_id(siteInfo.id)
        assert memberGroupId in groupNames, \
            '%s not in %s' % (memberGroupId, groupNames)
        acl_users.addGroupsToUser([memberGroupId], userInfo.id)
        auditor.info(JOIN_SITE)
    assert user_member_of_site(userInfo, siteInfo.siteObj)


# coding=utf-8
from Products.GSGroupMember.groupmembership import member_id
from gs.group.member.base.utils import user_member_of_site
from gs.groups.interfaces import IGSGroupsInfo
from audit import SiteMemberAuditor, LEAVE_SITE, LEAVE_SITE_MEMBER

def member_removed(context, event):
    groups = context
    groupInfo = event.groupInfo
    userInfo = event.memberInfo
    siteInfo = groupInfo.siteInfo
    auditor = SiteMemberAuditor(context, userInfo, siteInfo)
    
    if user_member_of_group_on_site(context, userInfo):
        auditor.info(LEAVE_SITE_MEMBER)
    else:
        site_root = context.site_root()
        acl_users = getattr(site_root, 'acl_users')
        assert acl_users, 'ACL Users not found in site_root'
        memberGroupId = member_id(siteInfo.id)
        acl_users.delGroupsFromUser([memberGroupId], userInfo.id)
        auditor.info(LEAVE_SITE)
        assert not(user_member_of_site(userInfo, siteInfo.siteObj))

def user_member_of_group_on_site(context, userInfo):
    groupsInfo = IGSGroupsInfo(context)
    u = userInfo.user
    groups = groupsInfo.get_member_groups_for_user(u, u)
    retval = bool(groups)
    return retval


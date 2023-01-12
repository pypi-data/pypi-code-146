from commonfate.paths.api_v1_admin_groups_group_id.get import ApiForget
from commonfate.paths.api_v1_admin_groups_group_id.put import ApiForput
from commonfate.paths.api_v1_admin_groups_group_id.delete import ApiFordelete


class ApiV1AdminGroupsGroupId(
    ApiForget,
    ApiForput,
    ApiFordelete,
):
    pass

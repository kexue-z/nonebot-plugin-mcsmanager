from .database_models import PermittedUser
from .models import Instance
from typing import List


async def get_permitteduser_instances_list(user_id: str) -> List[Instance]:
    _l = await PermittedUser.filter(user_id=user_id).values_list(
        "id",
        "permitted_instantce__instance_uuid",
        "permitted_instantce__remote_uuid",
        "permitted_instantce__name",
        "permitted_instantce__server_info__url",
        "permitted_instantce__server_info__apikey",
    )
    instances: List[Instance] = []

    for i in _l:
        ins = Instance(
            id=i[0],
            instance_uuid=i[1],
            remote_uuid=i[2],
            name=i[3],
            url=i[4],
            apikey=i[5],
        )
        instances.append(ins)

    return instances

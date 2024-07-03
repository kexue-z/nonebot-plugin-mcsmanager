from nonebot_plugin_tortoise_orm import add_model
from tortoise import fields
from tortoise.models import Model

model_path = "nonebot_plugin_mcsmanager.database_models"

add_model(model_path)


class PermittedUser(Model):
    """
    :说明: `PermittedUser`
    > 允许用户的表
    """

    id = fields.IntField(primary_key=True)
    user_id = fields.CharField(max_length=30)
    permitted_instantce: fields.ManyToManyRelation["PermittedInstantce"] = (
        fields.ManyToManyField(
            "default.PermittedInstantce",
            related_name="permitted_users",
            through="permitted_user_instantce",
        )
    )


class ServerInfo(Model):
    id = fields.IntField(primary_key=True)
    url = fields.TextField()
    apikey = fields.TextField()

    creator: fields.ReverseRelation["AdminUser"]


class PermittedInstantce(Model):
    id = fields.IntField(primary_key=True)
    instance_uuid = fields.TextField()
    remote_uuid = fields.TextField()
    name = fields.CharField(max_length=30, unique=True)
    server_info: fields.ForeignKeyRelation[ServerInfo] = fields.ForeignKeyField(
        "default.ServerInfo"
    )

    permitted_users: fields.ManyToManyRelation[PermittedUser]


class AdminUser(Model):
    id = fields.IntField(primary_key=True)
    user_id = fields.CharField(max_length=30)
    server: fields.OneToOneRelation[ServerInfo] = fields.OneToOneField(
        "default.ServerInfo", on_delete=fields.OnDelete.CASCADE, related_name="creator"
    )

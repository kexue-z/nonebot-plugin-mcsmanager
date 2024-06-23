from nonebot_plugin_tortoise_orm import add_model
from tortoise import fields
from tortoise.models import Model

model_path = "nonebot_plugin_mcsmanager.database_models"

add_model(model_path)


class PermittedUser(Model):
    id = fields.IntField(primary_key=True)
    user_id = fields.CharField(max_length=30)
    permitted_instantce: fields.ManyToManyRelation["PermittedInstantce"] = (
        fields.ManyToManyField(
            "default.PermittedInstantce",
        )
    )


class ServerInfo(Model):
    id = fields.IntField(primary_key=True)


class PermittedInstantce(Model):
    id = fields.IntField(primary_key=True)
    instance_uuid = fields.TextField()
    remote_uuid = fields.TextField()

    permitted_users: fields.ManyToManyRelation[PermittedUser]


class UserTable(Model):
    id = fields.IntField(primary_key=True)
    user_id = fields.CharField(max_length=30)
    # bind_server = fields.ForeignKeyField

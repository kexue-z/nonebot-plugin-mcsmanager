from nonebot_plugin_tortoise_orm import add_model
from tortoise import fields
from tortoise.models import Model

model_path = "nonebot_plugin_mcsmanager.database_models"

add_model(model_path)


class ServerInfo(Model):
    id = fields.IntField(primary_key=True)
    url = fields.TextField()
    apikey = fields.TextField()

    user: fields.ManyToManyRelation["Users"]

    class Meta:
        table = "nonebot_plugin_mcsmanager_server_info"


class Users(Model):
    id = fields.IntField(primary_key=True)
    user_id = fields.CharField(max_length=30)

    servers: fields.ManyToManyRelation[ServerInfo] = fields.ManyToManyField(
        "default.ServerInfo",
        related_name="nonebot_plugin_mcsmanager_users",
        on_delete=fields.OnDelete.CASCADE,
    )

    class Meta:
        table = "nonebot_plugin_mcsmanager_users"

from tortoise import fields
from tortoise.models import Model

from locales import Language


class User(Model):
    user_id = fields.IntField(unique=True)
    username = fields.CharField(max_length=255, null=True)
    full_name = fields.CharField(max_length=255)
    language = fields.CharField(max_length=20, default=str(Language.RU))
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "users"

    def __str__(self):
        return f"[{self.user_id}] {self.full_name}"


class Request(Model):
    user_id = fields.IntField(null=False)
    url = fields.CharField(max_length=255)
    created_at = fields.DatetimeField(auto_now_add=True)
    duration = fields.IntField(null=True)

    class Meta:
        table = "requests"

    def __str__(self):
        return f"[{self.user_id}] {self.url}"

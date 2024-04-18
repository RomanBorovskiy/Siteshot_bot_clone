from tortoise.models import Model
from tortoise import fields

from app.locales import Language


class User(Model):
    user_id = fields.IntField(unique=True)
    username = fields.CharField(max_length=255, null=True)
    full_name = fields.CharField(max_length=255)
    language = fields.CharField(max_length=20, default=str(Language.RU))

    class Meta:
        table = "users"

    def __str__(self):
        return f"[{self.user_id}] {self.full_name}"

from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    username = models.CharField(max_length=30, unique=True)
    email = models.CharField(max_length=64, unique=True)
    pass


class Completion(models.Model):
    itemid = models.IntegerField()
    compendium_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_completions"
    )

    def __str__(self):
        return f"{self.compendium_user.username} completed {self.itemid}"

    class Meta:
        unique_together = (
            "itemid",
            "compendium_user",
        )


class Todo(models.Model):
    itemid = models.IntegerField()
    list_writer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="todo_list"
    )

    def __str__(self):
        return f"{self.list_writer.username} prioritises {self.itemid}"

    class Meta:
        unique_together = (
            "itemid",
            "list_writer",
        )

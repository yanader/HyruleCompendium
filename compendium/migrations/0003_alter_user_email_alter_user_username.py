# Generated by Django 4.2.6 on 2023-10-22 19:26

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("compendium", "0002_completion"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="email",
            field=models.CharField(max_length=64, unique=True),
        ),
        migrations.AlterField(
            model_name="user",
            name="username",
            field=models.CharField(max_length=30, unique=True),
        ),
    ]
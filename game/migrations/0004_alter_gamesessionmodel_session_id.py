# Generated by Django 4.1 on 2022-09-06 19:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("game", "0003_waitinglistmodel_time_added"),
    ]

    operations = [
        migrations.AlterField(
            model_name="gamesessionmodel",
            name="session_id",
            field=models.TextField(),
        ),
    ]

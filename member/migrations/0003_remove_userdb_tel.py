# Generated by Django 4.1.4 on 2022-12-27 11:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("member", "0002_rename_userid_userdb_id"),
    ]

    operations = [
        migrations.RemoveField(model_name="userdb", name="tel",),
    ]
# Generated by Django 2.2.1 on 2019-06-08 18:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0002_auto_20190608_1451'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='timestap',
            new_name='timestamp',
        ),
    ]

# Generated by Django 2.2.1 on 2019-06-08 18:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0003_auto_20190608_1536'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='timestamp',
            field=models.DateField(auto_now=True),
        ),
    ]

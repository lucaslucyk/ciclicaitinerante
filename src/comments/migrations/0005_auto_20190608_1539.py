# Generated by Django 2.2.1 on 2019-06-08 18:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0004_auto_20190608_1537'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]

# Generated by Django 2.1.1 on 2019-06-25 05:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_auto_20190624_1425'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='department',
        ),
    ]
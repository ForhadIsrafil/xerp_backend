# Generated by Django 2.1.1 on 2019-06-29 05:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20190626_2344'),
    ]

    operations = [
        migrations.AddField(
            model_name='invitation',
            name='email',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
    ]
# Generated by Django 2.1.1 on 2019-06-30 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0004_auto_20190630_1737'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='issue',
            name='title',
            field=models.CharField(default=None, max_length=255),
            preserve_default=False,
        ),
    ]
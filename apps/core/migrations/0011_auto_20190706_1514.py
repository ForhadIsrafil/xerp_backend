# Generated by Django 2.1.1 on 2019-07-06 09:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_auto_20190706_1141'),
    ]

    operations = [
        migrations.AlterField(
            model_name='model',
            name='app',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.App'),
        ),
    ]

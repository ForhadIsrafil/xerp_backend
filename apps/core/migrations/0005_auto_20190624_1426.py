# Generated by Django 2.1.1 on 2019-06-24 08:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20190624_0602'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.Address'),
        ),
    ]

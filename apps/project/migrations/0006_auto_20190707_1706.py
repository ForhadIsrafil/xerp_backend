# Generated by Django 2.1.1 on 2019-07-07 11:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0005_auto_20190630_2118'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='owner', to='user.User'),
        ),
    ]
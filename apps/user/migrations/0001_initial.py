# Generated by Django 2.1.1 on 2019-06-23 17:25

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
        ('core', '0002_taskissueresulationaudit_task'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('security_code', models.TextField(blank=True, null=True)),
                ('image_url', models.CharField(blank=True, max_length=255, null=True)),
                ('is_2f_auth_enabled', models.BooleanField(default=False)),
                ('authy_id', models.CharField(blank=True, max_length=50, null=True)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Company')),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Department')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='UserAWSBucketInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.User')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
# Generated by Django 2.1.1 on 2019-06-23 17:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('project', '0001_initial'),
        ('core', '0002_taskissueresulationaudit_task'),
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='taskissueresulationaudit',
            name='updated_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='user.User'),
        ),
        migrations.AddField(
            model_name='taskfolloweraudit',
            name='task',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='project.Task'),
        ),
        migrations.AddField(
            model_name='taskfolloweraudit',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='user.User'),
        ),
        migrations.AddField(
            model_name='taskdetailaudit',
            name='task',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='project.Task'),
        ),
        migrations.AddField(
            model_name='taskaudit',
            name='goal',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='project.Goal'),
        ),
        migrations.AddField(
            model_name='taskaudit',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='user.User'),
        ),
        migrations.AddField(
            model_name='taskaudit',
            name='updated_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='user.User'),
        ),
        migrations.AddField(
            model_name='state',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='self', to='core.State'),
        ),
        migrations.AddField(
            model_name='role',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Company'),
        ),
        migrations.AddField(
            model_name='projectaudit',
            name='company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='core.Company'),
        ),
        migrations.AddField(
            model_name='projectaudit',
            name='updated_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='user.User'),
        ),
        migrations.AddField(
            model_name='model',
            name='app',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.App'),
        ),
        migrations.AddField(
            model_name='licenseaudit',
            name='app',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.App'),
        ),
        migrations.AddField(
            model_name='licenseaudit',
            name='company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.Company'),
        ),
        migrations.AddField(
            model_name='license',
            name='app',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.App'),
        ),
        migrations.AddField(
            model_name='license',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Company'),
        ),
        migrations.AddField(
            model_name='issuedetailsaudit',
            name='task',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='project.Task'),
        ),
        migrations.AddField(
            model_name='issueaudit',
            name='project',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='project.Project'),
        ),
        migrations.AddField(
            model_name='issueaudit',
            name='task',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='project.Task'),
        ),
        migrations.AddField(
            model_name='issueaudit',
            name='updated_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='user.User'),
        ),
        migrations.AddField(
            model_name='invitation',
            name='department',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Department'),
        ),
        migrations.AddField(
            model_name='goalaudit',
            name='company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.Company'),
        ),
        migrations.AddField(
            model_name='goalaudit',
            name='project',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='project.Project'),
        ),
        migrations.AddField(
            model_name='goalaudit',
            name='updated_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='user.User'),
        ),
        migrations.AddField(
            model_name='departmentrolemodelpermissionaudit',
            name='department',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='core.Department'),
        ),
        migrations.AddField(
            model_name='departmentrolemodelpermissionaudit',
            name='model',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.Model'),
        ),
        migrations.AddField(
            model_name='departmentrolemodelpermissionaudit',
            name='permission',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.Permission'),
        ),
        migrations.AddField(
            model_name='departmentrolemodelpermissionaudit',
            name='role',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.Role'),
        ),
        migrations.AddField(
            model_name='departmentrolemodelpermission',
            name='department',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Department'),
        ),
        migrations.AddField(
            model_name='departmentrolemodelpermission',
            name='model',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Model'),
        ),
        migrations.AddField(
            model_name='departmentrolemodelpermission',
            name='permission',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Permission'),
        ),
        migrations.AddField(
            model_name='departmentrolemodelpermission',
            name='role',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Role'),
        ),
        migrations.AddField(
            model_name='departmentmodelpermissionaudit',
            name='department',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.Department'),
        ),
        migrations.AddField(
            model_name='departmentmodelpermissionaudit',
            name='model',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.Model'),
        ),
        migrations.AddField(
            model_name='departmentmodelpermissionaudit',
            name='permission',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.Permission'),
        ),
        migrations.AddField(
            model_name='departmentmodelpermission',
            name='department',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Department'),
        ),
        migrations.AddField(
            model_name='departmentmodelpermission',
            name='model',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Model'),
        ),
        migrations.AddField(
            model_name='departmentmodelpermission',
            name='permission',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Permission'),
        ),
        migrations.AddField(
            model_name='department',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Company'),
        ),
        migrations.AddField(
            model_name='country',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='self', to='core.Country'),
        ),
        migrations.AddField(
            model_name='company',
            name='address',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Address'),
        ),
        migrations.AddField(
            model_name='city',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='self', to='core.City'),
        ),
        migrations.AddField(
            model_name='address',
            name='city',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.City'),
        ),
        migrations.AddField(
            model_name='address',
            name='country',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.Country'),
        ),
        migrations.AddField(
            model_name='address',
            name='state',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.State'),
        ),
    ]
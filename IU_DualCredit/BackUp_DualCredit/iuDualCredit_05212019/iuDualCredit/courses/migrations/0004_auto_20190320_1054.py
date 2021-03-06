# Generated by Django 2.1.7 on 2019-03-20 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('enrollments', '0001_initial'),
        ('courses', '0003_auto_20190320_1013'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='classdata',
            name='enrollment',
        ),
        migrations.AddField(
            model_name='classdata',
            name='enrollment',
            field=models.ManyToManyField(to='enrollments.Enrollments'),
        ),
        migrations.RemoveField(
            model_name='classdata',
            name='grantEnrollment',
        ),
        migrations.AddField(
            model_name='classdata',
            name='grantEnrollment',
            field=models.ManyToManyField(to='enrollments.GrantEnrollmentData'),
        ),
    ]

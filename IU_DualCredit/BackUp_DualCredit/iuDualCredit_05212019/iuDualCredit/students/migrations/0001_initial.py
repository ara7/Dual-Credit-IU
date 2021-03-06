# Generated by Django 2.1.7 on 2019-04-07 22:42

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('University_ID', models.IntegerField(default=0)),
                ('Appl_Nbr', models.IntegerField(default=0)),
                ('Effective_Date', models.DateField(blank=True, default=datetime.datetime.now)),
                ('Academic_Plan_Code', models.CharField(max_length=200)),
                ('Academic_Program_Code', models.CharField(max_length=200)),
                ('Institution_Code', models.CharField(max_length=200)),
                ('First_Name', models.CharField(max_length=200)),
                ('Last_Name', models.CharField(max_length=200)),
                ('Middle_Name', models.CharField(max_length=200)),
                ('Other_Email_Address', models.CharField(max_length=200)),
                ('GDS_Campus_Email_Address', models.CharField(max_length=200)),
                ('Network_ID', models.CharField(max_length=200)),
            ],
        ),
    ]

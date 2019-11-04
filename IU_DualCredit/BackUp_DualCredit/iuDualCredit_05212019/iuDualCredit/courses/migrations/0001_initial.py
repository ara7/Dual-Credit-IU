# Generated by Django 2.1.7 on 2019-03-19 22:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ClassData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('CLS_NBR', models.IntegerField()),
                ('CRS_ID', models.IntegerField()),
                ('ACAD_TERM_CD', models.IntegerField()),
                ('CLS_INSTR_NM', models.TextField(blank=True)),
                ('CLS_INSTR_GDS_CMP_EMAIL_ADDR', models.TextField(blank=True)),
                ('CAMPUS', models.CharField(max_length=200)),
                ('ENROLLMENT_CAP', models.IntegerField()),
                ('ENROLLMENT_TOTAL', models.IntegerField()),
            ],
        ),
    ]

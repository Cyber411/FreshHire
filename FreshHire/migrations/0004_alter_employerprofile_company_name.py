# Generated by Django 5.1.1 on 2025-02-06 22:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FreshHire', '0003_alter_seekerprofile_resume'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employerprofile',
            name='company_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]

# Generated by Django 3.0.2 on 2023-04-30 20:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0008_report_society'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='is_archived',
            field=models.BooleanField(default=False),
        ),
    ]

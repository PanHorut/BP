# Generated by Django 5.1.4 on 2025-02-05 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_task_skills'),
    ]

    operations = [
        migrations.AddField(
            model_name='skill',
            name='height',
            field=models.IntegerField(default=0),
        ),
    ]

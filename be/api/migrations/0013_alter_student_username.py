# Generated by Django 5.1.4 on 2025-02-12 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_skill_height'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='username',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]

# Generated by Django 5.1.4 on 2025-03-14 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0018_audioprompt'),
    ]

    operations = [
        migrations.AddField(
            model_name='skill',
            name='deleted',
            field=models.BooleanField(default=False),
        ),
    ]

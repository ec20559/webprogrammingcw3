# Generated by Django 4.2.6 on 2023-12-21 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='favorite_topic',
            field=models.CharField(blank=True, default=None, max_length=75, null=True),
        ),
    ]

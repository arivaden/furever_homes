# Generated by Django 4.1.2 on 2022-10-26 05:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fureverhomes_users_app', '0003_remove_futureowner_other_preferences_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='petprofile',
            name='date_uploaded',
            field=models.DateField(default='2022-10-25'),
        ),
    ]

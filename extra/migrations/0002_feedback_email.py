# Generated by Django 2.2.6 on 2020-05-14 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('extra', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedback',
            name='email',
            field=models.EmailField(max_length=70, null=True),
        ),
    ]

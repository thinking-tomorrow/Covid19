# Generated by Django 3.0.5 on 2020-04-30 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('covid', '0010_auto_20200429_2304'),
    ]

    operations = [
        migrations.AddField(
            model_name='countrydata',
            name='continent',
            field=models.TextField(default='World'),
            preserve_default=False,
        ),
    ]
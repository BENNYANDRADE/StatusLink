# Generated by Django 3.2 on 2023-02-28 20:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administrators', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='linkinfo',
            name='expiration_date',
            field=models.DateField(blank=True, db_column='ExpirationDate', null=True),
        ),
    ]

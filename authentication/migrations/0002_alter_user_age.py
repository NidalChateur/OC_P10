# Generated by Django 4.2.5 on 2023-09-12 02:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='age',
            field=models.DateField(blank=True, null=True),
        ),
    ]

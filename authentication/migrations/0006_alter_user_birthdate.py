# Generated by Django 4.2.5 on 2023-09-28 22:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0005_alter_user_first_name_alter_user_last_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='birthdate',
            field=models.DateField(blank=True, help_text='Vous devez avoir plus de 15 ans.', null=True, verbose_name='Date de naissance'),
        ),
    ]
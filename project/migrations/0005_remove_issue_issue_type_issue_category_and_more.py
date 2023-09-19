# Generated by Django 4.2.5 on 2023-09-19 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0004_issue'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='issue',
            name='issue_type',
        ),
        migrations.AddField(
            model_name='issue',
            name='category',
            field=models.CharField(blank=True, choices=[('Bug', 'Bug'), ('Feature', 'Feature'), ('Task', 'Task')], max_length=32, null=True, verbose_name='Balise'),
        ),
        migrations.AlterField(
            model_name='issue',
            name='name',
            field=models.CharField(blank=True, max_length=256, null=True, verbose_name='Nom'),
        ),
        migrations.AlterField(
            model_name='issue',
            name='priority',
            field=models.CharField(choices=[('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High')], max_length=32, verbose_name='Priorité'),
        ),
        migrations.AlterField(
            model_name='issue',
            name='status',
            field=models.CharField(choices=[('To Do', 'To Do'), ('In Progress', 'In Progress'), ('Finished', 'Finished')], default='To Do', max_length=32, verbose_name='Statut'),
        ),
    ]

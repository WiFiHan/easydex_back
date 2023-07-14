# Generated by Django 4.2 on 2023-07-11 08:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0002_rename_indicator_index'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='index',
            name='content',
        ),
        migrations.RemoveField(
            model_name='index',
            name='title',
        ),
        migrations.AddField(
            model_name='index',
            name='closing',
            field=models.CharField(blank=True, default='0.00', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='index',
            name='name',
            field=models.CharField(default='Dow Jones', max_length=100),
        ),
        migrations.AddField(
            model_name='index',
            name='opening',
            field=models.CharField(blank=True, default='0.00', max_length=100, null=True),
        ),
    ]
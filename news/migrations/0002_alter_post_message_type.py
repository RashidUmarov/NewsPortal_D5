# Generated by Django 4.1.2 on 2022-11-08 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='message_type',
            field=models.CharField(choices=[('NEWS', 'news'), ('ART', 'article')], max_length=4),
        ),
    ]

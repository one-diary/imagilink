# Generated by Django 3.2.4 on 2021-08-14 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imagilink_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='links',
            name='author',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='links',
            name='seo_image',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]
# Generated by Django 3.0.8 on 2020-07-11 22:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20200709_1418'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='uploads/avatars/%Y/%m/%d/'),
        ),
    ]
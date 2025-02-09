# Generated by Django 4.1 on 2022-08-10 08:15

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0006_commercialproject_commercialphotos'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Photo',
            new_name='PersonalPhotos',
        ),
        migrations.RenameModel(
            old_name='Post',
            new_name='PersonalProject',
        ),
        migrations.AlterField(
            model_name='commercialphotos',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='imgs/commercial/<django.db.models.query_utils.DeferredAttribute object at 0x000001C48B683A30>/'),
        ),
    ]

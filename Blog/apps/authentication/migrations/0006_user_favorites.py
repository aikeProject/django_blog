# Generated by Django 2.2.6 on 2019-10-23 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0002_auto_20191021_0729'),
        ('authentication', '0005_user_follows'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='favorites',
            field=models.ManyToManyField(related_name='favorite_by', to='articles.Article'),
        ),
    ]

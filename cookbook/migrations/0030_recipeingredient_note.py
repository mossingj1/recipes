# Generated by Django 3.0.4 on 2020-03-17 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cookbook', '0029_auto_20200317_1901'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipeingredient',
            name='note',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
    ]

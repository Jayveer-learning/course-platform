# Generated by Django 5.1.5 on 2025-02-08 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emails', '0003_alter_emailverification_parent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailverification',
            name='attempts',
            field=models.IntegerField(null=True),
        ),
    ]

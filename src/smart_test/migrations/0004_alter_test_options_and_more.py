# Generated by Django 5.1 on 2024-08-26 21:16

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smart_test', '0003_remove_testresult_score'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='test',
            options={'ordering': ['title']},
        ),
        migrations.AlterField(
            model_name='testresult',
            name='num_correct_answers',
            field=models.PositiveSmallIntegerField(default=0, validators=[django.core.validators.MaxValueValidator(20)]),
        ),
        migrations.AlterField(
            model_name='testresult',
            name='num_incorrect_answers',
            field=models.PositiveSmallIntegerField(default=0, validators=[django.core.validators.MaxValueValidator(20)]),
        ),
    ]

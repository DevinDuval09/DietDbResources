# Generated by Django 4.0.5 on 2022-07-27 03:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FoodJournal', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='foods',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='meals',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='measurements',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]

# Generated by Django 3.0.7 on 2020-06-30 17:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0002_auto_20200626_1709'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leadcontact',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='client.Client'),
        ),
    ]

# Generated by Django 2.1.4 on 2018-12-09 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendas', '0004_venda_vendedor'),
    ]

    operations = [
        migrations.AddField(
            model_name='venda',
            name='data',
            field=models.DateField(auto_created=True, default='2018-01-01'),
            preserve_default=False,
        ),
    ]

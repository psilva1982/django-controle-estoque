# Generated by Django 2.1.4 on 2018-12-09 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estoque', '0002_auto_20181206_1358'),
    ]

    operations = [
        migrations.AlterField(
            model_name='estoqueentrada',
            name='entrada',
            field=models.CharField(choices=[('cp', 'Compra para revenda'), ('dv', 'Cancelamento de venda'), ('ou', 'Outros')], default='cp', max_length=2),
        ),
    ]